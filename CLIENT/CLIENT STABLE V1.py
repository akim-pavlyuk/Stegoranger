import socket
from tkinter import *
import tkinter.scrolledtext as scrolledtext
import threading
import time
import img_coder

HOST = 'localhost'  # my ip
PORT = 1234
SEPARATOR = '<SEPARATOR>'
BUFFER_SIZE = 1024


class Client:
    def __init__(self, host, port):

        self.send_button = None
        self.input_area = None
        self.msg_label = None
        self.text_area = None
        self.chat_label = None
        self.win = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        self.gui_done = False
        self.running = True
        self.msg_count = 0

        self.gui_thread = threading.Thread(target=self.gui_loop)
        self.receive_thread = threading.Thread(target=self.listening)

        self.gui_thread.start()
        self.receive_thread.start()

    def gui_loop(self):
        self.win = Tk()
        self.win.title('Client 1.3s')
        self.win.configure(bg="lightgray")

        self.chat_label = Label(self.win, text="Chat:", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_label = Label(self.win, text="Message:", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = Text(self.win, height=5)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = Button(self.win, text="Send", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()

    def write(self):
        message = self.input_area.get(1.0, END)
        print('[msg] ME: ' + message)
        self.text_area.config(state='normal')
        self.text_area.insert(END, 'ME: ' + message)
        self.text_area.yview(END)
        self.text_area.config(state='disabled')
        self.input_area.delete(1.0, END)
        self.msg_count = img_coder.SelectionImages(message)
        self.sock.sendall(b'write')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def listening(self):
        while True:
            command = self.sock.recv(32).decode()
            if command == 'write':
                command = None
                self.sock.sendall(b'recv')
                img_coder.ClearDirectory()

                filename = '[empty]'
                file_size = 0
                while True:
                    print('[cmd] Waiting for command...')

                    if command is None:
                        command = self.sock.recv(32).decode()

                    if command:
                        print('[cmd] ' + command)

                    if command == 'recv':
                        break

                    if command == 'send':
                        command = None
                        self.sock.sendall(b'send_ok')

                    if command == 'file_info':
                        command = None
                        file_info = self.sock.recv(1024).decode()
                        print(file_info)
                        if SEPARATOR not in file_info:
                            self.sock.sendall(b'file_info_error')
                            break
                        else:
                            filename, file_size = file_info.split(SEPARATOR)
                            file_size = int(file_size)
                        self.sock.sendall(b'file_info_ok')

                    if command == 'img':
                        command = None
                        print('[img] File name: ' + filename + ' | File size: ' + str(file_size) + '.')
                        file = open('recv/' + filename, 'wb')
                        received_msg = b''
                        while file_size > len(received_msg):
                            data = self.sock.recv(BUFFER_SIZE)

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
                self.text_area.insert(END, HOST + ': ' + img_coder.DecodeImages() + '\n')
                self.text_area.yview(END)
                self.text_area.config(state='disabled')

            if command == 'recv':
                print(self.msg_count)
                for i in range(0, self.msg_count + 1):
                    # ---------Send command---------
                    print('Connected...')
                    time.sleep(0.1)
                    self.sock.sendall('send'.encode())
                    print('sending...')

                    # ---------Read file------------
                    filename = str(i) + '_msg.jpg'
                    if i == self.msg_count:
                        filename = 'end.jpg'
                    print(filename)

                    with open('4send/' + filename, 'rb') as f:
                        data = f.read()

                    # --------Beginning sending process--------------
                    while True:
                        cmd = self.sock.recv(32).decode()

                        if cmd:
                            print(cmd)

                        # ---------Receiving send_ok-----
                        if cmd == 'send_ok':
                            self.sock.sendall('file_info'.encode())
                            temp = (str(filename) + '<SEPARATOR>' + str(len(data))).encode()
                            print(temp)
                            self.sock.sendall(temp)

                        # --------Receiving file_info_ok------
                        if cmd == 'file_info_ok':
                            self.sock.sendall('img'.encode())
                            time.sleep(0.1)
                            self.sock.sendall(data)
                            print('File transmission done.')
                            break

                self.msg_count = 0
                self.sock.sendall('end'.encode())


client = Client(HOST, PORT)
