import pygame

def start():  # spustenie hry, inicializacia pygame, definicia moznosti, fontu
    pygame.init()

    screen = pygame.display.set_mode((1300, 780))
    font = pygame.font.Font('res/font/final_fantasy_36_font.ttf', 36)
    bigger_font = pygame.font.Font('res/font/final_fantasy_36_font.ttf', 60)

    options = [
        {'text': 'Silné heslo obsahuje veľké, malé písmená, číslice a špeciálne znaky', 'rect': pygame.Rect(150, 170, 1000, 130), 'correct': True},
        {'text': 'Najlepšie heslo je ľahké na zapamätanie, napr. "12345" alebo "heslo"', 'rect': pygame.Rect(150, 260, 1000, 60), 'correct': False},
        {'text': 'Heslo by malo obsahovať osobné údaje, ako meno/dátum narodenia', 'rect': pygame.Rect(150, 350, 1000, 60), 'correct': False},
        {'text': 'Ideálna dĺžka hesla je 16 a viac znakov', 'rect': pygame.Rect(150, 440, 1000, 80), 'correct': True},
        {'text': 'Heslá by sa nemali opakovane používať na rôznych webových stránkach', 'rect': pygame.Rect(150, 530, 1000, 60), 'correct': True},
        {'text': 'Heslo stačí meniť len raz za 15 rokov', 'rect': pygame.Rect(150, 610, 1000, 60), 'correct': False}
    ]

    for option in options:
        text_surface = font.render(option['text'], True, '#000000')
        text_height = text_surface.get_height()
        option['rect'].height = text_height + 43

    marked_options = {}  
    correct_options = []  
    game_over = False  
    space_pressed = False  

    def draw_options():  # vykreslenie moznosti na obrazovke
        for i, option in enumerate(options):
            fill_color = '#D8D8C8'
            if i in marked_options:
                if marked_options[i]:
                    fill_color = '#ADDFB1'  
                    if i not in correct_options:
                        correct_options.append(i)
                else:
                    fill_color = '#E69B9B'  
                    marked_options.pop(i)  

            pygame.draw.rect(screen, fill_color, option['rect'], border_radius=15)
            pygame.draw.rect(screen, '#000000', option['rect'], width=6, border_radius=15)
            text_surface = font.render(option['text'], True, '#000000')
            text_rect = text_surface.get_rect(center=option['rect'].center)
            screen.blit(text_surface, text_rect)

    clock = pygame.time.Clock()
    running = True

    while running:  # hlavny cyklus
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over: 
                mouse_pos = event.pos
                for i, option in enumerate(options): 
                    if option['rect'].collidepoint(mouse_pos): # ak sa kliklo na obdlznik s moznostou
                        if option['correct']:
                            marked_options[i] = True
                        else:
                            marked_options[i] = False 
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and space_pressed: # ak je koniec hry a stlaceny space - hra konci 
                space_pressed = False 
                return

        if len(correct_options) == 3 and not game_over: # kontrola ci su oznacene vsetky spravne moznosti
            game_over = True
            space_pressed = True  

        if space_pressed:  # vykreslenie obrazku next-posun do dalsej hry
            try:
                next_image = pygame.image.load('res/pictures/next.png')
                screen.blit(next_image, (380, 150))  
                pygame.display.flip()
            except pygame.error:
                running = False

        if not space_pressed: # pociatocne vykreslenie obrazovky
            screen.fill('#EBEBEB')
            txt = bigger_font.render('OZNAČ SPRÁVNE TVRDENIA', True, 'black')
            screen.blit(txt, (400, 25)) 
            draw_options()
        if running:
            pygame.display.flip()

        clock.tick(5) # obmedzenie FPS, aby bolo vidno nespravne zakliknutu odpoved (zafarbi sa na cerveno vo funkcii draw_options())
