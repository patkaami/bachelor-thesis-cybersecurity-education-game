from programs.games import phishing_minigame_2
from programs.games import phishing_minigame_1 # importovanie minihier z kategorie phishing

def run():
    phishing_minigame_1.start() # spustenie prvej minihry
    phishing_minigame_2.start() # spustenie druhej minihry
    return True # funkcia vracia True ako znak, ze obe hry prebehli
