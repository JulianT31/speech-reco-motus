#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Speech_reco.py
#  Speech_reco version 1.0
#  Created by Ingenuity i/o on 2023/10/27
#
# "no description"
#
import ingescape as igs


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SpeechReco(metaclass=Singleton):
    def __init__(self):
        # inputs

        # outputs
        self._wordO = None

    # outputs
    @property
    def wordO(self):
        return self._wordO

    @wordO.setter
    def wordO(self, value):
        self._wordO = value
        if self._wordO is not None:
            igs.output_set_string("word", self._wordO)


