from programs.games import password_minigame_1
from programs.games import password_minigame_2
from programs.games import password_minigame_3 # importovanie minihier z kategorie hesla

def run():
    password_minigame_1.start() # spustenie prvej minihry
    password_minigame_2.start() # spustenie druhej minihry
    password_minigame_3.start() # spustenie tretej minihry
    return True # funkcia vracia True ako znak, ze obe hry prebehli
