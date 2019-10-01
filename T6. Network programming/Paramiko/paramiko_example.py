import paramiko
import time
import os
import humanize
import select
from paramiko.ssh_exception import SSHException, BadHostKeyException, NoValidConnectionsError, AuthenticationException


class BaseSSH:
    DEFAULT_IO_SIZE = 1024
    DEFAULT_TIMEOUT = 60

    def __init__(self, ip, login, password):
        self.ip = ip
        self.login = login
        self.agent_password = password
        self.ssh = None

    def connect(self):
        if not self.ssh:
            try:
                self.ssh = paramiko.SSHClient()
                self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh.connect(self.ip, username=self.login, password=self.agent_password)

            except (SSHException, BadHostKeyException, NoValidConnectionsError) as msg:
                msg = 'Could not initialize ssh session.\
                 Check availability of IP address with submitted password\n{}'.format(msg)
                self.ssh = None
            except AuthenticationException as msg:
                msg = 'Check user name/password for host!\n{}'.format(msg)
                self.ssh = None
            except TimeoutError as msg:
                msg = 'Could not found entered host IP address. Timeout error!\n{}'.format(msg)
                self.ssh = None

    def call(self, *args, timeout=0):
        """
        # Works similar to subprocess.popen
        # Returns the return code attribute.
        """
        cmd = " ".join(args)
        exitcode, stdout, stderr = self.__execute(cmd, timeout)
        return exitcode

    def check_call(self, *args, timeout=0):
        """
        # Run command with arguments.  Wait for command to complete.  If
        # the exit code was zero then return, otherwise raise SSHException
        """
        cmd = " ".join(args)
        exitcode, stdout, stderr = self.__execute(cmd, timeout)
        if exitcode:
            raise SSHException(f"Command '{cmd}' failed on host {self.ip}",
                               exitcode, stderr + stdout)
        return 0

    def check_output(self, *args, timeout=0):
        """
        # Run command with arguments and return its output.
        # If the exit code was non-zero it raises a SSHException.
        # You can access the exitcode and stderr using this exception
        """
        cmd = " ".join(args)
        exitcode, stdout, stderr = self.__execute(cmd, timeout)
        if exitcode:
            raise SSHException(f"Command '{cmd}' failed on host {self.ip}",
                               exitcode,
                               stderr + stdout)
        return stdout

    def __execute(self, cmd, timeout):
        """
        # Issues a command to the device (via SSH)
        # RETURN: Exitcode and output(list or bytes) from command
        """
        assert isinstance(timeout, int) or isinstance(timeout, float), "Timeout must be integer or float value"

        stdout = ""
        stderr = ""
        exitcode = -1

        channel = None

        try:
            print("CMD: {}".format(cmd))

            if timeout > 0:
                transport = self.ssh.get_transport()
                channel = transport.open_session()
                # set non blocking mode for channel
                channel.setblocking(0)
                # execute remote command
                channel.exec_command(cmd)

                # wait for remote command output
                while True:
                    ready_to_read, ready_to_write, errors = select.select([channel], [], [channel], float(timeout))

                    if not ready_to_read and not ready_to_write and not errors:
                        # timeout occurs
                        stderr += "TESTWARE SSH CLIENT: CONNECTION TIMEOUT"
                        break

                    if ready_to_read:  # can read data
                        while channel.recv_ready():
                            current_output = channel.recv(self.DEFAULT_IO_SIZE).decode('utf-8')
                            stdout += current_output

                        while channel.recv_stderr_ready():
                            current_error = channel.recv_stderr(self.DEFAULT_IO_SIZE).decode('utf-8')
                            stderr += current_error

                    if ready_to_write:
                        # SSH CLIENT: ready to write. Interactive session is not supported
                        pass

                    if errors:  # error on socket occurs
                        stderr += "TESTWARE SSH CLIENT: SOCKET ERROR"
                        break

                    if channel.exit_status_ready():
                        # remote application execution has been finished
                        exitcode = channel.recv_exit_status()
                        break

            else:
                # No timeout specified
                stdin, stdout, stderr = self.ssh.exec_command(cmd)
                exitcode = stdout.channel.recv_exit_status()
                stdout = stdout.read().decode('utf-8')
                stderr = stderr.read().decode('utf-8')

        except SSHException as excn:
            stderr += "TESTWARE SSH CLIENT: ERROR OCCURS DURING EXECUTION REMOTE COMMAND"

        finally:
            if channel:
                channel.shutdown(2)

        return exitcode, stdout, stderr

    def send_package(self, src, dest):
        print('Send package "{}" to "{}".'.format(src, ssh.ip))
        t_begin = time.time()

        # TODO add connection error wrapper
        sftp = self.ssh.open_sftp()
        sftp.put(os.path.basename(src), dest)
        sftp.close()

        t_end = time.time()
        seconds_elapsed = int(t_end - t_begin)
        print('Sent, elapsed time {}.'.format(humanize.naturaldelta(seconds_elapsed)))

ssh = BaseSSH("192.168.1.108", "tishyk", "tishyk")
ssh.connect()
ssh.call("echo 'hello from ssh object' | systemd-cat")
output = ssh.check_output("ls -l /home/tishyk")
print(output)
ssh.send_package('paramiko_example.py', "/home/tishyk/paramiko_example.py")