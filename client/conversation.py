# -*- coding: utf-8-*-
import logging
from notifier import Notifier
from brain import Brain
import socket
import time


class Conversation(object):

    def __init__(self, persona, mic, profile):
        self._logger = logging.getLogger(__name__)
        self.persona = persona
        self.mic = mic
        self.profile = profile
        self.brain = Brain(mic, profile)
        self.notifier = Notifier(profile)

    def handleForever(self):
        """
        Delegates user input to the handling function when activated.
        """
        self._logger.info("Starting to handle conversation with keyword '%s'.",
                          self.persona)
        while True:
            # Print notifications until empty
            notifications = self.notifier.getAllNotifications()
            for notif in notifications:
                self._logger.info("Received notification: '%s'", str(notif))

            self._logger.debug("Started listening for keyword '%s'",
                               self.persona)
            threshold, transcribed = self.mic.passiveListen(self.persona)
            self._logger.debug("Stopped listening for keyword '%s'",
                               self.persona)

            if not transcribed or not threshold:
                self._logger.info("Nothing has been said or transcribed.")
                continue
            self._logger.info("Keyword '%s' has been said!", self.persona)
            
            
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                host = socket.gethostname()
                client.connect((host, 41384))
                client.send("go")
                data = s.recv(1024) 
                s.close() 
                print 'Received:', data
                client.shutdown(socket.SHUT_RDWR)
                client.close()
            except Exception as msg:
                print msg
            ##time.sleep(10) 

            ## self._logger.debug("Started to listen actively with threshold: %r",
            ##                   threshold)
            ##input = self.mic.activeListenToAllOptions(threshold)
            ##self._logger.debug("Stopped to listen actively with threshold: %r",
            ##                   threshold)

            ##if input:
            ##    self.brain.query(input)
            ##else:
            ##    self.mic.say("Pardon?")
