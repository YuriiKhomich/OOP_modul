"""
Main game script. Runs the game for the user.
"""

import re

import game_exceptions
from game_exceptions import GameOver
from models import Player, Enemy
from settings import MAX_ENEMY_LEVELS, ENEMY_LEVEL_LIVES, ENEMY_LEVELS


def print_header(text):
    """Beauty is a terrible force!"""
    print(f"{'=' * 40}")
    print(f"{text:^40}")
    print(f"{'=' * 40}")


def print_status(player, enemy):
    """The current state of the Player. Number of lives and points."""
    print(
        f"{player.name} (lives: {player.lives}, score: {player.score})"
        f" vs. Enemy (level: {enemy.level}, lives: {enemy.lives})\n")


def get_user_input(prompt, allowed):
    """Validation of data entry"""
    while True:
        user_input = input(prompt)
        if user_input.lower() in allowed:
            return user_input.lower()
        print(f"Invalid input. Please choose from {', '.join(allowed)}")


def show_scores():
    """Viewing the table of results"""
    with open('scores.txt', 'r') as fil:
        scores = fil.readlines()
        for score in scores:
            print(score.strip())


def help_doc():
    """Read when things are bad."""
    with open('help.txt', 'r', encoding="utf-8") as fil:
        help_text = fil.read()
        print(help_text)


def enter_menu():
    """Main menu of the game"""
    while True:
        command = input("Enter a command (1 - start, 2 - show scores, 3 - help, 4 - exit): ")
        if command in {"start", "1"}:
            break
        if command in {"show scores", "2"}:
            show_scores()
        elif command in {"help", "3"}:
            help_doc()
        elif command in {"exit", "4"}:
            raise SystemExit
        else:
            print("Invalid command. Please try again")
    print_header("Welcome to the Battle!")


def validate_name(player_name):
    """The function validates the correctness of the input of the player's name"""
    player_name_entered = False
    while not player_name_entered:
        if re.search('^([a-zA-Zа-яА-Я]{3,20})$', player_name):
            player_name_entered = True
        else:
            print('The name can be 3-20 characters long. '
                  'Can consist of lowercase and uppercase letters and digits.\n')
            player_name = input("Please enter your name2:  ")
    return player_name


def play():
    """
    Main game function. Handles the user and the game process.
    """
    enter_menu()
    player_name = input("Please enter your name: ")
    player = Player(validate_name(player_name))
    enemy = Enemy(ENEMY_LEVELS)
    while True:
        try:
            print_status(player, enemy)
            player.attack(enemy)
            player.defense(enemy)
        except game_exceptions.EnemyDown as edn:
            if enemy.lives == 0:
                print(f"Congratulations! You defeated the enemy at level {enemy.level}!\n")
                player.score += 5
                print(f"Now, yours score: {player.score}\n")
                next_level = input("Press any key to continue (!Enemy level up!) or 'No' to Game Over: ")
                if next_level.lower() == 'no':
                    raise GameOver(player.score, player_name) from edn
                if enemy.level < MAX_ENEMY_LEVELS:
                    enemy = Enemy(enemy.level + 1)
                    enemy.lives = ENEMY_LEVEL_LIVES
                else:
                    raise GameOver(player.score, player_name) from edn


if __name__ == '__main__':
    try:
        play()
    except GameOver as e:
        print(f"Game over! Your final score is {e.score}.")
        e.save_score(e.name, e.score)
    except KeyboardInterrupt:
        pass
    finally:
        print("Hasta la vista, baby!")
