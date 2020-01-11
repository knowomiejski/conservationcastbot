import socket
import re
import json
import threading


class CCChatBot:

    def __init__(self, docHandler):
        self.docHandler = docHandler
        self.s = socket.socket()
        settingsfile = open('settings.json', 'r')
        self.settingsfileData = json.load(settingsfile)
        self.irc_token = self.settingsfileData['TMI_TOKEN'],
        self.client_id = self.settingsfileData['TWITCH_CLIENT_ID'],
        self.nick = self.settingsfileData['BOT_NICK'],
        self.prefix = self.settingsfileData['BOT_PREFIX'],
        self.channel = self.settingsfileData['CHANNEL']
        self.timer = float(self.settingsfileData['BOT_REMINDER_TIMER'])
        self.help_regex = re.compile(self.prefix[0] + 'help')
        self.question_regex = re.compile(self.prefix[0] + 'q ')


    def open_socket(self):
        self.s.connect(('irc.twitch.tv', 6667))
        self.s.send(bytes('PASS ' + self.irc_token[0] + '\r\n', 'UTF-8'))
        self.s.send(bytes('NICK ' + self.nick[0].lower() + '\r\n', 'UTF-8'))
        self.s.send(bytes('JOIN #' + self.channel + '\r\n', 'UTF-8'))

    def join_room(self):
        print('Joining room...')
        readbuffer = ''
        loading = True

        while loading:
            print('-------------------------------')
            readbuffer = readbuffer + self.s.recv(1024).decode('UTF-8')
            current_buffer = str.split(readbuffer, '\n')
            readbuffer = current_buffer.pop()

            for line in current_buffer:
                print(line)
                if "End of /NAMES list" in line:
                    loading = False
                    print('Joined room...')

        self.send_message('/me has landed 🦅')

    def send_message(self, message):
        message = 'PRIVMSG #' + self.channel + ' :' + message
        self.s.send(bytes(message + '\r\n', 'UTF-8'))

    def start_watching(self):
        readbuffer = ''
        print('-------------------------------')
        reminder_thread = threading.Thread(target=self.send_reminder)
        print('Starting reminder thread...')
        reminder_thread.start()
        print('\nReminder thread running...')
        watching = True

        while watching:
            # reminder_thread.start()
            print('-------------------------------')

            readbuffer = readbuffer + self.s.recv(1024).decode('UTF-8')
            current_buffer = str.split(readbuffer, '\n')
            readbuffer = current_buffer.pop()

            for line in current_buffer:
                if 'PING :tmi.twitch.tv' in line:
                    self.s.send(bytes(line.replace('PING', 'PONG') + '\r\n', 'UTF-8'))
                    # not sure why but only the second message fires when ponging
                    print('Send PONG to server...')
                else:
                    self.read_message(line)

    def read_message(self, line):
        split_message = line.split(':', 2)
        user = split_message[1].split('!')[0]
        message = split_message[2]
        print(user, message)
        if self.question_regex.match(message):
            self.write_question(user, message.strip(self.prefix[0] + 'q '))

        elif self.help_regex.match(message):
            self.display_help()

    def write_question(self, user, message):
        self.send_message(user + ', Thanks for asking the question! We\'ll look at it ASAP :)')
        print('Writing: ' + message)
        self.docHandler.writeToDoc(user + ': ' + message + '\n')

    def display_help(self):
        help_message = 'To ask a question type ' + self.prefix[0] + 'q <your question>'
        self.send_message(help_message)

    def send_reminder(self):
        # initial start
        print('(Reminder) Starting timer')
        self.display_help()
        timer_thread = threading.Timer(self.timer, self.display_help)
        while True:
            if not timer_thread.is_alive():
                print('(Reminder) Renewing timer...')
                timer_thread = threading.Timer(self.timer, self.display_help)
                print('(Reminder) Sending reminder...')
                timer_thread.start()
