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

"""Below this point is my PigGame class. Everything above is header."""
from os import system, name
from .die import Die
from .player import ComputerPigPlayer, PigPlayer


def clear():
    """clears terminal"""
    # for windows
    if name == "nt":
        _ = system("cls")
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system("clear")


class PigGame:
    """This is my PigGame class"""

    def __init__(self):
        self.welcome_screen()
        self._die = Die()
        while True:
            try:
                self.n_o_p = int(input("How many player(1-4): "))
                if self.n_o_p > 4 or self.n_o_p < 1:
                    clear()
                    print("Your input is not valid. Please Try again...")
                else:
                    break
            except ValueError:
                clear()
                print("Your input is not valid. Please Try again...")

        self.p_l = []
        for i in range(self.n_o_p):
            new_name = input("Person {} --> Enter your name: ".format(i + 1))
            self.p_l.append(PigPlayer(new_name))
        if self.n_o_p == 1:
            self.p_l.append(ComputerPigPlayer(self))
        print()

    def run(self):
        """This run the Pig Game"""
        if self.n_o_p > 1:
            self.sort_list_of_players()
            self.pvp()
        else:
            self.cpu_v_p()

    def score_board(self):
        """Dislays Players Scores from most to least"""
        s_l = []
        p_c = []

        for i in range(len(self.p_l)):
            s_l.append(self.p_l[i].get_score())
            p_c.append([self.p_l[i], False])
        s_l.sort(reverse=True)

        print("****SCORE BOARD*****")
        print("--------------------")
        for i in range(len(self.p_l)):
            for j in range(len(self.p_l)):
                if not p_c[j][1] and p_c[j][0].get_score() == s_l[i]:
                    p_c[j][1] = True
                    print("{}){}".format(i + 1, p_c[j][0].get_n()), end="")
                    print(" ---> {}".format(s_l[i]))
        print()

    def print_error(self):
        """Prints out Error Message"""
        clear()
        self.score_board()
        print()
        print("Your input is not valid. Please Try again...")
        print("------------------------------------------")

    def check_winner_pvp(self, c_p, p_score):
        """Finds the winner of PvP"""
        winner_index = -1
        for i in range(len(self.p_l)):
            if self.p_l[i] == c_p and self.p_l[i].check_t_score(p_score):
                winner_index = i
                self.p_l[i].add_score(p_score)
        return winner_index

    @staticmethod
    def print_for_pvp(c_p, rotation, c_p_i):
        """Prints for Player versus Player"""
        print("Your turn Player {} --> {}!".format(c_p_i + 1, c_p.get_n()))
        print("SELECT YOUR MOVE:")
        print("1) Roll")
        if rotation != 0:
            print("2) Hold")

    def found_winner_pvp(self, winner_index):
        """Prints out the final scores once the winner is found"""
        input("WE HAVE A WINNER! Press Enter to see final scores...")
        clear()
        w_name = self.p_l[winner_index].get_n()
        w_score = self.p_l[winner_index].get_score()
        print("*******FINAL********")
        self.score_board()
        print("WINNER: {} with {} points!".format(w_name, w_score))

    def pvp(self):
        """Player versus Player"""
        c_p_i = 0
        p_score = 0
        rotation = 0
        winner_index = -1
        while True:
            try:
                c_p = self.p_l[c_p_i]
                self.print_for_pvp(c_p, rotation, c_p_i)
                move = int(input("Choose an option: "))
                clear()
                self.score_board()
                if move == 1:
                    roll = self._die.roll()
                    if roll == 1:
                        clear()
                        self.score_board()
                        print("Uh Oh! {} rolled a 1!".format(c_p.get_n()))
                        p_score = 0
                        c_p_i = (c_p_i + 1) % self.n_o_p
                        print("NEXT: {}".format(self.p_l[c_p_i].get_n()))
                        rotation = 0
                    else:
                        print("Rotation Number: {}".format(rotation + 1))
                        print("{} rolled {}".format(c_p.get_n(), roll))
                        p_score = p_score + roll
                        print("{} has {}".format(c_p.get_n(), p_score))
                        rotation = rotation + 1
                    print("------------------------------------------")
                elif move == 2 and rotation != 0:
                    clear()
                    c_p.add_score(p_score)
                    p_score = 0
                    c_p_i = (c_p_i + 1) % self.n_o_p
                    self.score_board()
                    print("{}, your turn!".format(self.p_l[c_p_i].get_n()))
                    print("------------------------------------------")
                    rotation = 0
                else:
                    self.print_error()
                winner_index = self.check_winner_pvp(c_p, p_score)
                if winner_index != -1:
                    break
            except ValueError:
                self.print_error()
        self.found_winner_pvp(winner_index)

    @staticmethod
    def print_cpuvp(c_p, rotation, c_p_i, p_score):
        """Prints for CPU versus Player"""
        move = 0
        if c_p_i == 0:
            print("Your turn Human Player --> {}! ".format(c_p.get_n()))
            print("SELECT YOUR MOVE:")
            print("1) Roll")
            if rotation != 0:
                print("2) Hold")
            move = int(input("Choose an option: "))
        else:
            print("Your turn Computer Player --> {}! ".format(c_p.get_n()))
            print("SELECT YOUR MOVE:")
            print("1) Roll")
            if rotation != 0:
                print("2) Hold")
            if rotation != 0:
                move = c_p.roll_or_hold(p_score)
            else:
                move = c_p.choose_to_roll()
        return move

    @staticmethod
    def after_roll(rotation, roll, p_score, c_p):
        """Prints out what happens after the roll and returns the score"""
        print("Roll number: {}".format(rotation + 1))
        print("{} rolled {}".format(c_p.get_n(), roll))
        p_score = p_score + roll
        print("{} has {}".format(c_p.get_n(), p_score))
        print("------------------------------------------")
        return p_score

    def cpu_v_p(self):
        """CPU versus Player"""
        c_p_i = 0
        c_p = self.p_l[c_p_i]
        p_score = 0
        rotation = 0
        self.score_board()
        while True:
            try:
                move = self.print_cpuvp(c_p, rotation, c_p_i, p_score)
                clear()
                self.score_board()
                if move == 1:
                    roll = self._die.roll()
                    if roll == 1:
                        print("Uh Oh! {} rolled a 1!".format(c_p.get_n()))
                        p_score = 0
                        c_p_i = (c_p_i + 1) % 2
                        c_p = self.p_l[c_p_i]
                        print("NEXT: {}".format(self.p_l[c_p_i].get_n()))
                        rotation = 0
                        if c_p_i == 1:
                            c_p.reset_turn()
                    else:
                        p_score = self.after_roll(rotation, roll, p_score, c_p)
                        rotation = rotation + 1
                elif move == 2 and rotation != 0:
                    clear()
                    c_p.add_score(p_score)
                    p_score = 0
                    c_p_i = (c_p_i + 1) % 2
                    c_p = self.p_l[c_p_i]
                    self.score_board()
                    print("{}, Your turn!".format(self.p_l[c_p_i].get_n()))
                    print("------------------------------------------")
                    rotation = 0
                else:
                    self.print_error()
                winner_index = self.check_winner_pvp(c_p, p_score)
                if winner_index != -1:
                    break
            except ValueError:
                self.print_error()
        self.found_winner_pvp(winner_index)

    def print_order_list(self, pair_l, roll_l):
        """Prints and Stores order of the Players"""
        p_order = []
        clear()
        print("****ORDER LIST*****")
        print("-------------------")
        for i in range(self.n_o_p):
            for j in range(self.n_o_p):
                if pair_l[j][1] == roll_l[i]:
                    pair_l[j][0].set_order(i + 1)
                    p_order.append(pair_l[j][0])
                    p_name = pair_l[j][0].get_n()
                    num = roll_l[i]
                    print("Player {}".format(i + 1), end="")
                    print("---> {} rolled {}".format(p_name, num))
        print()
        self.p_l = p_order

    def sort_list_of_players(self):
        """Sorts the players based on the number they rolled"""
        pair_l = []
        roll_l = []
        flag = [True, True, True, True, True, True]
        print("**Roll the dice to see who goes first!**")
        i = 0
        while i < len(self.p_l):
            try:
                print("Your turn --> {}! ".format(self.p_l[i].get_n()))
                input("When you are ready press Enter to roll...")
                roll = self._die.roll()
                print("You rolled --> {}! ".format(roll))
                print()
                if roll == 1 and flag[0]:
                    pair_l.append([self.p_l[i], roll])
                    roll_l.append(roll)
                    flag[0] = False
                    i = i + 1
                elif roll == 2 and flag[1]:
                    pair_l.append([self.p_l[i], roll])
                    roll_l.append(roll)
                    flag[1] = False
                    i = i + 1
                elif roll == 3 and flag[2]:
                    pair_l.append([self.p_l[i], roll])
                    roll_l.append(roll)
                    flag[2] = False
                    i = i + 1
                elif roll == 4 and flag[3]:
                    pair_l.append([self.p_l[i], roll])
                    roll_l.append(roll)
                    flag[3] = False
                    i = i + 1
                elif roll == 5 and flag[4]:
                    pair_l.append([self.p_l[i], roll])
                    roll_l.append(roll)
                    flag[4] = False
                    i = i + 1
                elif roll == 6 and flag[5]:
                    pair_l.append([self.p_l[i], roll])
                    roll_l.append(roll)
                    flag[5] = False
                    i = i + 1
                else:
                    print("Please Roll again!")
            except ValueError:
                clear()
                print("Your input is not valid. Please Try again...")
                print()
        roll_l.sort(reverse=True)
        self.print_order_list(pair_l, roll_l)

    @staticmethod
    def rules():
        """Prints out the rule for Pig"""
        print("   2) To start the game, a player can enter the number 1 ")
        print("      through 4 to establish how many players there are.")
        print("      If a player enters 1, then the other player is a")
        print("      computer AI.")
        print("   3) When the player enteres 2 or more players, then the")
        print("       computer AI is not used as a player.")
        print("   4) There is one six-sided die (simulated by the game using")
        print("      a psuedo-random number generator) the faces of the die")
        print("      are numbered 1, 2, 3, 4, 5, and 6.")
        print("   5) The game is turn based.")
        print("   6) All players have a name, including the computer AI.")
        print("   7) The player who goes first is selected by each player")
        print("      rolling the die once. The players are ordered in")
        print("      ascending order given the number they rolled. If")
        print("      there is a tie between two or more players, the ")
        print("      computer can break the tie by arbitrarily assigning that")
        print("      player to a position not less than theposition the")
        print("      player rolled.")
        print("   8) Once each player has had a turn in ascending order, the ")
        print("      turn returns to the first player. ")
        print("      (The process is a circular queue.)")
        print("   9) Each turn, a player rolls the die,")
        print("      * The current player rolls the die until their turn")
        print("        ends. All other playerswait their turn. A turn ")
        print("        ends when a player rolls a 1 or chooses to hold.")
        print("      * If the player rolls a 1, the player scores nothing")
        print("        thatturn and it becomes the next player's turn. The")
        print("        player's overall score does not change because ")
        print("        the player  has lost the points accrued during ")
        print("        their turn.")
        print("      * If the player rolls any other number, the value of the")
        print("        die is added to their turn's score as points and ")
        print("        the player's turn may continue. The player's overall ")
        print("        score does not change because the player has lost ")
        print("        the points accrued during their turn.")
        print("      * If a player chooses to hold, their turn score total ")
        print("        is added to their score and it becomes the next")
        print("        player's turn.")
        print("  10) The player may not choose to hold until after the ")
        print("      die has been rolled at least once.")
        print("  11) The game ends when a player ends their turn with a")
        print("      score of 30 points or greater.")
        print("  12) At the beginning of every die roll, the game displays")
        print("      the current player's total score, current turn score,")
        print("      and how many times the player has rolled. Once the ")
        print("      die is rolled, the computer displays the value of the")
        print("      die. If it is a 1, the computer ends the current ")
        print("      player's turn and moves on to the next player.")

    def welcome_screen(self):
        """Displays the rules of the game"""
        print("**************************WELCOME**************************")
        print("The game uses only one six sided die and is played with 2 ")
        print("or more players.")
        print("Players take turns rolling the die and tabulating a score")
        print("according to the rules.")
        print("  Rules:")
        print("   1) There is at least two players playing the game and at")
        print("      most four.")
        self.rules()
        print("The first player to score 30 or more points wins.")
        input("Press Enter to continue...")
        clear()
