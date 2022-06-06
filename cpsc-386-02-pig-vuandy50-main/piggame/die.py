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

"""Below this point is my Die class. Everything above is header."""
from random import randrange


class Die:
    """This function initializes class Die"""

    def __init__(self):
        pass

    def roll_two_dice(self):
        """This will be rolling 2 dice"""

    @staticmethod
    def roll():
        """This returns a number 1 - 6"""
        total = randrange(1, 7)
        return total
