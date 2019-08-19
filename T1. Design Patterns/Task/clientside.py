import os
import paramiko
import logging
from abc import ABC, abstractmethod

class ABCClient(ABC):
    ip = ''
    mask = '255.255.255.0'
    gateway = '192.198.10.1'
    os_name = ''
    username = ''
    password = ''

    @abstractmethod
    def drive_space(self, ip, os_name, disk_name):
        pass

    @abstractmethod
    def reboot(self, ip, command):
        self.call(ip, self.username, self.password, command)

    @abstractmethod
    def register(self,ip, subject):
        subject.register_client(ip, self)

    def call(self, ip, user_name, password, command, strategy='ssh'):
        """Refactoring to state pattern can be here"""
        data = ''
        if strategy == 'ssh':
            print('SSH call with params: {};{};{};{}'.format(ip, user_name, password, command))
            data = self.ssh_call(ip, user_name, password, command)
        return data

    def ssh_call(self, ip, user_name, password, command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh.connect(ip, username=user_name, password=password)
        logging.info('SSH connection established successfully')
        # stdin, stdout, stderr = ssh.exec_command(command)
        # return stdin, stdout, stderr

class WinClient(ABCClient):
    os_name = "win"
    username = 'win_root'
    password = 'win_toor'

    def drive_space(self, ip, disk_name):
        print('Get Win client disk info')
        command = 'fsutil volume diskfree {}:'.format(disk_name)
        data = self.call(ip, self.username, self.password, command, strategy='ssh')
        return data

    def reboot(self, ip):
        print("Rebooting {}:{}".format(self.os_name, ip))
        reboot_cmd = 'win reboot cmd'
        super().reboot(ip, reboot_cmd)

    def register(self,ip, subject):
        print('Register {} client ip {} in {}'.format(self.os_name, ip, subject.name))
        super().register(ip, subject)

class LinuxClient(ABCClient):
    os_name = 'linux'
    username = 'root'
    password = 'toor'

    def drive_space(self, ip, disk_name):
        """ Connection method for Linux clients. Ex. ssh connection"""
        print('Get Linux client disk info')
        command = 'df -h {}'.format(disk_name)
        data = self.call(ip, self.username, self.password, command)
        return data

    def reboot(self, ip):
        print("Rebooting {}:{}".format(self.os_name, ip))
        reboot_cmd = 'linux reboot cmd'
        super().reboot(ip, reboot_cmd)

    def register(self,ip, subject):
        """Comment this method to see why we need abstract class )"""
        print('Register {} client ip {} in {}'.format(self.os_name, ip, subject.name))
        super().register(ip, subject)

class ClientFactory():
    os_family = {}

    def __new__(cls, *args, **kwargs):
        family_id = kwargs.get('os_name')
        if family_id == 'win':
            cls_obj = cls.os_family.setdefault(family_id, WinClient())
        elif family_id == 'linux':
            cls_obj = cls.os_family.setdefault(family_id, LinuxClient())
        return cls_obj
