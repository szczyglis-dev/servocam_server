#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

import configparser
import os


class Configurator:
    def __init__(self, tracker=None):
        """
        Configs handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker

        # prepare cfg ids
        self.ids = ['config', 'hosts', 'streams']
        self.active = {}

        # prepare active
        for id in self.ids:
            self.active[id] = False

    def get_path(self, id):
        """
        Get path to file

        :param id: file id
        :return: path to file
        """
        if id == 'config':
            path = self.tracker.storage.get_user_config_path()
            if os.path.exists(path):
                return path
            else:
                return self.tracker.storage.get_default_config_path()
        elif id == 'hosts':
            path = self.tracker.storage.get_user_hosts_path()
            if os.path.exists(path):
                return path
            else:
                return self.tracker.storage.get_default_hosts_path()
        elif id == 'streams':
            path = self.tracker.storage.get_user_streams_path()
            if os.path.exists(path):
                return path
            else:
                return self.tracker.storage.get_default_streams_path()

    def update_path_label(self, id):
        """
        Update UI path label

        :param id: file id
        """
        self.tracker.window.path_label[id].setText(str(self.get_path(id)))

    def load(self, id):
        """
        Load file
        :param id: file id
        """
        # update path label
        self.update_path_label(id)

        # load file
        if id == 'config':
            path = self.tracker.storage.get_user_config_path()
            if not os.path.exists(path):
                path = self.tracker.storage.get_default_config_path()
            try:
                with open(path, 'r') as f:
                    txt = f.read()
                    f.close()
                    self.tracker.window.editor['config'].setPlainText(txt)
            except:
                self.tracker.debug.log('[ERROR] Error loading file: {}'.format(path))
        elif id == 'hosts':
            path = self.tracker.storage.get_user_hosts_path()
            if not os.path.exists(path):
                path = self.tracker.storage.get_default_hosts_path()
            try:
                with open(path, 'r') as f:
                    txt = f.read()
                    f.close()
                    self.tracker.window.editor['hosts'].setPlainText(txt)
            except:
                self.tracker.debug.log('[ERROR] Error loading file: {}'.format(path))
        elif id == 'streams':
            path = self.tracker.storage.get_user_streams_path()
            if not os.path.exists(path):
                path = self.tracker.storage.get_default_streams_path()
            try:
                with open(path, 'r') as f:
                    txt = f.read()
                    f.close()
                    self.tracker.window.editor['streams'].setPlainText(txt)
            except:
                self.tracker.debug.log('[ERROR] Error loading file: {}'.format(path))

    def load_defaults(self, id):
        """
        Load default file

        :param id: file id
        """
        if id == 'config':
            path = './assets/defaults/config.ini'
            try:
                with open(path, 'r') as f:
                    txt = f.read()
                    f.close()
                    self.tracker.window.editor['config'].setPlainText(txt)
                    self.tracker.debug.log('[OK] LOADED DEFAULT: {}'.format(path))
            except:
                self.tracker.debug.log('[ERROR] Error loading default file: {}'.format(path))
        elif id == 'hosts':
            path = './assets/defaults/hosts.txt'
            try:
                with open(path, 'r') as f:
                    txt = f.read()
                    f.close()
                    self.tracker.window.editor['hosts'].setPlainText(txt)
                    self.tracker.debug.log('[OK] LOADED DEFAULT: {}'.format(path))
            except:
                self.tracker.debug.log('[ERROR] Error loading default file: {}'.format(path))
        elif id == 'streams':
            path = './assets/defaults/streams.txt'
            try:
                with open(path, 'r') as f:
                    txt = f.read()
                    f.close()
                    self.tracker.window.editor['streams'].setPlainText(txt)
                    self.tracker.debug.log('[OK] LOADED DEFAULT: {}'.format(path))
            except:
                self.tracker.debug.log('[ERROR] Error loading default file: {}'.format(path))

        self.update_path_label(id)

    def save(self, id):
        """
        Save file

        :param id: file id
        """
        if id == 'config':
            data = self.tracker.window.editor['config'].toPlainText()
            path = self.tracker.storage.get_user_config_path()
            try:
                with open(path, 'w') as f:
                    f.write(data)
                    f.close()
                    self.tracker.debug.log('[OK] SAVED: {}'.format(path))
            except:
                self.tracker.debug.log('[ERROR] Error saving file: {}'.format(path))
        elif id == 'hosts':
            data = self.tracker.window.editor['hosts'].toPlainText()
            path = self.tracker.storage.get_user_hosts_path()
            try:
                with open(path, 'w') as f:
                    f.write(data)
                    f.close()
                    self.tracker.debug.log('[OK] SAVED: {}'.format(path))
            except:
                self.tracker.debug.log('[ERROR] Error saving file: {}'.format(path))
        elif id == 'streams':
            data = self.tracker.window.editor['streams'].toPlainText()
            path = self.tracker.storage.get_user_streams_path()
            try:
                with open(path, 'w') as f:
                    f.write(data)
                    f.close()
                    self.tracker.debug.log('[OK] SAVED: {}'.format(path))
            except:
                self.tracker.debug.log('[ERROR] Error saving file: {}'.format(path))

        self.update_path_label(id)

    def dump_config(self):
        """Dump config to file"""
        path = self.tracker.storage.get_user_config_path()
        config = configparser.ConfigParser()
        config.read(path)

        # update config
        self.tracker.storage.parse_cfg(config)

        with open(path, 'w') as configfile:  # save
            config.write(configfile)

    def dump_hosts(self):
        """Dump hosts to file"""
        data = []
        path = self.tracker.storage.get_user_hosts_path()
        for ip in self.tracker.remote.clients:
            client = self.tracker.remote.clients[ip]
            txt = ''
            if client.removed:
                txt += '# '
            txt += client.ip
            if client.hostname is not None and client.hostname != '':
                txt += ' ' + client.hostname
            if client.name is not None and client.name != '':
                txt += ' ' + client.name
            data.append(txt)

        with open(path, 'w') as file:
            for item in data:
                file.write(item + '\n')

    def dump_streams(self):
        """Dump streams to file"""
        data = []
        path = self.tracker.storage.get_user_streams_path()
        for unique_id in self.tracker.stream.streams.keys():
            txt = self.tracker.stream.parse_as_entry(self.tracker.stream.streams[unique_id])
            data.append(txt)

        with open(path, 'w') as file:
            for item in data:
                file.write(item + '\n')
