import paramiko
import time
import os
import humanize
from paramiko.ssh_exception import SSHException, BadHostKeyException, NoValidConnectionsError, AuthenticationException

ip = ""
agent_password = ""


def ssh_connection():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username='root', password=agent_password)

    except (SSHException, BadHostKeyException, NoValidConnectionsError) as msg:
        msg = 'Could not initialize ssh session.\
         Check availability of IP address with submitted password\n{}'.format(msg)
    except AuthenticationException as msg:
        msg = 'Check user name/password for host!\n{}'.format(msg)
    except TimeoutError as msg:
        msg = 'Could not found entered host IP address. Timeout error!\n{}'.format(msg)
    else:
        return ssh
    raise RuntimeError(msg)


ssh = ssh_connection()
prepare_package = lambda package_path: 'path to some file'


def get_sftp():
    package_pathname = prepare_package()  # virtual func

    print('Send package "{}" to "{}".'.format(package_pathname, ip))
    t_begin = time.time()

    # TODO add connection error wrapper
    sftp = ssh.open_sftp()
    sftp.put(package_pathname, os.path.basename(package_pathname))
    sftp.close()

    t_end = time.time()
    seconds_elapsed = int(t_end - t_begin)
    print('Sent, elapsed time {}.'.format(humanize.naturaldelta(seconds_elapsed)))
