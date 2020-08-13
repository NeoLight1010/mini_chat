class Linker:
    def __init__(self):
        self.notification = ''
        self.arguments = ''
        self.connected = True
        print('Linker started.')

    def get_notif(self):
        if self.notification:
            temp = self.notification
            arguments = self.arguments
            return temp, arguments

    def reset_notif(self):
        self.notification = ''
        self.arguments = ''

    def send_notif(self, notif, arguments=''):
        self.notification = notif
        self.arguments = arguments

    def disconnect(self):
        self.connected = False

