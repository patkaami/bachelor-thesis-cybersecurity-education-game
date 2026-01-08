import pygame
import re
from zxcvbn import zxcvbn

pygame.init() # inicializacia Pygame a nastavenie okna
screen = pygame.display.set_mode((1300, 750))
screen.fill('#EBEBEB')

class Hacker: # trieda hacker
    def __init__(self, img_path, animation_paths, x, y, new_width, new_height):
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (new_width, new_height))
        self.anim_images = []
        self.current_frame = 0
        self.smiling = False
        self.x = x
        self.y = y
        self.animation_delay = 5
        self.tick = 0
        self.win_timer = None

        for path in animation_paths: # nacitanie animacii hackera
            image = pygame.image.load(path)
            scaled_image = pygame.transform.scale(image, (new_width, new_height))
            self.anim_images.append(scaled_image)

    def update(self): # aktualizacia animacii
        if not self.smiling:
            self.tick += 1
            if self.tick >= self.animation_delay:
                self.current_frame = (self.current_frame + 1) % len(self.anim_images)
                self.tick = 0

    def draw(self, screen): # vykreslenie hackera
        if self.smiling:
            screen.blit(self.img, (self.x, self.y))
        else:
            screen.blit(self.anim_images[self.current_frame], (self.x, self.y))

def password_checker(event, password): # spracovanie vstupu a vyhodnotenie hesla
    display_crack_time = ''
    display_suggestions = ''
    
    if event.key == pygame.K_RETURN:  
        if password:
            library = zxcvbn(password) # analyza hesla pomocou zxcvbn
            crack_time = library['crack_times_display']['offline_fast_hashing_1e10_per_second']  # simuluje najagressivnejsi utok
            crack_time_slovak = translate_crack_time(crack_time) # preklad do slovenciny
            if 'feedback' in library and library['feedback']['suggestions']:
                suggestions = '\n'.join(library['feedback']['suggestions'])
                display_suggestions = translate_suggestions(suggestions) # preklad do slovenciny
            
            display_crack_time = f'Predpokladaný čas odhalenia:/{crack_time_slovak}'

    elif event.key == pygame.K_BACKSPACE: 
        password = password[:-1] # ak je stlaceny backspace, odstrani posledny znak
    else:
        password += event.unicode # inak prida novy znak
    return password, display_crack_time, display_suggestions

def translate_crack_time(crack_time): # preklad hodnoty crack_time do slovenciny, vyuzitie re kniznice pre lepsi preklad
    translations = {
        r'\binstant\b': 'okamžite',
        r'\bless than a second\b': 'menej ako sekunda',
        r'\bseconds\b': 'sekúnd',
        r'\bsecond\b': 'sekunda',
        r'\bminute\b': 'minúta',
        r'\bminutes\b': 'minút',
        r'\bhour\b': 'hodina',         
        r'\bhours\b': 'hodín',
        r'\bday\b': 'deň',
        r'\bdays\b': 'dní',
        r'\bmonth\b': 'mesiac',
        r'\bmonths\b': 'mesiacov',
        r'\byear\b': 'rok',
        r'\byears\b': 'rokov',
        r'\bcenturies\b': 'storočia'
    }
    
    for eng, slovak in translations.items():
        crack_time = re.sub(eng, slovak, crack_time)
    return crack_time

def translate_suggestions(suggestions): # preklad odporucani do slovenciny
    translations = {
        "Add another word or two. Uncommon words are better.": "Pridaj jedno alebo/viac slov, najlepšie/ak sú nezvyčajné.",
        "Avoid sequences.": "Skús nepoužívať/'abc' alebo '6543'/a podobne.",
        "Avoid years that are associated with you.": "Nepoužívaj roky,/ktoré sa spájajú s tebou.",
        "Avoid recent years.": "Nepoužívaj/nedávne roky.",
        "Avoid repeated words and characters.": "Neopakuj slová/a znaky.",
        "Avoid dates and years that are associated with you.": "Nepoužívaj dátumy,/ktoré sa/spájajú s tebou.",
        "Capitalization doesn't help very much.": "Použitie iba/veľkých písmen moc/nepomôže.",
        "Avoid common phrases and names.": "Skús použiť/neobvyklé frázy/a mená.",
        "All-uppercase is almost as easy to guess as all-lowercase.": "Skús kombinovať/malé a veľké/písmená.",
        "Reversed words aren't much harder to guess.": "Slová otočené/naopak sa tiež/lámu ľahko.",
        "Predictable substitutions like '@' instead of 'a' don't help very much.": "Náhrady ako/'@' za 'a' sa dajú/ľahko predvídať.",
        "Use a longer keyboard pattern with more turns.": "Nepíš heslá ako slovo/v jednom riadku/na klávesnici."
    }
    for eng, slovak in translations.items():
        suggestions = suggestions.replace(eng, slovak)
    return suggestions

