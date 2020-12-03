from client.gui.login_window import LoginWindow
from client.gui.chat_window import ChatWindow
from tkinter import messagebox
from threading import Thread
import client.engine.client as client
from client.classes.Notificator import Linker
from client.classes.GuiHandler import GuiHandler
import sys


class InternalAlerts:
    def __init__(self, linker_actions=None):
        if linker_actions is None:
            linker_actions = {}
        self.linker_actions = linker_actions


def backend_thread(name):
    this_client = client.Client(linker_obj, user_name=name)
    this_server = client.Server()
    client.start(this_server, this_client)


def linker_thread_func(linker, actions):
    while True:
        linker.receive_and_exec(actions)


# linker actions v
# TODO: Move linker actions to Linker class.
def start_backend(user_name):
    backend = Thread(target=backend_thread, args=[user_name])
    backend.start()


def disconnect():
    sys.exit()


def conn_error():
    messagebox.showerror(message="Couldn't connect to server. Try again later.")


if __name__ == '__main__':
    ialerts = InternalAlerts()

    # Set up main linker.
    linker_obj = Linker()
    linker_act = {
        'START_BACKEND': start_backend,
        'DISCONNECT': disconnect,
        'CONNECT_ERROR': conn_error,
        'CONNECT_SUCCESS': linker_obj.conn_success
    }
    linker_thread = Thread(target=linker_thread_func, args=[linker_obj, linker_act])
    linker_thread.start()

    # Set up GuiHandler and link it to Linker.
    login_window = LoginWindow
    chat_window = ChatWindow
    windows = [login_window, chat_window]

    gui_handler = GuiHandler(linker_obj, windows)
    linker_obj.set_gui(gui_handler)
    gui_handler.switch_frame(1)  # For testing.
    gui_handler.start()
