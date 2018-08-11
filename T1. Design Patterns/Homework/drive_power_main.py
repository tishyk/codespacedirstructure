from chh_power_mgr import CHHPowerMgr
from cgemhdd_drive import CGEMHDDrive


def main():
    power_manager = CHHPowerMgr()
    drive = CGEMHDDrive('D1')

    power_manager.add_shh_client(drive)
    power_manager.request("on")

    drive2 = CGEMHDDrive("D2")
    power_manager.add_shh_client(drive2)
    power_manager.request('on')
    power_manager.request('off')
    power_manager.request('reset')
    power_manager.request('blink')

if __name__ == '__main__':
    main()
