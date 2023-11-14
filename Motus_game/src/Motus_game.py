#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Motus_game.py
#  Motus_game version 1.0
#  Created by Ingenuity i/o on 2023/10/20
#
# "no description"
#
# import ingescape as igs
import ingescape as igs
import random

from Color import Color


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MotusGame(metaclass=Singleton):
    def __init__(self):
        # inputs
        self.wordI = None
        self.nb_try = 0
        self.nb_try_max = 4
        self.word_to_discover = ""
        # if you want to exec the wining test uncomment this line
        # self.word_database = ["fleur"]
        # if you want to exec the wining test comment this line
        self.word_database = ["fleur", "table", "soleil", "plage", "bonjour", "chien", "chaton", "orange","forêt"]


        self.init_game()

    def init_game(self):
        self.word_to_discover = random.choice(self.word_database)
        self.wordI = self.word_to_discover[0] + "_" * (len(self.word_to_discover) - 1)
        self.nb_try = 0

    def get_color_by_letter(self, letter, letter_index):
        if letter == self.word_to_discover[letter_index]:
            return Color.RED.value
        elif letter in self.word_to_discover:
            return Color.YELLOW.value
        else:
            return Color.BACKGROUND.value

    def is_win(self):
        return self.wordI == self.word_to_discover

    def is_lose(self):
        return self.nb_try == self.nb_try_max

    def incr_nb_try(self):
        self.nb_try += 1

    def reset_game(self):
        self.init_game()
