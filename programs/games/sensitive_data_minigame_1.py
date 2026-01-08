import pygame

class Button: # trieda tlacidlo s textom, polohou, farbou a funkcnostou
    def __init__(self, text, x, y, width, height, color, font, correct = False):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.font = font
        self.original_color = color
        self.correct = correct

    def hovered(self, mouse_pos): # kontrola ci je kurzor nad tlacidlom
        return self.rect.collidepoint(mouse_pos)

    def draw(self, screen, mouse_pos): # vykreslenie tlacidla na obrazovku
        if self.hovered(mouse_pos):
            current_border_color = 'black'
        else:
            current_border_color = 'white'
        pygame.draw.rect(screen, current_border_color, self.rect, border_radius=30)
        rect = self.rect.inflate(-10, -10)
        pygame.draw.rect(screen, self.color, rect, border_radius=25)
        text_surface = self.font.render(self.text, True, 'white')
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def set_color(self, correct): # nastavi farbu podla zakliknutej odpovede
        if correct:
            self.color = '#759658'
        else:
            self.color = '#8A2A2A'

    def reset_color(self): # obnova povodnej farby
        self.color = self.original_color


def load_file(file_path): # nacitanie zadani z textoveho suboru
    questions = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('|')
            questions.append({
                'data': parts[0],
                'question': parts[1],
                'answer': parts[2],
                'explanation': parts[3],
                'correct_answers': parts[4].strip().split(', ')
            })
    return questions

def draw_footprints(screen, footprints): # vykreslenie stop noh
    for footprint in footprints:
        faded_image = footprint['image'].copy()
        faded_image.set_alpha(footprint['alpha'])
        screen.blit(faded_image, footprint['position'])

