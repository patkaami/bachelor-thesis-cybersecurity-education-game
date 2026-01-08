import pygame

pygame.init()
screen = pygame.display.set_mode((1300, 750))
font = pygame.font.Font('res/font/final_fantasy_36_font.ttf', 38)
smaller_font = pygame.font.Font('res/font/final_fantasy_36_font.ttf', 30)

class Block: # trieda reprezentujuca jeden tahany blok
    def __init__(self, width, x, y, colour, text, correct):
        self.rect = pygame.Rect(x, y, width, 50)
        self.colour = colour
        self.text = text
        self.outline = 'black'
        self.drag = False
        self.locked = False
        self.org_x, self.org_y = x, y
        self.correct = correct

    def draw(self, screen): # vykreslenie bloku
        pygame.draw.rect(screen, self.colour, self.rect, border_radius=500)
        if self.locked: # ak je locked (uz spravne zaradeny), outline sa prefarbi na zeleno
            pygame.draw.rect(screen, '#ADDFB1', self.rect, 5, border_radius=500)
        else:
            pygame.draw.rect(screen, self.outline, self.rect, 5, border_radius=500)
        
        lines = self.text.split('#') # rozdelenie textu do viac riadkov
        y = self.rect.top + 22 
        for line in lines:
            text_surface = smaller_font.render(line, True, 'black')
            text_rect = text_surface.get_rect(center=(self.rect.centerx, y))
            screen.blit(text_surface, text_rect)
            y += 20 

    def hover(self, mouse_x, mouse_y): # ak nie je locked, zisti ci je and nim mys, ak ano outline sa zmeni na bielu
        if not self.locked:
            self.hovered = self.rect.collidepoint(mouse_x, mouse_y)
            if self.hovered:
                self.outline = 'white'
            else:
                self.outline = 'black'

    def start_drag(self): # spusti tahanie bloku
        if not self.locked:
            self.drag = True

    def stop_drag(self): # zastavenie tahania bloku
        self.drag = False

    def move(self, mouse_poz, new_x, new_y): # presunutie bolu podla polohy mysi
        self.rect.x = mouse_poz[0] - new_x
        self.rect.y = mouse_poz[1] - new_y

    def is_inside(self, target_rect): # kontrola, ci je blok vo vnutri slotu
        return target_rect.contains(self.rect) # vracia true

def check_winning_condition(blocks, correct_stack, incorrect_stack): # zistenie, ci hrac spravne rozdelil vsetky bloky
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
    return all_correct and all_incorrect # vracia true ak su vsetky bloky spravne rozdelene

