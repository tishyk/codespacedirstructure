#!/opt/python3/bin/python3

"""
#  storage/isis/disk_manager/system_drives/dm_missing_drive_hot_plug.py
#
#     dm_missing_drive_hot_plug - test to check meta drive state and detail message after pull off, pull in one meta drive.
#
"""
#from CExceptions import CSshExcn
#from core.lib.testwarelogger import testlog
#from storage.isis.disk_manager.CDMBaseTest import CDMBaseTest
import argparse

class BaseTest():
    """    This class is used, as parent class of all tests for DiskManager    """

    STATE_TIMEOUT = 600
    STATE_CHANGE_TIMEOUT = 120
    STATE_REBUILDING_TIMEOUT = 1800
    FLAG_STATE_TIMEOUT = 120
    SERVICE_LIST = []  # Services for obtaining dmcli -d -s output
    OLD_BRANDING_SCHEME_DRIVE = ["ST2000NM0034", "ST200FM0073",
                                 "ST2000NM0023",]  # "ST2000NM0023" moved to new branding scheme

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("system_name", help="System Director Name")
        self.parser.add_argument("media_pack", help="Media Pack Name")
        self.parser.add_argument("-s", "--slot", default="all", type=str, help="Drive slot for test")


    def setup(self):
        print("setup {}".format(self.parser.parse_args()))
        # super().setup()
        # self.stop_redundant_ha()
        # self.SERVICE_LIST.extend([self.ha_mgr.DISK_MANAGER_RESOURCE_NAME, self.ha_mgr.DISK_HELPER_DM_RESOURCE_NAME])
        # self.STATE_TIMEOUT = self.STATE_REBUILDING_TIMEOUT

    def run(self):
        self.results_obj = None
        print("run method")
        # for disk in self.metadata_disks[:1]:
        #     try:
        #         self.slot, self.disk = disk['slot'], disk
        #         detail_msg = self.DETAIL_MSG.format(self.disk['S/N'])
        #         testlog.info("Start test for '{}' device on host: {}!".format(disk['device'],
        #                                                                       self.storage_controller.host_ip))
        #
        #         testlog.info('Stop HA cluster!')
        #         self.storage_controller.ha_mgr.stop_ha_cluster()
        #         self.storage_controller.power_mgr.power_off(self.slot)
        #         testlog.info('Start HA cluster!')
        #         self.storage_controller.ha_mgr.start_ha_cluster(self.SERVICE_LIST)
        #
        #         self.wait_drive_by(self.slot, 'State', 'Empty', timeout=self.STATE_CHANGE_TIMEOUT)
        #         self.wait_drive_by(self.slot, 'Detail', "", timeout=60)
        #         self.wait_drive_by(self.slot, 'LED', 'OFF')
        #
        #         self.wait_drive_by(self.buddy_disk['slot'], 'State', 'Initializing', timeout=self.STATE_CHANGE_TIMEOUT)
        #         self.wait_drive_by(self.buddy_disk['slot'], 'Detail', detail_msg, timeout=60)
        #         self.wait_drive_by(self.buddy_disk['slot'], 'LED', 'OFF')
        #
        #         self.storage_controller.power_mgr.power_on(self.slot)
        #         self.wait_drive_by(self.slot, 'State', 'Operational', timeout=self.STATE_CHANGE_TIMEOUT)
        #         self.wait_drive_by(self.slot, 'Detail', "", timeout=60)
        #         self.wait_drive_by(self.slot, 'LED', 'OFF')
        #         self.wait_drive_by(self.buddy_disk['slot'], 'State', 'Operational', timeout=self.STATE_CHANGE_TIMEOUT)
        #         self.wait_drive_by(self.buddy_disk['slot'], 'Detail', "")
        #         self.wait_drive_by(self.buddy_disk['slot'], 'LED', 'OFF')
        #
        #         self._pass()
        #     except (RuntimeError, CSshExcn) as excn:
        #         testlog.error(excn)

        return self.results_obj

    def cleanup(self):
        print("Cleanup")
        # if not self.results_obj.get_success():
        #     self.storage_controller.power_mgr.power_on(self.slot)
        # super().cleanup()


if __name__ == '__main__':
    test = BaseTest()
    test.setup()
    test.run()






















































































































 # Hidden part :)
def decorator(cls):
    class Wrapper(object):
        def __init__(self, *args):
            self.wrapped = cls(*args)
            self.wrapped.parser = argparse.ArgumentParser()
            self.wrapped.parser.add_argument("Workspace", help="System Workspace Name")

        def __getattr__(self, name):
            print('Getting the {} of {}'.format(name, self.wrapped))
            return getattr(self.wrapped, name)

    return Wrapper

#@decorator