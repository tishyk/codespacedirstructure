#!/usr/bin/env python3

# @@ AVID HEADER - DO NOT EDIT @@
# Copyright 2017-2018 by Avid Technology, Inc.
# @@ AVID HEADER @@

import argparse
import base64
import os
import sys
import time
import uuid

import Pyro4
import Pyro4.naming
import humanize
import paramiko
from Pyro4.errors import NamingError
from paramiko.ssh_exception import SSHException, BadHostKeyException, NoValidConnectionsError, AuthenticationException

import make_zip
import sdm_common
from migration_logging import logger

pyro_server_ip = sdm_common.get_admin_ip()
UNIQUE_NAME = 'tmp_mgrn_{}'.format(uuid.uuid4().hex[:14])

WELCOME_MSG = "{1}{0}{1}\tSystem Director Migration process started!{1}{0}{1}".format('*' * 80, '\n')
SDA_Product_NAME = "SDA"
INDEXSERVER_CONFIG_FILE = sdm_common.INDEXSERVER_CONFIG_FILE
LOCAL_IP_IS_ESD_ERR = "File System migration from SDA to the same SDA. Check ESD virtual IP address."

CSMessage = "Reboot storage controller and try again!"
FS_PRESENCE_ERR = 'SDA File System found!'
NO_IS_MOUNTPOINT_ERR = "IndexServer configuration file not found!\n {}.".format(CSMessage)
PRODUCT_NAME_ERR = "SDA product name not found for this storage controller! Check SDA IP Address!"

WS_CREATION_ERR = "Temporary data creation failed."
SSH_CONNECTION_ERR = "Could not establish ssh remote session to '{}' ip address."  # Format with ip address
PROFILE_UPDATE_ERR = 'ESD Profile has not been updated correctly!\n' \
                     'Disable ESD System Director manually from Agent Page.\n' \
                     'Contact to the Avid Nexis Support for data loss prevention!!!\n'

# Format with esd virtual ip address - 0, and typed ip address from argument - 1
ESD_VIP_ERR = 'Entered ESD ip address is not valid virtual ip address for ESD!\n' \
              '"{0}" is a valid virtual ip address for entered "{1}" ip address.'


