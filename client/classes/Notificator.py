class Linker:
    """
    The Linker class links the frontend and backend. It allows sending and receiving information.
    """
    def __init__(self, gui=None):
        self.gui = gui  # GUI handler class
        self.notification = ''
        self.arguments = ''
        self.connected = True
        print('Linker started.')

    def set_gui(self, new_gui):
        self.gui = new_gui

    # v Notification related methods...
    def get_notif(self):
        if self.notification:
            temp = self.notification
            arguments = self.arguments
            return temp, arguments

    def reset_notif(self):
        self.notification = ''
        self.arguments = ''

    def send_notif(self, notif, arguments=''):
        # TODO: Make send_notif's be able to receive multiple arguments.
        self.notification = notif
        self.arguments = arguments

    def disconnect(self):
        self.connected = False

    # Execution methods
    def receive_and_exec(self, actions):
        received = self.get_notif()
        if received:
            notification = received[0]
            arguments = received[1]

            print("[LINKER]: " + notification)
            if notification in actions:
                if arguments:
                    actions[notification](arguments)
                else:
                    actions[notification]()
            self.reset_notif()

    def conn_success(self):
        print("Is there a gui here?")
        if self.gui:
            print("Switching to second frame")
            self.gui.switch_frame(1)
