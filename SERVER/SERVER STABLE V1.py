import threading
import socket
import time
from tkinter import *
from tkinter import scrolledtext
import img_coder

HOST_IP = 'localhost'
HOST_PORT = 1234
SEPARATOR = '<SEPARATOR>'
BUFFER_SIZE = 1024
NUMS_OF_CLIENT = 1


class Server:
    def __init__(self, host, port):

        self.input_area = None
        self.send_button = None
        self.exit_button = None
        self.msg_label = None
        self.text_area = None
        self.chat_label = None
        self.win = None

        self.gui_thread = threading.Thread(target=self.gui_loop)
        self.gui_thread.start()

        self.host = host
        self.port = port
        self.client_info = None
        self.socket_client = None
        self.msg_count = 0

        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.bind((self.host, self.port))
        self.socket_server.listen(NUMS_OF_CLIENT)
        print('[*] Waiting for client to connect')
        self.socket_client, self.client_info = self.socket_server.accept()
        print('[+] Client (' + str(self.client_info[0]) + ') connected.')
        self.gui_done = False

        rec = threading.Thread(target=self.listening)
        rec.start()

        self.running = True

    def listening(self):
        while True:
            command = self.socket_client.recv(32).decode()
            if command == 'write':
                command = None
                self.socket_client.sendall(b'recv')
                img_coder.ClearDirectory()

                while True:
                    print('[cmd] Waiting for command...')

                    filename = '[empty]'
                    file_size = 0

                    if command is None:
                        command = self.socket_client.recv(32).decode()

                    if command:
                        print('[cmd] ' + command)

                    if command == 'send':
                        command = None
                        self.socket_client.sendall(b'send_ok')

                    if command == 'file_info':
                        command = None
                        file_info = self.socket_client.recv(1024).decode()
                        print(file_info)
                        if SEPARATOR not in file_info:
                            self.socket_client.sendall(b'file_info_error')
                            break
                        else:
                            filename, file_size = file_info.split(SEPARATOR)
                            file_size = int(file_size)
                        self.socket_client.sendall(b'file_info_ok')

                    if command == 'img':
                        command = None
                        print('[img] File name: ' + filename + ' | File size: ' + str(file_size) + '.')
                        file = open('recv/' + filename, 'wb')
                        received_msg = b''
                        while file_size > len(received_msg):
                            data = self.socket_client.recv(BUFFER_SIZE)

                            if b'send' in data:
                                print('kekW')
                                file.write(data)
                                command = 'send'
                                break

                            if not data:
                                break

                            received_msg += data
                            file.write(data)
                            print('[rcv] Received ' + str(len(received_msg)) + '/' + str(file_size) + '.')

                    if command == 'end':
                        command = None
                        break
                self.text_area.config(state='normal')
                self.text_area.insert(END, str(self.client_info[0]) + ': ' + img_coder.DecodeImages() + '\n')
                self.text_area.yview(END)
                self.text_area.config(state='disabled')

            if command == 'recv':
                print(self.msg_count)
                for i in range(0, self.msg_count + 1):
                    # ---------Send command---------
                    print('Connected...')
                    time.sleep(0.1)
                    self.socket_client.sendall('send'.encode())
                    print('sending...')

                    # ---------Read file------------
                    filename = str(i) + '_msg.jpg'
                    if i == self.msg_count:
                        filename = 'end.jpg'
                    # data = None
                    print(filename)

                    with open('4send/' + filename, 'rb') as f:
                        data = f.read()

                    # --------Beginning sending process--------------
                    while True:
                        cmd = self.socket_client.recv(32).decode()

                        if cmd:
                            print(cmd)

                        # ---------Receiving send_ok-----
                        if cmd == 'send_ok':
                            self.socket_client.sendall('file_info'.encode())
                            time.sleep(0.1)
                            temp = (str(filename) + '<SEPARATOR>' + str(len(data))).encode()
                            print(temp)
                            self.socket_client.sendall(temp)

                        # --------Receiving file_info_ok------
                        if cmd == 'file_info_ok':
                            self.socket_client.sendall('img'.encode())
                            time.sleep(0.1)
                            self.socket_client.sendall(data)
                            print('File transmission done.')
                            # time.sleep(0.5)
                            break

                self.msg_count = 0
                self.socket_client.sendall('end'.encode())

    def send(self):
        message = self.input_area.get(1.0, END)
        print('[msg] ' + self.host + ': ' + message)
        self.text_area.config(state='normal')
        self.text_area.insert(END, 'ME: ' + message)
        self.text_area.yview(END)
        self.text_area.config(state='disabled')
        self.input_area.delete(1.0, END)
        self.msg_count = img_coder.SelectionImages(message)
        self.socket_client.sendall(b'write')

    def send_th(self):
        send_thread = threading.Thread(target=self.send)
        send_thread.start()

    def exit(self):
        print('[*] Disconnecting...')
        try:
            self.socket_client.close()
            self.socket_server.close()
        finally:
            print('[-] Disconnected.')
        print('[-] Disconnected with errors.')

    def gui_loop(self):
        self.win = Tk()
        self.win.title("Server 1.3s")
        self.win.configure(bg="lightgray")

        self.chat_label = Label(self.win, text="Chat:", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.grid(row=0, column=0, columnspan=3)

        self.text_area = scrolledtext.ScrolledText(self.win)
        self.text_area.grid(row=1, column=0, columnspan=3, rowspan=5)
        self.text_area.config(state='disabled')

        self.msg_label = Label(self.win, text="Message:", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.grid(row=6, column=0, columnspan=3)

        self.input_area = Text(self.win, height=5)
        self.input_area.grid(row=7, column=0, columnspan=3)

        self.send_button = Button(self.win, text="Send", command=self.send_th)
        self.send_button.config(font=("Arial", 12))
        self.send_button.grid(row=8, column=1)

        self.exit_button = Button(self.win, text="Exit", command=self.exit)
        self.exit_button.config(font=("Arial", 12))
        self.exit_button.grid(row=8, column=2)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW")
        self.win.mainloop()


server = Server(HOST_IP, HOST_PORT)
