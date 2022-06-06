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

"""Below this point is the main code. Everything above is header."""

from piggame import game


def main_run():
    """This function will run the Pig Game"""
    start_game = game.PigGame()
    start_game.run()


if __name__ == "__main__":
    main_run()