def render_multiline_text(text, font, screen, x, y, color): # upravenie textu, rozdelenie na riadky
    lines = text.split('#')
    total_height = len(lines) * font.get_linesize()
    y_offset = y - total_height // 2
    for i, line in enumerate(lines):
        rendered_line = font.render(line.strip(), True, color)
        line_rect = rendered_line.get_rect(center=(screen.get_width() // 2, y_offset + i * font.get_linesize()))
        screen.blit(rendered_line, line_rect)

def start_game(): # funkcia pre spustenie hry
    pygame.init()
    screen = pygame.display.set_mode((1300, 750))
    small_font = pygame.font.Font('res/font/final_fantasy_36_font.ttf', 27)
    font = pygame.font.Font('res/font/final_fantasy_36_font.ttf', 35)
    large_font = pygame.font.Font('res/font/final_fantasy_36_font.ttf', 52)

    buttons = [
        Button('ÁNO', 300, 600, 300, 100, '#C1B5BE', large_font),
        Button('NIE', 700, 600, 300, 100, '#C1B5BE', large_font)
    ] # tlacidla ANO, NIE
    
    potential_risks_buttons = [
        Button('Zneužitie identity', 290, 400, 320, 80, '#A3A4A4', font),
        Button('Finančná strata', 290, 500, 320, 80, '#A3A4A4', font),
        Button('Spamové správy', 290, 600, 320, 80, '#A3A4A4', font),
        Button('Sledovanie polohy', 690, 400, 320, 80, '#A3A4A4', font),
        Button('Prístup k súkromným súborom', 690, 500, 320, 80, '#A3A4A4', small_font),
        Button('Krádež účtu', 690, 600, 320, 80, '#A3A4A4', font)
    ] # tlacidla MOZNE RIZIKA
    next_button = Button('ĎALŠIA OTÁZKA', 500, 310, 280, 50, '#574B60', font) # tlacidlo DALSIA OTAZKA

    questions = load_file('res/data/digital_footprint_questions.txt')
    question_index = 0
    show_explanation = False
    explanation_text = ''
    show_next_image = False
    next_image_timer = None
    show_risks = False
    show_primary_buttons = True
    correct_clicked = 0

    image = pygame.image.load('res/pictures/private_data/footprint.png')
    scaled_image = pygame.transform.scale(image, (60, 100))
    rotated_image = pygame.transform.rotate(scaled_image, 270)
    mirrored_image = pygame.transform.flip(rotated_image, False, True)
    footprints = []

    x, y = 50, 50
    alpha = 30
    for i in range(len(questions)): # vygenerovanie footprintov, vizualny prvok na znazornenie odstranenia digitalnej stopy
        if i % 2 == 0:
            image = rotated_image
            y = 10
        else:
            image = mirrored_image
            y = 90
        footprints.append({
            'image': image,
            'position': (x, y),
            'alpha': alpha
        })
        alpha += 25
        alpha = max(0, alpha)
        x += 135

    running = True
    delay_timer = None  
    delayed_action = None  
    show_message = False

    while running: # herny cyklus
        screen.fill('#EBEBEB')
        mouse_pos = pygame.mouse.get_pos()
        draw_footprints(screen, footprints)

        if show_message: # ak hrac spravne prejde situaciu, ukaze sa mu vyherna sprava
            render_multiline_text('SPRÁVNE! ZMENŠIL SI SVOJU DIGITÁLNU STOPU!', font, screen, screen.get_width() // 2, 190, '#759658')
        if show_next_image: # ak prejde vsetky situacie, zobrazi sa next image
            next_image = pygame.image.load('res/pictures/next2.png')
            screen.blit(next_image, (380, 200))

        elif show_explanation: # zobrazenie vysvetlenia pre danu situaciu po odpovedi
            explanation_rect = pygame.Rect(250, 190, 780, 110)
            pygame.draw.rect(screen, '#D3D3D3', explanation_rect, border_radius=20)  
            pygame.draw.rect(screen, 'black', explanation_rect, width=5, border_radius=20)
            render_multiline_text(explanation_text, font, screen, screen.get_width() // 2, 260, 'black')
            if question_index < len(questions) - 1: # ak otazka nie je posledna, vykresli sa tlacidlo DALSIA OTAZKA
                next_button.draw(screen, mouse_pos)
            if show_risks_in_explanation: # vykreslenie tlacidiel MOZNE RIZIKA
                for button in potential_risks_buttons:
                    button.draw(screen, mouse_pos)
            else:
                if question_index == len(questions) - 1 and not next_image_timer: # ak to je posledna otazka, spusti sa timer 
                    next_image_timer = pygame.time.get_ticks() + 5000


        else:
            render_multiline_text(questions[question_index]['data'], font, screen, screen.get_width() // 2, 260, 'black') # zobrazenie situacie
            if show_risks: # ak sa maju zobrazovat rizika, zobraz zadanie
                render_multiline_text('VYBER VŠETKY MOŽNÉ RIZIKÁ,#KTORÉ MÔŽU NASTAŤ PRI TEJTO SITUÁCII:', font, screen, screen.get_width() // 2, 380, 'black')
            else:
                render_multiline_text(questions[question_index]['question'], font, screen, screen.get_width() // 2, 340, 'black') # inak zobraz otazku
            if show_primary_buttons: # ak sa maju zobrazovat ANO/NIE tlacidla, vykresli ich
                show_message = False
                for button in buttons:
                    button.draw(screen, mouse_pos)

            if show_risks: # ak sa maju zobrazovat rizika, vykreslia sa
                for button in potential_risks_buttons:
                    button.draw(screen, mouse_pos)

        if delay_timer and pygame.time.get_ticks() > delay_timer:
            delay_timer = None
            if delayed_action == "show_risks": # ak sa ma zobrazit faza vyberu moznych rizik (stlacilo sa tlacidlo ANO)
                show_risks = True # zobrazia sa rizika
                show_primary_buttons = False # skryju sa ANO/NIE tlacidla
                show_message = True # zobrazi sa vyherna sprava 
            elif delayed_action == "show_explanation": # ak sa ma zobrazit vysvetlenie (stlacilo sa tlacidlo NIE)
                show_explanation = True # zobrazi sa vysvetlenie
                show_primary_buttons = False # skryju sa ANO/NIE tlacidla
                show_risks_in_explanation = False # neukazuju sa rizika vo vysvetlovani
                show_message = True  # zobrazi sa vyherna sprava 
            delayed_action = None # reset stavu

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if show_primary_buttons: # ak su ANO/NIE tlacidla
                    for button in buttons:
                        if button.hovered(mouse_pos):
                            if button.text in questions[question_index]['answer']: # ak spravne zaklikol ANO/NIE tlacidlo
                                button.set_color(True) # spravna odpoved - zafarbenie na zeleno
                                delay_timer = pygame.time.get_ticks() + 300  
                                if footprints:
                                    footprints.pop() # odstrani sa jedna digitalna stopa
                                if button.text == 'ÁNO':
                                    delayed_action = "show_risks" # pokracuj na vyber rizik
                                elif button.text == 'NIE':
                                    explanation_text = questions[question_index]['explanation']
                                    delayed_action = "show_explanation" # pokracuj na vysvetlenie
                            else:
                                button.set_color(False) # nespravna odpoved - zafarbenie na cerveno

                elif show_risks: # oznacenie spravnych rizik
                    for i, risk_button in enumerate(potential_risks_buttons):
                        if risk_button.hovered(mouse_pos):
                            if str(i) in questions[question_index]['correct_answers']:
                                risk_button.set_color(True) # spravna odpoved - zafarbenie na zeleno
                                correct_clicked += 1
                            else:
                                risk_button.set_color(False) # nespravna odpoved - zafarbenie na cerveno

                    if correct_clicked == len(questions[question_index]['correct_answers']): # ak sa oznacili vsetky spravne rizika
                        show_explanation = True # ukaze sa vysvetlenie
                        explanation_text = questions[question_index]['explanation']
                        correct_clicked = 0  # reset kliknutych
                        show_risks_in_explanation = True # ukazu sa rizika aj vo vysvetleni
                        show_risks = False

                if show_explanation:
                    if next_button.hovered(mouse_pos) and question_index < len(questions) - 1: # ak sa stlaci next button, a nie je to posledna otazka
                        show_explanation = False # skryt vysvetlenie
                        question_index += 1 # pocitadlo otazok
                        show_primary_buttons = True # ukaz ANO/NIE tlacidla
                        # skry rizika
                        show_risks = False 
                        show_risks_in_explanation = False  
                        # reset farieb vsetkych tlacidiel
                        for button in buttons: 
                            button.reset_color()
                        for risk_button in potential_risks_buttons:
                            risk_button.reset_color()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and show_next_image: # ak su prejdene vsetky situacie a stlaceny space, program sa skonci
                return 
        if next_image_timer and pygame.time.get_ticks() > next_image_timer:
            show_next_image = True
            next_image_timer = None

        pygame.display.flip()

def start(): 
    pygame.init()
    screen = pygame.display.set_mode((1300, 750))
    runnig = True
    while runnig:
        screen.fill('#EBEBEB')
        start_image = pygame.transform.scale(pygame.image.load('res/pictures/private_data/private_data_text.png'), (800, 600))
        screen.blit(start_image, (260, 70))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_game()
                return
        pygame.display.flip()