class MigrationMaster:
    def __init__(self):
        self.ns = None
        self.temp_data = tuple()
        self.temp_data_storage = None
        self.migration_agent_proxy = None
        self.agent_gx0_ssh = None
        self.agent_gx0_ip = ""

        self.args = self.parser.parse_args()
        self.check_arguments()
        self.ssh = self.ssh_connection()

    @property
    def parser(self):
        """ Set tool arguments
        :return: ArgumentParser object"""
        parser = argparse.ArgumentParser()
        parser.add_argument('esd_ip', help="ESD System Director virtual IP address to obtaining File System")
        parser.add_argument('esd_agent_password', help="ESD System Director host 'root' password")
        parser.add_argument('esd_mc_password', help="ESD Management Console 'Administrator' password \
                                                            (Can't be blank or none 'utf-8' encoding)")
        parser.add_argument('-f', '--force', action='store_true',
                            help="Skip build number, engine product name and workspace validation")
        parser.add_argument('--no_sda_verify', action='store_true',
                            help="Warning! Set this argument for skipping verification of SDA product name.")
        parser.add_argument('--no_data_validation', action='store_false',
                            help="Warning!!! Set this argument for skipping  verification of migrated data")

        parser.add_argument('--master_ip', help=argparse.SUPPRESS)  # Argument transferred to ESD agent.py call

        return parser

    def check_arguments(self):
        if self.args.master_ip:
            try:
                import agent
                agent.master_ip = self.args.master_ip
                agent.agent_main()
            except Exception as msg:
                logger.exception(msg)
            sys.exit()
        if self.args.force:
            self.args.no_sda_verify = True
            self.args.no_data_validation = False
        sdm_common.flockadminapi.NEED_API = self.args.no_data_validation

    def ssh_connection(self, ip=''):
        assert (pyro_server_ip != self.args.esd_ip), LOCAL_IP_IS_ESD_ERR  # check esd ip not the same as local ip
        try:
            ip = ip if ip else self.args.esd_ip
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, username='root', password=self.args.esd_agent_password)
            logger.info('SSH connection to ESD established successfully')
        except (SSHException, BadHostKeyException, NoValidConnectionsError) as msg:
            logger.exception(msg)
            _msg = 'Could not initialize ssh session. Check availability of "{}" IP address with submitted password'
            logger.critical(_msg.format(ip))
        except AuthenticationException as msg:
            logger.exception(msg)
            logger.critical('Check password for ESD host!')
        except TimeoutError as msg:
            logger.exception(msg)
            logger.critical('Could not found entered "{}" ESD host IP address. Timeout error!'.format(ip))
        else:
            return ssh
        raise RuntimeError(SSH_CONNECTION_ERR.format(self.args.esd_ip))

    def requirements_validation(self):
        self.check_sda()
        sdm_common.check_ssd_drives()
        self.clean = True
        self.check_esd_vip()

    def check_sda(self):
        assert os.path.exists(INDEXSERVER_CONFIG_FILE), NO_IS_MOUNTPOINT_ERR
        logger.debug("Path for indexServer configuration file exist '{}'".format(INDEXSERVER_CONFIG_FILE))
        if self.args.no_sda_verify:
            logger.warn('SDA product verification skipped!')
        else:
            # Make sure SDA have product name SDA not any other
            prod_name = sdm_common.get_product_name()
            logger.info("SDA Product Name: {}.".format(prod_name.strip()))
            if SDA_Product_NAME.lower() not in prod_name.lower():
                raise AssertionError(PRODUCT_NAME_ERR)
                # TODO: make sure SDA does not have a filesystem
            try:
                sdm_common.connect_flockadminapi(self.args.no_data_validation)
                raise RuntimeError(FS_PRESENCE_ERR)
            except AssertionError as msg:
                logger.exception(msg)
                logger.debug(sdm_common.flockadminapi.FAIL_APICONNECTION_MSG)

    def run_remote_command(self, command):
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            return stdout.channel.recv_exit_status()
        except Exception as msg:
            logger.exception(msg)

    def start_migration_agent(self):
        self.migration_agent_proxy = self.bootstrap_sdm_agent()
        self.clean = False
        self.migration_agent_proxy.ping()  # TODO: check/wait Agent up and running
        self.agent_gx0_ip = self.migration_agent_proxy.get_gx0_ip()

        logger.info('Client proxy started')

    def bootstrap_sdm_agent(self):

        package_pathname = make_zip.prepare_package()

        logger.info('Send package "{}" to "{}".'.format(package_pathname, self.args.esd_ip))
        t_begin = time.time()

        # TODO add connection error wrapper
        sftp = self.ssh.open_sftp()
        sftp.put(package_pathname, make_zip.PACKAGE_FILENAME)
        sftp.close()

        t_end = time.time()
        seconds_elapsed = int(t_end - t_begin)
        logger.info('Sent, elapsed time {}.'.format(humanize.naturaldelta(seconds_elapsed)))

        t_begin = time.time()

        logger.info('Will now start ESD migration agent at "{}".'.format(self.args.esd_ip))
        assert 0 == self.run_remote_command('rm -rf {}'.format(make_zip.PACKAGE_NAME))
        assert 0 == self.run_remote_command('unzip {}'.format(make_zip.PACKAGE_FILENAME))
        try:
            package_path = os.path.join(make_zip.PACKAGE_NAME, 'sd_migration')
            logger.debug("Package path is : {}".format(package_path))
            remote_cmd = './{} N N N --master_ip {}'.format(package_path, pyro_server_ip)
            self.ssh.exec_command(remote_cmd, timeout=15)
        except AssertionError:
            restart_agent = os.path.join(make_zip.PACKAGE_NAME, 'sd_migration')
            self.run_remote_command("/bin/sed -i -e 's/777/775/g' {}".format(restart_agent))
            result = self.run_remote_command('bash ./{} {}'.format(restart_agent, pyro_server_ip))
            if result != 0:
                raise RuntimeError("Could not start agent script on ESD!\n")

        t_end = time.time()
        seconds_elapsed = int(t_end - t_begin)
        time.sleep(15)
        pyro_proxy = Pyro4.Proxy('PYRONAME:SDMAgent@{}'.format(pyro_server_ip))
        logger.info('Started, elapsed time {}.'.format(humanize.naturaldelta(seconds_elapsed)))

        return pyro_proxy

    def download_fstar(self):
        logger.info('Will now download File System from ESD. Please wait..')
        t_begin = time.time()

        with open(sdm_common.FS_TAR_FILE_PATH, 'wb') as f:
            offset = 0
            size10mb = 10 * 1024 * 1024
            total = 0
            while True:
                buf = self.migration_agent_proxy.read_fstar(offset, size10mb)
                assert buf['encoding'] == 'base64' or not buf
                if len(buf['data']) == 0:  # EOF
                    break
                f.seek(offset)
                data = base64.b64decode(buf['data'])
                total += len(data)
                f.write(data)
                f.flush()

                offset += size10mb
            f.close()
        t_end = time.time()

        seconds_elapsed = int(t_end - t_begin)
        logger.info(
            'Transfer complete, elapsed time {}, bytes transferred {}.'.format(humanize.naturaldelta(seconds_elapsed),
                                                                               humanize.naturalsize(total,
                                                                                                    binary=True)))
        self.check_fstar_hash()

    def download_pdbin(self):
        logger.info('Will now download File System from ESD. Please wait..')
        t_begin = time.time()

        with open(sdm_common.FILESYSTEM_FILE, 'wb') as f:
            offset = 0
            size10mb = 10 * 1024 * 1024
            total = 0
            while True:
                buf = self.migration_agent_proxy.read_pdbin(offset, size10mb)
                assert buf['encoding'] == 'base64' or not buf
                if len(buf['data']) == 0:  # EOF
                    break
                f.seek(offset)
                data = base64.b64decode(buf['data'])
                total += len(data)
                f.write(data)
                f.flush()

                offset += size10mb
            f.close()
        t_end = time.time()

        seconds_elapsed = int(t_end - t_begin)
        logger.info(
            'Transfer complete, elapsed time {}, bytes transferred {}.'.format(humanize.naturaldelta(seconds_elapsed),
                                                                               humanize.naturalsize(total,
                                                                                                    binary=True)))

    def check_pdhash(self, reload_file_cycles=3):
        logger.info('Check filesystem files hash')
        sda_hexdigest = sdm_common.get_partition_hexdigets(sdm_common.FILESYSTEM_FILE)
        esd_hexdigest = self.migration_agent_proxy.get_partition_hexdigets(sdm_common.PARTITION_DUMPBIN_PATH)
        if sda_hexdigest != esd_hexdigest and reload_file_cycles:
            reload_file_cycles -= 1
            self.download_filesystem()
            self.check_partitiondump_hash(reload_file_cycles)
        elif sda_hexdigest != esd_hexdigest:
            logger.info('File system copy failed. Hash mismatch')
            raise RuntimeError('Filesystem files hash mismatch!')
        else:
            logger.info('Filesystem hash matched')

    def check_fstar_hash(self, reload_file_cycles=3):
        sda_hexdigest = sdm_common.get_partition_hexdigets(sdm_common.FS_TAR_FILE)
        esd_hexdigest = self.migration_agent_proxy.get_tar_hexdigest()
        if sda_hexdigest != esd_hexdigest and reload_file_cycles:
            reload_file_cycles -= 1
            self.download_fstar()
            self.check_fstar_hash(reload_file_cycles)
        elif sda_hexdigest != esd_hexdigest:
            logger.info('File system copy failed. Hash sum mismatch')
            raise RuntimeError('File systems hash sum mismatch!')
        else:
            logger.info('File system hash matched!')

    def check_esd_vip(self):
        ip_cmd = "/avid/sbin/profile -r admin.gx0.ipaddr"
        stdin, stdout, stderr = self.ssh.exec_command(ip_cmd)
        agent_vip_output = stdout.read().decode()
        if self.args.esd_ip not in agent_vip_output and "--" not in agent_vip_output:
            raise RuntimeError(ESD_VIP_ERR.format(agent_vip_output.strip(), self.args.esd_ip))

    def check_system_name(self):
        sda_sys_name = sdm_common.get_system_name()
        esd_sys_name = self.migration_agent_proxy.get_system_name()

        if sda_sys_name != esd_sys_name:
            logger.debug('SDA system name: {}'.format(sda_sys_name))
            logger.debug('ESD system name: {}'.format(esd_sys_name))
            raise RuntimeError('Different system names!')

        logger.info("System name: {}".format(sda_sys_name.strip()))
        return True

    def check_product_version(self):
        sda_pversion = sdm_common.get_product_version()
        esd_pversion = self.migration_agent_proxy.get_product_version()

        if sda_pversion != esd_pversion:
            logger.debug('SDA system name: {}'.format(sda_pversion))
            logger.debug('ESD system name: {}'.format(esd_pversion))
            raise RuntimeError('Different product versions!')
        self.clean = 0

        logger.info("Product version: {}".format(sda_pversion.strip()))

    def apply_filesystem_on_sda(self):
        """ Set configuration for import filesystem to indexserver.conf file.
        Start indexServer service on SDA.
        Check successful import with FS connect and WS/User temp data deleting. """
        sdm_common.apply_filesystem_on_sda()

    def apply_changes_on_esd(self):
        # wait for sysytemdirector reboot, gx0 interface is up, adminserver/indexServer service not started
        logger.info('Update ESD profile configuration')
        self.migration_agent_proxy.disable_sd()
        logger.info('Profile configuration on ESD updated')
        self.migration_agent_proxy.shutdown()
        self.ssh.close()
        logger.info('Wait for ESD controllers to reboot..')
        time.sleep(60 * 4)

        logger.info('Will now check profile configuration')
        self.check_profile_updates()

    def check_profile_updates(self):
        self.agent_gx0_ssh = self.ssh_connection(self.agent_gx0_ip)
        stdin, stdout, stderr = self.agent_gx0_ssh.exec_command('/avid/sbin/profile -r system.systemdirector')
        system_director = b'true' in stdout.read()
        if system_director:  # or not system_director_ip:
            logger.warn(PROFILE_UPDATE_ERR)
        else:
            logger.info('ESD System Director disabled. Profile configuration updated.')
        self.agent_gx0_ssh.close()

    def validate_sda_filesystem(self):
        if not self.args.no_data_validation:
            sdm_common.validate_sda_filesystem(self.args.no_data_validation, self.args.esd_mc_password, self.temp_data)

    def master_main(self):
        self.requirements_validation()
        self.ns = sdm_common.PyroDaemonThread.start_server(pyro_server_ip)
        self.start_migration_agent()
        assert self.check_system_name(), CSMessage  # Check that ESD is configured with the same system name
        self.check_product_version()  # Check that ESD is running the same Nexis version

        # Create workspace/user for validation that all data in safe
        logger.info("Create temporary '{}' workspace ..".format(UNIQUE_NAME))
        self.migration_agent_proxy.connect_flockadminapi(self.args.no_data_validation, self.args.esd_mc_password)
        self.temp_data = self.migration_agent_proxy.create_temp_data(UNIQUE_NAME)  # get temp name and type

        # Raise assertion error in case of temp data creation failed
        assert (self.temp_data and self.args.no_data_validation), WS_CREATION_ERR
        self.temp_data_storage = 'esd'  # Change temp data location
        if UNIQUE_NAME:
            logger.info("Temporary '{0}' {1} created.".format(*self.temp_data))
        logger.info('Management Console page will not be available until migration complete')
        self.migration_agent_proxy.stop_indexServer()  # Stop indexServer service on ESD, check filesystem files
        sdm_common.stop_indexServerd()  # Stop indexServer service on SDA
        logger.info('IndexServerd services stopped.')

        self.download_pdbin()
        self.check_pdhash()
        logger.info("Wait for ESD file system archiving..")
        self.migration_agent_proxy.compress_fs()
        logger.info("ESD archiving is complete")

        self.apply_filesystem_on_sda()
        self.temp_data_storage = 'sda'
        self.clean = True
        self.validate_sda_filesystem()  # All data safe validation
        self.apply_changes_on_esd()  # Setup ESD profile configuration, apply new profile
        self.cleanup()

    def cleanup(self):
        logger.info('Wait for cleanup ..')
        if self.temp_data_storage == 'esd':
            # Remove temporary data used for validation filesystem migration
            self.migration_agent_proxy.delete_temp_data(*self.temp_data)
        elif self.temp_data_storage == 'sda':
            sdm_common.connect_flockadminapi(self.args.no_data_validation, self.args.esd_mc_password)
            sdm_common.delete_temp_data(*self.temp_data)
        logger.info("Temporary {1} with name '{0}' deleted".format(*self.temp_data))
        if self.ns:
            self.ns.stop_ns()


if __name__ == '__main__':
    try:
        try:
            print(WELCOME_MSG)
            master = MigrationMaster()
            master.master_main()
            logger.info('Filesystem successfully migrated to {}. \nDone!'.format(pyro_server_ip))
        except NamingError as msg:
            logger.exception(msg)
            raise RuntimeError('Could not initialize migration service from the agent ip address.')
    except (AssertionError, RuntimeError) as msg:
        logger.critical(msg)
        logger.critical('System Director migration failed!')
        del logger
        sys.exit(1)
