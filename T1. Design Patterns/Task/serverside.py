class Subject:
    clients = {}
    def register_client(self, ip, client):
        self.clients[ip]=client

    def unregister_client(self, ip):
        # some unregister actions for specific ip can be here
        return self.clients.pop(ip)

    def unregister_all(self):
        self.clients.clear()

    def reboot_client(self, ip):
        self.clients[ip].reboot(ip)

    def reboot_os(self, os_name):
        for ip, client in self.clients.items():
            if client.os_name == os_name:
                client.reboot(ip)

    def reboot_all(self):
        for ip, client in self.clients.items():
            client.reboot(ip)

    def drive_spaces(self, drive):
        for ip, client in self.clients.items():
            client.drive_space(ip, drive)