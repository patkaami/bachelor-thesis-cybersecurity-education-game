import pygame
# inicializacia pygame, vytvorenie okna, nacitanie fontu
pygame.init()
screen = pygame.display.set_mode((1300, 750))
font = pygame.font.Font('res/font/final_fantasy_36_font.ttf', 45)
smaller_font = pygame.font.Font('res/font/final_fantasy_36_font.ttf', 30)

class Block: # trieda reprezentujuca blok s textom, ktory sa da tahat a oznacit ako spravny/nespravny
    def __init__(self, width, x, y, colour, text, correct):
        self.rect = pygame.Rect(x, y, width, 70)
        self.colour = colour
        self.text = text
        self.outline = 'black'
        self.drag = False
        self.locked = False # premenna pre zafixovanie bloku na spravne miesto
        self.org_x, self.org_y = x, y
        self.correct = correct

    def draw(self, screen): # vykreslenie bloku so zaoblenymi rohmi
        pygame.draw.rect(screen, self.colour, self.rect, border_radius=30)
        if self.locked: # ak je locked, outline sa zmeni na zelenu, co indikuje ze je spravne zaradeny
            pygame.draw.rect(screen, '#ADDFB1', self.rect, 5, border_radius=30)
        else:
            pygame.draw.rect(screen, self.outline, self.rect, 5, border_radius=30)
        
        lines = self.text.split('#') # rozdelenie na viac riadkov
        y = self.rect.top + 22 
        for line in lines:
            text_surface = smaller_font.render(line, True, 'black')
            text_rect = text_surface.get_rect(center=(self.rect.centerx, y))
            screen.blit(text_surface, text_rect)
            y += 20 

    def hover(self, mouse_x, mouse_y):  # ak blok nie je locked, zmeni farbu obrysu na bielu pri prechode mysou, inak je cierna
        if not self.locked:
            self.hovered = self.rect.collidepoint(mouse_x, mouse_y)
            if self.hovered:
                self.outline = 'white'
            else:
                self.outline = 'black'

    def start_drag(self): # ak nie je locked, moze sa tahat
        if not self.locked:
            self.drag = True

    def stop_drag(self): # konci tahanie
        self.drag = False

    def move(self, mouse_poz, new_x, new_y): # posuva blok podla mysi
        self.rect.x = mouse_poz[0] - new_x
        self.rect.y = mouse_poz[1] - new_y

    def is_inside(self, target_rect): # vracia true ak je cely blok vo vnutri zadaneho slotu 
        return target_rect.contains(self.rect)

def check_winning_condition(blocks, correct_stack, incorrect_stack): # kontroluje ci su vsetky bloky v spravnych stlpcoch
    all_correct = True
    for block in blocks:
        if block.correct and block not in correct_stack:
            all_correct = False
            break
    all_incorrect = True
    for block in blocks:
        if not block.correct and block not in incorrect_stack:
            all_incorrect = False
            break
    return all_correct and all_incorrect # vracia true ak su vsetky bloky spravne zoradene

