"""
Module for Player and Enemy classes.
Handles the fight logic, lives, levels and in-game score tracking.
"""

import random

import game_exceptions
from settings import PLAYER_LIVES, ENEMY_LEVEL_LIVES


class Player:
    """
    Contains the player property constructor, returns the attack/defense result,
     throws an end-of-game exception.
    """
    def __init__(self, name):
        self.name = name
        self.lives = PLAYER_LIVES
        self.score = 0
        self.allowed_attacks = {
            1: 'wizard',
            2: 'warrior',
            3: 'rogue'
        }

    @staticmethod
    def fight(attack, defense):
        """Method of determining the result of the fight"""
        winning_combinations = [(1, 2), (2, 3), (3, 1)]
        if attack == defense:
            return 0
        if (attack, defense) in winning_combinations:
            return 1
        return -1

    def decrease_lives(self):
        """method correcting the number of player's lives"""
        self.lives -= 1
        if self.lives == 0:
            raise game_exceptions.GameOver(self.score, self.name)

    def attack(self, enemy_obj):
        """Method for determining the player's attack"""
        while True:
            try:
                user_attack = int(input("Enter attack (1-wizard, 2-warrior, 3-rogue): "))
                if user_attack not in [1, 2, 3]:
                    print("Invalid input. Please enter 1, 2 or 3.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a number.")

        enemy_attack = enemy_obj.select_attack()
        result = self.fight(user_attack, enemy_attack)

        if result == 0:
            print("It's a draw!\n")
        elif result == 1:
            print("You attacked successfully!\n")
            enemy_obj.decrease_lives()
            self.score += 1
        else:
            print("You missed!\n")

    def defense(self, enemy_obj):
        """Method for determining the player's defense"""
        while True:
            try:
                user_defense = int(input("Enter defense (1-wizard, 2-warrior, 3-rogue): "))
                if user_defense not in [1, 2, 3]:
                    print("Invalid input. Please enter 1, 2 or 3.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a number.")

        enemy_attack = enemy_obj.select_attack()
        result = self.fight(enemy_attack, user_defense)

        if result == 0:
            print("It's a draw!\n")
        elif result == 1:
            print("You defended successfully!\n")
        else:
            print("You failed to defend!\n")
            self.decrease_lives()


class Enemy:
    """
    Selects attack level and reduces life after defeat
    """
    def __init__(self, level):
        self.level = level
        self.lives = ENEMY_LEVEL_LIVES

    @staticmethod
    def select_attack():
        """Select attack fo game"""
        return random.randint(1, 3)

    def decrease_lives(self):
        """Function that reduces the number of lives"""
        self.lives -= 1
        if self.lives == 0:
            raise game_exceptions.EnemyDown