def draw0(): # vykreslenie instrukcii
    pygame.draw.rect(screen, (200, 200, 200), input_box, border_radius=30)
    pygame.draw.rect(screen, 'black', input_box, 3, 30)
    instruction = font.render('VYTVOR ČO NAJSILNEJŠIE HESLO', True, 'black')
    screen.blit(instruction, (110, 300))

def draw1(password, crack_time, suggestions): # vykreslenie hesla, cracktimu a odporucani
    global input_box, space_pressed, running
    max_line_width = 560
    line_height = 40  
    padding = 20  
    max_height = 300  

    words = list(password)
    lines = []
    current_line = ""

    for word in words: # rozdelenia hesla na viac riadkov, ak je dlhe
        test_line = current_line + word
        test_width = font.size(test_line)[0]
        if test_width + padding > max_line_width:
            lines.append(current_line)
            current_line = word
        else:
            current_line = test_line
    if current_line:
        lines.append(current_line)

    new_height = max(len(lines) * line_height + padding, 80) # prisposobenie aj vysky vstupneho pola podla dlzky hesla
    if new_height <= max_height:
        input_box.height = new_height
    else:
        input_box.height = max_height

    for i, line in enumerate(lines): # vykreslenie zadaneho hesla
        if i * line_height + padding >= max_height:
            break  
        line_surface = font.render(line, True, 'black')
        line_width, line_height_actual = line_surface.get_size()
        line_x = input_box.x + (input_box.width - line_width) // 2
        line_y = input_box.y + 20 + (i * line_height)
        screen.blit(line_surface, (line_x, line_y))

    if crack_time: # vykreslenie cracktimu (cas prelomenia)
        crack_time_parts = crack_time.split('/', 1) # rozdelenie riadkov pomocou "/"
        time_value = crack_time_parts[1].strip()
        second_part_color = 'black'
        if 'storočia' in time_value: # nastavenie farby podla odhadu prelomenia
            value = 'storočia'
            second_part_color = '#478211' 
        elif time_value in ['menej ako sekunda', 'okamžite']:
            second_part_color = '#8F250C'
        
        else:
            match = re.match(r'(\d+)?\s*(sekunda|sekúnd|minúta|minút|hodina|hodín|deň|dní|mesiac|mesiacov|rok|rokov)', time_value) # pomocou kniznice re, regularneho vyrazu, zistujeme time value, aby sme spravne mohli priradit farbu
            if match:
                number = match.group(1)
                value = match.group(2)
                if value in ['sekunda', 'sekúnd', 'minúta', 'minút']:
                    second_part_color = '#8F250C'
                elif value in ['hodina', 'hodín']:
                    second_part_color = '#F88D41'
                elif value in ['deň', 'dní', 'mesiac', 'mesiacov']:
                    second_part_color = '#C6AE60'
                elif value in ['rok', 'rokov']:
                    second_part_color = '#B7DC95'

        first_part = font.render(crack_time_parts[0], True, 'black') # vykreslenie casu
        screen.blit(first_part, (100, 20))
        second_part = font.render(time_value, True, second_part_color)
        screen.blit(second_part, (55 + (first_part.get_width() - second_part.get_width()) // 2, 65))
        if 'storočia' in time_value: # ak je heslo dostatocne silne, animacia sa zmeni na smiling, hra prejdena
            hacker.smiling = True
        else:
            hacker.smiling = False

    if hacker.smiling:  # ak je heslo dostatocne silne
        if hacker.win_timer is None: 
            hacker.win_timer = pygame.time.get_ticks() # spustenie casovaca
        current_time = pygame.time.get_ticks()
        if current_time - hacker.win_timer < 2000:  # ak neuplynuli viac ako 2 sekundy, zobrazi sa vyherna sprava 
            screen.blit(text_bubble, (810, 40))
            smile_message = "Porazil si ma a tvoje/ heslo je dosť silné,/túto kategóriu máš/úspešne za sebou.".split('/')
            y = 80 
            for line in smile_message: # rozdelenie riadkov pomocou "/"
                message_surface = smaller_font.render(line, True, 'black')
                text_width, text_height = message_surface.get_size()
                x = (screen.get_width() - text_width) // 2 + 375
                screen.blit(message_surface, (x, y))
                y += text_height + 10
        else:
            end_category_image = pygame.transform.scale(pygame.image.load('res/pictures/end.png'), (700, 550))
            screen.blit(end_category_image, (80, 150)) # po 2 sekundach sa zobrazi obrazok, s popisom, ze hrac dokoncil kategoriu

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:  # ak sa stlaci medzernik, koniec hry
            running = False
    else:
        hacker.win_timer = None # reset casovaca, ak hrac este nevyhral

    if suggestions: # vykreslenie odporucani
            screen.blit(text_bubble, (810, 40))
            suggestion_lines = suggestions.split('\n') # rozdelenie odporucani na riadky
            suggestion_to_display = suggestion_lines[0]
            sub_lines = suggestion_to_display.split('/') # rozdelenie riadkov pomocou "/"
            if len(suggestion_lines) > 1: # ak mame viac ako 1 odporucanie, pridame dalsie ak je, musi mat do 60 znakov aby sa zmestilo do bubliny
                first_suggestion = suggestion_lines[0]
                second_suggestion = suggestion_lines[1]
                if len(second_suggestion) < 60: 
                    sub_lines.extend(second_suggestion.split('/')) # rozdelenie riadkov pomocou "/"
            for i, sub_line in enumerate(sub_lines): # vykreslenie
                suggestions_surface = smaller_font.render(sub_line, True, 'black')

                offset = i * 20  
                text_width, text_height = suggestions_surface.get_size()
                x = (screen.get_width() - text_width) // 2 + 370
                y = 80 + (30 * i)  
                screen.blit(suggestions_surface, (x, y))

    hacker.update()
    hacker.draw(screen)

def start(): 
    global password, display_crack_time, display_suggestions, hacker

    password = ''  
    display_crack_time = ''
    display_suggestions = ''
    hacker.smiling = False

    running = True
    while running: # hlavny cyklus
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 
            if event.type == pygame.KEYDOWN:
                if not hacker.smiling: # ak este hrac nevyhral, spracuj vstup/heslo
                    password, display_crack_time, display_suggestions = password_checker(event, password)
                elif event.key == pygame.K_SPACE and hacker.smiling: # ak hrac vyhral a stlacil medzernik, ukonci kategoriu
                    running = False 

        screen.fill('#EBEBEB') 
        draw0()
        draw1(password, display_crack_time, display_suggestions)

        hacker.update()
        hacker.draw(screen)

        pygame.display.flip() # aktualizacia obrazovky
        clock.tick(26) # obmedzenie FPS
    return

hacker = Hacker( 
    img_path='res/pictures/hacker/heker1.png', animation_paths=[f'res/pictures/hacker/heker{i}.png' for i in range(2, 8)],
    x=800, y=340, new_width=450, new_height=500) # inicializacia hackera

font = pygame.font.Font('res/font/final_fantasy_36_font.ttf', 48)
smaller_font = pygame.font.Font('res/font/final_fantasy_36_font.ttf', 40)
input_box = pygame.Rect(100, 380, 600, 150)
text_bubble = pygame.image.load('res/pictures/hacker/text_bubble.png')
password = ''
display_crack_time = ''
display_suggestions = ''
space_pressed = False

clock = pygame.time.Clock()
running = True
