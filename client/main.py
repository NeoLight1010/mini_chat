from client.gui.login_window import LoginWindow
from threading import Thread
import client.engine.client as client
from client.classes.Notificator import Linker


connected = False


class InternalAlerts:
    def __init__(self, linker_actions={}):
        self.linker_actions = linker_actions


def gui_thread(linker):
    login_window = LoginWindow(linker)
    login_window.start()


def backend_thread(linker, name):
    this_client = client.Client(linker=linker, user_name = name)
    this_server = client.Server()
    client.start(this_server, this_client)


def linker_thread_func(linker, actions):
    while connected:
        received = linker.get_notif()
        if received:
            notification = received[0]
            arguments = received[1]

            print("[LINKER]: " + notification)
            if notification in actions:
                if arguments:
                    actions[notification](arguments)
                else:
                    actions[notification]
            linker_obj.reset_notif()


def start_backend(user_name):
    backend = Thread(target=backend_thread, args=[linker_obj, user_name])
    backend.start()


def disconnect():
    connected = False


if __name__ == '__main__':
    connected = True
    linker_act = {
        'START_BACKEND': start_backend
    }

    ialerts = InternalAlerts()

    linker_obj = Linker()
    linker_thread = Thread(target=linker_thread_func, args=[linker_obj, linker_act])
    linker_thread.start()

    gui = Thread(target=gui_thread, args=[linker_obj])
    gui.start()
