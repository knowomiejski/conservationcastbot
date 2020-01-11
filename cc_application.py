import sys
import os
import datetime
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import socket
import time
import json

from cc_chatbot import CCChatBot
from cc_docs_handler import CCDocsHandler


class Application:

    def set_new_channel(self, settingsfileData):
        new_channel = input('pls enter the channel name :)\n')
        settingsfileData['CHANNEL'] = new_channel

    def set_new_prefix(self, settingsfileData):
        new_prefix = input('pls enter the prefix :)\n')
        settingsfileData['BOT_PREFIX'] = new_prefix

    def set_new_folder(self, settingsfileData):
        new_folderID = input('pls enter the new folderID :)\n')
        settingsfileData['FOLDER_ID'] = new_folderID

    def set_new_reminder_timer(self, settingsfileData):
        new_reminder_timer = input('pls enter the new timer value in seconds :)\n')
        settingsfileData['BOT_REMINDER_TIMER'] = new_reminder_timer



    def setup_channel_name(self, settingsfileData):
        while True:
            print('\n-----------------------------------------------')
            print('\nCurrent loaded channel is:')
            print(settingsfileData['CHANNEL'])
            add_channel_input = input(
                'Would you like to update the twitch channel? (y/n)\n')
            if add_channel_input == 'y':
                self.set_new_channel(settingsfileData)
            elif add_channel_input == 'n':
                break

    def setup_prefix(self, settingsfileData):
        while True:
            print('\n-----------------------------------------------')
            print('\nCurrent loaded bot prefix is (in !q the ! is the prefix):')
            print(settingsfileData['BOT_PREFIX'])
            change_prefix_input = input(
                'Would you like to update bot prefix? (y/n)\n')
            if change_prefix_input == 'y':
                self.set_new_prefix(settingsfileData)
            elif change_prefix_input == 'n':
                break

    def setup_folderID(self, settingsfileData):
        print('\n-----------------------------------------------')
        print('\nThe folder id can be found in the url when you are in the folder.')
        print('for example:\n')
        print('in https://drive.google.com/drive/folders/1byWobqcHkOQMBELGSXK1WL3Gjrp-_J5_ the folderID is:')
        print('1byWobqcHkOQMBELGSXK1WL3Gjrp-_J5_\n')
        while True:
            print('The current Google Drive folder ID is:')
            print(settingsfileData['FOLDER_ID'])

            change_folder_input = input(
                'Would you like to change the folder? (y/n)\n')
            if change_folder_input == 'y':
                self.set_new_folder(settingsfileData)
            elif change_folder_input == 'n':
                break

    def setup_reminder_time(self, settingsfileData):
        while True:
            print('\n-----------------------------------------------')
            print('\nCurrent loaded reminder timer in seconds is:')
            print(settingsfileData['BOT_REMINDER_TIMER'])
            change_prefix_input = input(
                'Would you like to update the timer? (y/n)\n')
            if change_prefix_input == 'y':
                self.set_new_reminder_timer(settingsfileData)
            elif change_prefix_input == 'n':
                break



    def start_application_setup(self):
        print('Hi Cyto! :)')
        print('Im gonna ask you a few questions to start up')
        print('Please answer them by typing y for yes or n for no, and pressing enter')
        settingsfile = open('settings.json', 'r')
        settingsfileData = json.load(settingsfile)

        while True:
            setup_settings_input = input(
                "Would you like to edit the loaded settings? (y/n)\n")

            if setup_settings_input == 'y':
                self.setup_channel_name(settingsfileData)
                self.setup_prefix(settingsfileData)
                self.setup_reminder_time(settingsfileData)

            elif setup_settings_input == 'n':
                break
        self.setup_folderID(settingsfileData)
        print('\n-----------------------------------------------')
        print('Current settings file data:')
        print(settingsfileData)
        settingsfile = open('settings.json', 'w')
        new_settingsfile = json.dumps(settingsfileData, indent=4)
        settingsfile.write(new_settingsfile)
        settingsfile.close()

    def startup_bot(self):
        print('\n-----------------------------------------------')
        settingsfile = open('settings.json', 'r')
        print('Starting the Google Drive/Docs handler...')
        settingsfileData = json.load(settingsfile)
        docshandler = CCDocsHandler(settingsfileData['FOLDER_ID'])
        print('Initializing chatbot...')
        chatbot = CCChatBot(docshandler)
        print('Starting Chatbot...')
        chatbot.open_socket()
        chatbot.join_room()
        chatbot.start_watching()

    def run(self):
        self.start_application_setup()
        self.startup_bot()

    def print_meme(self):
        print('meme')


if __name__ == '__main__':
    application = Application()
    application.run()
