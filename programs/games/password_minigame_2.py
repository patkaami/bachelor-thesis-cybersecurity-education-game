import pygame

def start(): # spustenie hry, inicializacia pygame
    pygame.init()
    screen = pygame.display.set_mode((1300, 750))
    font = pygame.font.Font('res/font/final_fantasy_36_font.ttf', 48)
    smaller_font = pygame.font.Font('res/font/final_fantasy_36_font.ttf', 35)

    class PasswordBlock: # trieda reprezentujuca blok s heslom, ktory sa da tahat
        def __init__(self, width, x, y, colour, text, strength):
            self.rect = pygame.Rect(x, y, width, 55)
            self.colour = colour
            self.text = text
            self.outline = 'black'
            self.drag = False
            self.strength = strength  # poradie spravneho umiestnenia
            self.org_x, self.org_y = x, y  # povodna pozicia bloku

        def draw(self, screen): # vykreslenie bloku a textu v nom
            pygame.draw.rect(screen, self.colour, self.rect, border_radius=30)
            pygame.draw.rect(screen, self.outline, self.rect, 5, border_radius=30)
            text_surface = smaller_font.render(self.text, True, 'black')
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

        def hover(self, mouse_x, mouse_y): # vizualny prvok, ak sa mysou prejde ponad blok, okraje sa prefarbia na bielo
            self.hovered = self.rect.collidepoint(mouse_x, mouse_y)
            if self.hovered:
                self.outline = 'white'
            else:
                self.outline = 'black'

        def start_drag(self): # aktivuje moznost tahania bloku 
            if not game_over:
                self.drag = True

        def stop_drag(self): # pustenie mysi
            self.drag = False

        def move(self, mouse_poz, new_x, new_y): # pohyb bloku podla mysi, ak nie je koniec hry
            if not game_over:
                self.rect.x = mouse_poz[0] - new_x
                self.rect.y = mouse_poz[1] - new_y

        def center(self, spot_rect): # vycentrovanie bloku do stredu cieloveho obdlznika (spot)
            self.rect.center = spot_rect.center

        def reset_position(self): # vracia blok na povodnu poziciu
            self.rect.x, self.rect.y = self.org_x, self.org_y

    blocks = [
        PasswordBlock(450, 820, 460, '#AF4D98', 'P3kn@#m0DR0#Fi4l0Va#r@KeT4?', 0),
        PasswordBlock(400, 820, 140, '#EE7674', 'aKoz3.B3zP3cn3.H3sLo', 1),
        PasswordBlock(400, 820, 620, '#91C7B1', 'Pomarancovy_dzus89', 2),
        PasswordBlock(250, 820, 220, '#C2E7DA', 'Siln3Heslo!', 3),
        PasswordBlock(230, 820, 300, '#D0D6B5', 'ferko12345', 4),
        PasswordBlock(180, 820, 380, '#987284', '12345678', 5),
        PasswordBlock(150, 820, 540, '#75B9BE', 'heslo', 6),
    ]

    spots = [pygame.Rect(180, 150 + i * 80, 600, 72) for i in range(7)]     # miesta na zoradenie hesiel
    running = True
    new_x, new_y = 0, 0
    hovered_block = None
    is_in = [None] * len(spots)
    game_over = False
    space_pressed = False

    while running: # hlavny cyklus
        all_placed = True  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for block in blocks:
                        if block.rect.collidepoint(event.pos): # ak kliknem na blok
                            block.start_drag()
                            hovered_block = block
                            new_x = event.pos[0] - block.rect.x
                            new_y = event.pos[1] - block.rect.y
                            break 

                elif event.type == pygame.MOUSEBUTTONUP:
                    if hovered_block:
                        placed_in_slot = False  # nie je umiestneny
                        for i, spot in enumerate(spots):
                            if spot.collidepoint(hovered_block.rect.center):
                                if is_in[i] is not None: # ak je tam iny, vrat ho naspat
                                    akt_block = is_in[i]
                                    akt_block.rect.x, akt_block.rect.y = akt_block.org_x, akt_block.org_y
                                if hovered_block in is_in: # ak uz niekde bol predtym, vymazeme ho
                                    is_in[is_in.index(hovered_block)] = None
                                hovered_block.center(spot) # vycentrovanie bloku
                                is_in[i] = hovered_block
                                placed_in_slot = True # umiestneny
                                break

                        if not placed_in_slot: # ak nebol placnuty(pustili sme mys mimo slotov), vrat na povodnu poziciu
                            hovered_block.reset_position()

                        hovered_block.stop_drag() # stop tahanie
                        hovered_block = None

            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and space_pressed: # ak sa hra skoncila a stlacil sa medzernik, koniec programu returne sa
                return

            if hovered_block: # tahanie bloku podla mysi
                mouse_poz = pygame.mouse.get_pos()
                hovered_block.move(mouse_poz, new_x, new_y)

        mouse_poz = pygame.mouse.get_pos()

        if not game_over:
            screen.fill('#EBEBEB')
            pygame.draw.rect(screen, '#000000', (80, 120, 720, 600), 8) # graficke prvky na obrazovke

            for i in range(7): # graficke prvky na obrazovke
                rect = pygame.draw.rect(screen, '#D3CACA', (180, 145 + i * 81, 600, 74), border_radius=10)
                number_text = font.render(str(i + 1), True, 'black')
                number_rect = number_text.get_rect(center=(140, rect.centery))
                screen.blit(number_text, number_rect)

            txt1 = font.render('POTIAHNI A ZORAĎ HESLÁ OD NAJSILNEJŠIEHO PO NAJSLABŠIE', True, 'black') # instrukcie na obrazovke
            txt2 = font.render('1 = NAJSILNEJŠIE, 7 = NAJSLABŠIE', True, 'black')
            screen.blit(txt1, (100, 20))
            screen.blit(txt2, (100, 70))

            correct = True # overenie spravnosti poradia a umiestnenia
            for i, block in enumerate(blocks):
                if not spots[i].contains(block.rect) or block.strength != i:
                    correct = False
                    all_placed = False 
                    break

            if correct and all_placed: # ak je vsetko spravne, aktivuje sa zobrazenie next obrazka
                game_over = True
                space_pressed = True

            for block in blocks: # vykreslenie blokov
                block.hover(mouse_poz[0], mouse_poz[1])
                block.draw(screen)

        if game_over: # zobrazenie next obrazka
            next_image = pygame.transform.scale(pygame.image.load('res/pictures/next.png'), (450, 400))
            screen.blit(next_image, (820, 180))

        pygame.display.flip() # aktualizacia okna
