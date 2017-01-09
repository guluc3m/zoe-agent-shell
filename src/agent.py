# -*- coding: utf-8 -*-
#
# This file is part of Zoe Assistant
# Licensed under MIT license - see LICENSE file
#

from zoe import *
from colors import green
import threading
import logging
import json
import cmd
import sys
import os

def show(what):
    return {
        'intent': 'shell.show',
        'payloads': [ what ]
    }

def user(name):
    return {
        'intent': 'user.get',
        'name': name
    }

def email(user, subject, text):
    return {
        'intent': 'mail.send',
        'recipient': user,
        'subject': subject,
        'body': text
    }

@Agent('Shell')
class ZoeShell(cmd.Cmd):
    prompt = ''

    def __init__(self):
        super().__init__()
        if not sys.stdout.isatty():
            print('Not in a TTY, exiting...')
            sys.exit(1)
        self._thread = threading.Thread(target = self.cli, daemon = True)
        self._thread.start()

    @Intent('shell.show')
    def receive(self, msg):
        print(green(str(msg['payloads'])))

    def cli(self):
        print('Welcome to the Zoe shell!')
        self.cmdloop()

    def emptyline(self):
        pass

    def default(self, line):
        try:
            result = eval(line)
            self.send(show(result))
        except:
            print('Error:', sys.exc_info())
