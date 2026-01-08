from programs.games import sensitive_data_minigame_1 # importovanie minihier z kategorie osobne udaje
from programs.games import sensitive_data_minigame_2

def run():
    sensitive_data_minigame_1.start() # spustenie prvej minihry
    sensitive_data_minigame_2.start() # spustenie druhej minihry
    return True # funkcia vracia True ako znak, ze obe hry prebehli
