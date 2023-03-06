"""Module for implementing exceptions """


class GameOver(Exception):
    """Class for saving the final results of the game."""
    
    def __init__(self, score, name):
        self.name = name
        self.score = score
    
    @staticmethod
    def save_score(name, score):
        """Recording results in a table. Conclusion of the top 10 results."""
        with open("scores.txt", "r+") as fil:
            lines = fil.readlines()
            lines.append(f"{name} | {score}\n")
            lines.sort(key=lambda x: int(x.split("|")[1].strip()), reverse=True)
            lines = lines[:10]
            fil.seek(0)
            fil.writelines(lines)
            fil.truncate()


class EnemyDown(Exception):
    """Class without functionality."""