def start(): # funkcia pre spustenie hry
    blocks = [
        Block(560, 30, 70, '#AF4D98', 'Ak správa obsahuje časové obmedzenie#(napr. do 12 hodín), môže ísť o phishing', True),
        Block(560, 30, 150, '#EE7674', 'Ihneď reaguj na podozrivý email a poskytni# osobné údaje', False),
        Block(560, 30, 230, '#91C7B1', 'Over si pravosť správy kontaktovaním#organizácie cez oficiálne stránky', True),
        Block(560, 700, 70, '#A9AFD1', 'Pri podozrivých správach si všímaš gramatické#preklepy a nesprávne domény stránok', True),
        Block(560, 700, 150, '#D0D6B5', 'Nikdy netreba kontrolovať emailovú#adresu odosielateľa', False),
        Block(560, 700, 230, '#987284', 'Phishingový útok môže prísť cez e-mail,# správy alebo aj cez sociálne siete', True)
    ] # vytvorenie vsetkych blokov

    running = True
    new_x, new_y = 0, 0
    tahany_block = None
    correct_stack = []
    incorrect_stack = []
    game_won = False
    space_pressed = False

    while running: # hlavny cyklus
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for block in blocks:
                    if block.rect.collidepoint(event.pos) and not block.locked: # ak sa kliklo na nejaky blok a nie je locked, zacne sa tahanie
                        block.start_drag()
                        tahany_block = block
                        new_x = event.pos[0] - block.rect.x
                        new_y = event.pos[1] - block.rect.y
                        break

            elif event.type == pygame.MOUSEBUTTONUP:
                if tahany_block:
                    if tahany_block.correct and tahany_block.is_inside(left_rect): # ak je tahany blok pravdivy a je ulozeny v lavom stlpci
                        tahany_block.rect.centerx = left_rect.centerx
                        new_y_pos = left_rect.top + 20 + len(correct_stack) * (tahany_block.rect.height + 10)   # zaradi sa na poziciu podla poctu už umiestnenych blokov
                        tahany_block.rect.y = new_y_pos
                        correct_stack.append(tahany_block) # prida sa do pravdivych 
                        tahany_block.locked = True # zafixuje/lockne sa, aby sa s nim nedalo uz hybat
                        tahany_block.stop_drag()

                    elif not tahany_block.correct and tahany_block.is_inside(right_rect): # ak je tahany blok nepravdivy a je ulozeny v pravom stlpci
                        tahany_block.rect.centerx = right_rect.centerx
                        new_y_pos = right_rect.top + 20 + len(incorrect_stack) * (tahany_block.rect.height + 10) # zaradi sa na poziciu podla poctu už umiestnenych blokov
                        tahany_block.rect.y = new_y_pos
                        incorrect_stack.append(tahany_block) # prida sa do nepravdivych
                        tahany_block.locked = True # zafixuje/lockne sa, aby sa s nim nedalo uz hybat
                        tahany_block.stop_drag()

                    else: # ak blok nie je spravne umiestneny (napr. pravdivy do praveho stlpca) vrati sa na svoju povodnu poziciu
                        tahany_block.rect.x = tahany_block.org_x
                        tahany_block.rect.y = tahany_block.org_y
                        tahany_block.stop_drag()

                    tahany_block = None

                game_won = check_winning_condition(blocks, correct_stack, incorrect_stack) # po kazdom pustenom bloku sa kontroluje ci su splnene podmienky vyhry
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and space_pressed: # ak je aktivovana moznost stlacenia medzernika (hra je prejdena), po jeho stlaceni sa program skonci
                return
            
        if tahany_block: # ak sa taha prave nejaky blok, aktualizuje sa podla mysi
            mouse_poz = pygame.mouse.get_pos()
            tahany_block.move(mouse_poz, new_x, new_y)

        mouse_poz = pygame.mouse.get_pos()

        screen.fill('#EBEBEB')
        left_rect = pygame.draw.rect(screen, '#000000', (10, 350, 630, 390), 7) # vykreslenie laveho stlpca
        right_rect = pygame.draw.rect(screen, '#000000', (660, 350, 630, 390), 7) # vykreslenie praveho stlpca

        # vykreslenie nadpisov nad stlpcami a zadania hore 
        txt1_surface = font.render('SPRÁVNE', True, 'black') 
        txt2_surface = font.render('NESPRÁVNE', True, 'black')
        zadanie_surface = font.render('ZORAĎ TVRDENIA NA SPRÁVNE A NESPRÁVNE', True, 'black')

        screen.blit(txt1_surface, (left_rect.centerx - 70, left_rect.top - 35))
        screen.blit(txt2_surface, (right_rect.centerx - 70, right_rect.top - 35))
        screen.blit(zadanie_surface, (310, 5))

        for block in blocks: # vykreslenie blokov, zistenie ci je nad nim mys
            block.hover(mouse_poz[0], mouse_poz[1])
            block.draw(screen)
        if game_won: # ak je hra prejdena, zobrazi sa end_img, nastavi sa moznost stlacit medzernik pre ukoncenie kategorie
            end_img = pygame.image.load('res/pictures/end.png')
            screen.blit(end_img, (350, 60))
            space_pressed = True

        pygame.display.flip()
