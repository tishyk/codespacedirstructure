#! /usr/bin/python

# This is a simple gem_utils.py wrapper for turning off or on all engine drives

import argparse
import copy
import json
import logging
import os
import re
import sys
from time import sleep
from datetime import datetime

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt="%b %d %H:%M:%S")
firmware_gem_utils_dir_path = '../seagate/laguna-seca/fwtool-usm/'  # Firmware tool gem_util.py script
gem_utils_dir_path = '/avid/tools/bin/'  # System tool gem_util.py script

try:
    if os.path.exists(firmware_gem_utils_dir_path):
        gem_utils_dir_path = firmware_gem_utils_dir_path
    sys.path.append(gem_utils_dir_path)
    import gem_utils as gu
except ImportError:
    logging.error("gem_utils.py file not found!")
    sys.exit(1)


# noinspection PyShadowingNames
class BaseDriveMgr:
    CMD_POWER_OFF = 'poweroffdrive'
    CMD_POWER_ON = 'powerondrive'
    CMD_DRIVE_DUMP = 'dumpdrives'
    RETRIES = 60  # command fail retries
    TIMEOUT = 0.3  # TIMEOUT between each retry
    DUMP_FILE = '/perm/drive_map'

    def __init__(self):
        self.sgpath = BaseDriveMgr._get_sgpath()
        self.init_drive_power_map = self.__get_init_drive_map()

    @staticmethod
    def all_off():
        drive_mgr = BaseDriveMgr()
        try:
            drive_mgr.power_off_all()
        except KeyboardInterrupt:
            drive_mgr.power_on_all()
            raise KeyboardInterrupt
        drive_mgr.wait_all_drives_state('offline')
        logging.info(drive_mgr.get_dump())

    @staticmethod
    def all_on(timeout):
        drive_mgr = BaseDriveMgr()
        drive_mgr.power_on_all()
        drive_mgr.wait_all_drives_state('online', timeout)
        logging.info(drive_mgr.get_dump())
        drive_mgr.remove_drive_map_file()

    @staticmethod
    def _get_sgpath():
        ses_targets = gu.get_targets({'type': 13})
        if len(ses_targets) == 0 or not ses_targets[0].get('sgpath'):
            error_msg = 'No SES targets were found, exiting'
            gu.su.die(error_msg)
            raise AssertionError("gem_utils.py: {}".format(error_msg))
        sgpath = ses_targets[0]['sgpath']
        return sgpath

    def _get_drive_map(self, dump):
        """ Return dict with a slot as key and drive state as value"""
        d_map = re.findall('\[\s*(\d{1,2})\s+(\w+)', dump, re.S)
        assert d_map, "Could not parse {} output".format(self.CMD_DRIVE_DUMP)
        drive_map = dict(d_map)
        return drive_map

    @property
    def drive_power_map(self):
        dump = self.get_dump()
        return self._get_drive_map(dump)

    def get_dump(self):
        return self.__cli_call(self.CMD_DRIVE_DUMP)

    def power_off_all(self):
        drives_map = copy.copy(self.drive_power_map)
        for slot in drives_map:
            if self.drive_power_map[slot] == 'online':
                command = "{} {}".format(self.CMD_POWER_OFF, slot)
                self.__cli_call(command)

    def power_on_all(self):
        drives_map = copy.copy(self.drive_power_map)
        for slot in drives_map:
            if self.drive_power_map[slot] != 'online' and self.init_drive_power_map[slot] == 'online':
                command = "{} {}".format(self.CMD_POWER_ON, slot)
                self.__cli_call(command)

    def wait_all_drives_state(self, state, timeout=60):
        if timeout < 1:
            return 0
        for slot in self.drive_power_map:
            if self.init_drive_power_map[slot] != 'online':
                continue
            init_time = datetime.now()
            while (datetime.now() - init_time).seconds < timeout:
                if state == 'online' and self.drive_power_map[slot] == 'online':  # Check online
                    break
                elif state != 'online' and self.drive_power_map[slot] != 'online':  # Check offline
                    break
            else:
                logging.info(self.get_dump())
                raise RuntimeError("Drive slot {} not changed to {}!".format(slot, state))

    def remove_drive_map_file(self):
        try:
            if os.path.exists(self.DUMP_FILE):
                os.remove(self.DUMP_FILE)
        except OSError:
            msg = "Cannot delete temporary data file {}. Please delete it manually.".format(self.DUMP_FILE)
            logging.info(msg.format(self.DUMP_FILE))

    def __cli_call(self, command):
        """ Return str '' if call return 0, else return str with a traceback and error code or None"""
        result = None
        for i in range(self.RETRIES):
            result = gu.inband_cli(self.sgpath, module='local', command=command)
            if result is None or 'invalid' in result:
                sleep(self.TIMEOUT)
            else:
                break
        assert result is not None, ('Could not execute cli command: {}'.format(command))
        return result

    def __get_init_drive_map(self):
        drive_power_map = None
        if not os.path.exists(self.DUMP_FILE):
            power_map = self._get_drive_map(self.get_dump())
            with open(self.DUMP_FILE, 'wb') as jsonfile:
                json.dump(power_map, jsonfile)
        with open(self.DUMP_FILE, 'rb') as jsonfile:
            try:
                drive_power_map = json.load(jsonfile)
                assert drive_power_map
            except (ValueError, AssertionError):
                raise AssertionError("Backup drive map file is not valid")
        return drive_power_map


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", dest='timeout', type=int, default=60)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--all_on", dest='all_on', action="store_true", default=False, help="Turn on all engine drives")
    group.add_argument("--all_off", dest='all_off', action="store_true", default=False,
                       help="Turn off all engine drives")
    try:
        args = parser.parse_args()
        if args.all_off:
            BaseDriveMgr.all_off()
        elif args.all_on:
            BaseDriveMgr.all_on(args.timeout)
    except RuntimeError as msg:
        sys.exit(7)  # Not all initial drives turn back online
    except BaseException as msg:
        logging.error(msg)
        sys.exit(1)
    else:
        sys.exit(0)
