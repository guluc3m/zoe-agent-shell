# -*- coding: utf-8 -*-
#
# This file is part of Zoe Assistant
# Licensed under MIT license - see LICENSE file
#

from zoe import *
from colors import green, yellow
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

def i(i):
    return {
        'data': 'integer',
        'value': i
    }

def s(s):
    return {
        'data': 'string',
        'value': s
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
            print('You are running this agent non interactively, which is not the idea :)')
            print('If you are running it with docker-compose, try:')
            print('\n  docker-compose run zoe-agent-shell')
            sys.exit(1)
        self._thread = threading.Thread(target = self.cli, daemon = True)
        self._thread.start()

    @Intent('shell.show')
    def receive(self, msg):
        print(green(str(msg['payloads'])))

    def cli(self):
        print('Welcome to the Zoe shell!')
        print('You can send Zoe commands like', green("email(user('someone'), 'subject', 'body')"))
        print('This shell will translate those commands to the Zoe language and show the results when')
        print('they are available.')
        print(yellow('Please note that due to Kafka rebalancing, the first commands'))
        print(yellow('can take a few seconds to be dispatched.'))
        self.cmdloop()

    def emptyline(self):
        pass

    def default(self, line):
        try:
            result = eval(line)
            self.send(show(result))
        except:
            print('Error:', sys.exc_info())