def start(): # funkcia pre spustenie hry
    blocks = [
        Block(300, 500, 110, '#6683BD', 'Aktuálna poloha', False),
        Block(300, 500, 170, '#A02E32', 'Obľúbená farba', True),
        Block(300, 500, 650, '#E99989', 'Telefónne číslo', False),
        Block(300, 500, 230, '#91C7B1', 'Rodné číslo', False),
        Block(300, 500, 290, '#A9AFD1', 'Tvoju prezývku', True),
        Block(300, 500, 350, '#E4959E', 'Fotky tvojej tváre', False),
        Block(300, 500, 470, '#ADA0A6', 'Adresa trvalého bydliska', False),
        Block(300, 500, 530, '#A16DAC', 'Číslo OP', False),
        Block(300, 500, 590, '#E7CA6A', 'Meno tvojho psa', True),
        Block(300, 500, 410, '#1C856F', 'Číslo kreditnej karty', False)]

    running = True
    new_x, new_y = 0, 0
    tahany_block = None
    correct_stack = []
    incorrect_stack = []
    game_won = False
    space_pressed = False

    while running: # herny cyklus
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN: # zaciatok tahania bloku, ak nie je locked
                for block in blocks:
                    if block.rect.collidepoint(event.pos) and not block.locked:
                        block.start_drag()
                        tahany_block = block
                        new_x = event.pos[0] - block.rect.x
                        new_y = event.pos[1] - block.rect.y
                        break

            elif event.type == pygame.MOUSEBUTTONUP: # pustenie bloku
                if tahany_block:
                    if tahany_block.correct and tahany_block.is_inside(left_rect): # ak je tahany blok oznaceny ako correct a je ulozeny v lavom stlpci
                        tahany_block.rect.centerx = left_rect.centerx
                        new_y_pos = left_rect.top + 20 + len(correct_stack) * (tahany_block.rect.height + 10)  # zaradi sa na poziciu podla poctu už umiestnenych blokov
                        tahany_block.rect.y = new_y_pos
                        correct_stack.append(tahany_block) # prida sa do pravdivych 
                        tahany_block.locked = True # zafixuje/lockne sa, aby sa s nim nedalo uz hybat
                        tahany_block.stop_drag()

                    elif not tahany_block.correct and tahany_block.is_inside(right_rect): # ak je tahany blok oznaceny ako not correct a je ulozeny v pravom stlpci
                        tahany_block.rect.centerx = right_rect.centerx
                        new_y_pos = right_rect.top + 20 + len(incorrect_stack) * (tahany_block.rect.height + 10) #  zaradi sa na poziciu podla poctu už umiestnenych blokov
                        tahany_block.rect.y = new_y_pos
                        incorrect_stack.append(tahany_block) # prida sa do pravdivych 
                        tahany_block.locked = True # zafixuje/lockne sa, aby sa s nim nedalo uz hybat
                        tahany_block.stop_drag()

                    else:  # ak blok nie je spravne umiestneny (napr. blok correct do praveho stlpca) vrati sa na svoju povodnu poziciu
                        tahany_block.rect.x = tahany_block.org_x
                        tahany_block.rect.y = tahany_block.org_y
                        tahany_block.stop_drag()

                    tahany_block = None

                game_won = check_winning_condition(blocks, correct_stack, incorrect_stack) # po kazdom pustenom bloku sa kontroluje ci su splnene podmienky vyhry
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and space_pressed: # ak je aktivovana moznost stlacenia medzernika (hra je prejdena), po jeho stlaceni sa program skonci, hrac sa vrati naspat do menu
                return
             
        if tahany_block:  # ak sa taha prave nejaky blok, aktualizuje sa podla mysi
            mouse_poz = pygame.mouse.get_pos()
            tahany_block.move(mouse_poz, new_x, new_y)

        mouse_poz = pygame.mouse.get_pos()

        screen.fill('#EBEBEB')
        left_rect = pygame.draw.rect(screen, '#000000', (10, 100, 460, 620), 7) # vykreslenie laveho stlpca
        right_rect = pygame.draw.rect(screen, '#000000', (830, 100, 460, 620), 7) # vykreslenie praveho stlpca

        # vykreslenie nadpisov nad stlpcami a zadania hore 
        txt1_surface = font.render('ÁNO', True, 'black')
        txt2_surface = font.render('NIE', True, 'black')
        zadanie_surface = font.render('ROZHODNI, KTORÉ ÚDAJE JE BEZPEČNÉ ZDIEĽAŤ S CUDZÍMI OSOBAMI NA INTERNETE A KTORÉ NIE', True, 'black')

        screen.blit(txt1_surface, (left_rect.centerx - 30, left_rect.top - 35))
        screen.blit(txt2_surface, (right_rect.centerx - 30, right_rect.top - 35))
        screen.blit(zadanie_surface, (80, 5))

        for block in blocks:  # vykreslenie blokov, zistenie ci je nad nim mys
            block.hover(mouse_poz[0], mouse_poz[1])
            block.draw(screen)
        if game_won: # ak je hra prejdena, zobrazi sa end_img, nastavi sa moznost stlacit medzernik pre ukoncenie kategorie
            end_img = pygame.image.load('res/pictures/end.png')
            screen.blit(end_img, (350, 130))
            space_pressed = True

        pygame.display.flip()
