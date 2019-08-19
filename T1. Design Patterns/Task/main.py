from clientside import ClientFactory
from serverside import Subject

subj = Subject()

for win_id in range(100):
    win_client = ClientFactory(os_name='win')
    win_ip = '10.151.8.{}'.format(win_id)
    subj.register_client(win_ip, win_client)

for linux_id in range(100, 200):
    linux_client = ClientFactory(os_name='linux')
    linux_ip = '10.151.10.{}'.format(linux_id)
    subj.register_client(linux_ip, linux_client)

subj.reboot_os('win')
subj.drive_spaces('c')
subj.unregister_client('10.151.8.0')
pass
