#!/usr/bin/env python3
# Andy Vu
# CPSC 386-04
# 2022-03-01
# avu53@csu.fullerton.edu
# @vuandy50
#
# Lab 04-00
#
# This program runs a game called Pig.
#

"""Below is my Player classes. Everything above is header."""
from random import randrange
import sys
import time

GOAL = 30

"""This is the Player class"""


class Player:
    """Player has a name and gender"""

    def __init__(self, name):
        """Initializes Player's name"""
        self._name = name

    def get_n(self):
        """Returns Playe's Name"""
        return self._name

    def get_gender(self):
        """Returns gender of player"""


class PigPlayer(Player):
    """Pig Player"""

    def __init__(self, name):
        """Initalizes PigPlayer"""
        super().__init__(name)
        self._order = 0
        self._score = 0

    def add_score(self, add):
        """Adds Score to current score"""
        self._score = self._score + add

    def check_t_score(self, add):
        """Checks if player has the goal points with addScore"""
        return self._score + add >= GOAL

    def check_score(self):
        """checks if player has the goal points"""
        return self._score >= GOAL

    def get_score(self):
        """Returns score"""
        return self._score

    def get_order(self):
        """Returns Order"""
        return self._order

    def set_order(self, order):
        """Sets order"""
        self._order = order


class ComputerPigPlayer(PigPlayer):
    """Computer Pig Player"""

    def __init__(self, game):
        """Initializes Computer Pig Player"""
        super().__init__("Master Pig")
        self._game = game
        self._score = 0
        self.turn_num = 0

    def check_opp_scores(self, cpu_score):
        """Checks opponents score"""
        for i in range(len(self._game.p_l)):
            if (self._score + cpu_score) < self._game.p_l[i].get_score():
                return True
        return False

    def check_cpu_score(self, cpu_score):
        """Checks if score is close to goal points"""
        flag = False
        if self._score < cpu_score:
            flag = True
        elif (self._score + cpu_score) - GOAL < 5:
            flag = True
        return flag

    def roll_tracker(self):
        """Keeps track of turns"""
        self.turn_num = self.turn_num + 1

    def reset_turn(self):
        """Sets turns back to 0"""
        self.turn_num = 0

    def check_roll_tracker(self):
        """Can only roll a max of 4 times in a row"""
        return self.turn_num < 4

    def roll_or_hold(self, cpu_score):
        """Decides whether to hold or roll"""
        choice = randrange(1, 3)
        if self.check_opp_scores(cpu_score) or self.check_cpu_score(cpu_score):
            if self.check_roll_tracker():
                choice = 1
            else:
                choice = 2
        else:
            choice = 2
        if choice == 1:
            self.roll_tracker()
        elif choice == 2:
            self.reset_turn()
        print("Choose an option:", end="")
        self.slowprint(" " + str(choice))
        return choice

    def choose_to_roll(self):
        """First turn as Roll"""
        choice = 1
        self.roll_tracker()
        print("Choose an option:", end="")
        self.slowprint(" " + str(choice))
        return choice

    @staticmethod
    def slowprint(string):
        """Slow prints CPU actions"""
        for cha in string + "\n":
            sys.stdout.write(cha)
            sys.stdout.flush()
            time.sleep(1.5)
