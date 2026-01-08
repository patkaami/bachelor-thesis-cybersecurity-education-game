import pygame
from programs.animations import Fish, Bubble, TextPhishing # import animacii

def load_data(file_path): # nacitanie phishingovych dat z textoveho suboru
    phishing_messages = []
    with open(file_path, encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('|')
            clickable_parts = parts[-1].split(', ') if len(parts) > 4 else []
            phishing_messages.append({
                'sender': parts[0],
                'text': parts[1],
                'link': parts[2] if len(parts) > 2 else '',
                'image': parts[3] if len(parts) > 3 else '',
                'clickable_parts': clickable_parts
            })
    return phishing_messages 

def start(): # hlavna funkcia na spustenie hry, inicializacia premennych, zoznamov, objektov
    pygame.init()
    screen = pygame.display.set_mode((1300, 750))
    font = pygame.font.Font('res/font/final_fantasy_36_font.ttf', 26)
    large_font = pygame.font.Font('res/font/final_fantasy_36_font.ttf', 30)
    smaller_font = pygame.font.Font('res/font/final_fantasy_36_font.ttf', 23)
    phishing_examples = load_data('res/data/phishing_messages.txt')

    fishes = [
        Fish([f'res/pictures/phishing/fish1/{i:02}.png' for i in range(3)], x=100, y=150, move_speed=2, frame_delay=10, resize=True, resize_width=200, resize_height=150),
        Fish([f'res/pictures/phishing/fish2/{i:02}.png' for i in range(3)], x=200, y=250, move_speed=-2, frame_delay=12, resize=False),
        Fish([f'res/pictures/phishing/fish3/{i:02}.png' for i in range(3)], x=350, y=400, move_speed=4, frame_delay=12, resize=False),
        Fish([f'res/pictures/phishing/fish4/{i:02}.png' for i in range(3)], x=500, y=550, move_speed=-2, frame_delay=15, resize=False),
    ] 

    bubbles = [Bubble(screen.get_width(), screen.get_height(), 12, 'res/pictures/phishing/bubble.png')] 
    clock = pygame.time.Clock()
    running = True
    clicked_fish = None
    message_image = None
    message_image_rect = None
    current_example = None
    words_rects = [] 
    can_change_color = []
    remove_timer = 0
    timer_started = False
    caught = 0
    caught_fish_positions = []  
    lock = False  
    space_pressed = False
    first_image_path = 'res/pictures/phishing/phishing_text_1.png' # uvodny text pred samotnou hrou
    arrow_image_path = 'res/pictures/arrow.png'
    third_image_path = 'res/pictures/phishing/phishing_text_2.png'
    text_phishing = TextPhishing(first_image_path, arrow_image_path, third_image_path, 250, 80, screen)

    text_phishing.run(screen)
    while running: # hlavny cyklus
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if lock:
                    continue
                if event.button == 1: # kliknutie laveho tlacidla
                    mouse_pos = event.pos
                    fish_clicked = False

                    if current_example is None:  # ak ziadna sprava nie je zobrazena
                        for i, fish in enumerate(fishes):
                            if fish.rect.collidepoint(mouse_pos):
                                fish_clicked = True
                                if clicked_fish != i: # ak klikneme na inu rybu ako predtym, resetnem premenne, ulozim index
                                    clicked_fish = i
                                    current_example = None
                                    message_image = None
                                    message_image_rect = None
                                    can_change_color.clear()
                                    data = phishing_examples[clicked_fish]
                                    current_example = {
                                        'sender': data['sender'],
                                        'text': data['text'],
                                        'link': data['link'],
                                        'image': data['image'],
                                        'clickable_parts': data['clickable_parts']} # phishingovy pripad
                                    message_image = pygame.image.load(f'res/pictures/phishing/{data["image"]}') # nacitanie obrazku spravy
                                    message_image_rect = message_image.get_rect(center=(screen.get_width() // 2, 350))
                                    remove_timer = 0
                                    hint = large_font.render(f'Počet podozrivých elementov: {len(data["clickable_parts"])}', True, 'black') # vykreslenie hintu na obrazovke
                                    timer_started = False
                    if not fish_clicked and (message_image_rect is None or not message_image_rect.collidepoint(mouse_pos)): # ak kliknem mimo ryby a mimo spravy, zrusi sa vyber phishingoveho prikladu
                        clicked_fish = None  
                        current_example = None
                        message_image = None
                        message_image_rect = None
                    for rect, word in words_rects: 
                        if rect.collidepoint(mouse_pos): # kontrola, ci sa kliklo na nejake slovo v sprave
                            if word in current_example['clickable_parts'] and word not in can_change_color: # ak je slovo oznacitelne a este nebolo oznacene
                                can_change_color.append(word) # pridame ho do tych ktorym vieme zmenit farbu (ktore sa daju oznacit)
                                remaining_elements = len(current_example['clickable_parts']) - len(can_change_color) # vytvorime novy hint s aktualizovanym poctom podozrivych elementov (slov)
                                hint = large_font.render(f'Počet podozrivých elementov: {remaining_elements}', True, 'black')
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and space_pressed: # po chyteni vsetkych ryb, stlacenie medzernika ukonci hru
                return                  

        screen.fill('#B0D0D3') # vykreslenie pozadia
        for bubble in bubbles: # amimacia bublin
            bubble.update()
            bubble.draw(screen)

        for fish in fishes: # animacia ryb
            fish.update(screen.get_width())
            fish.draw(screen)

        words_rects.clear()

        if current_example: # ak je kliknuta ryba (zobrazi sa phishingovy priklad)
            if message_image:
                screen.blit(message_image, message_image_rect) # vykresli sa pozadie spravy
                x, y = message_image.get_width() - 30, 40
                if current_example['image'] == 'microsoft_email.png':
                    x -= 250
                    y = 20
                if current_example['image'] == 'instagram_message.png':
                    y -= 35
                    x += 130
                screen.blit(hint, (x, y))
            # spracovanie roznych typov phishingovych sprav, ktore su interaktivne, centrovanie slov a podobne
            if current_example['image'] == 'message.png':
                color = '#3A964B' if current_example['sender'] in can_change_color else 'black'
                sender_text = large_font.render(current_example['sender'], True, color)
                sender_rect = sender_text.get_rect(topleft=(screen.get_width() // 2 - sender_text.get_width() // 2, 190))
                screen.blit(sender_text, sender_rect.topleft)
                words_rects.append((sender_rect, current_example['sender']))

                lines = current_example['text'].split(', ')
                y = 280
                for line in lines:
                    x_offset = 450
                    words = line.strip().split()
                    for word in words:
                        color = '#3A964B' if word in can_change_color else 'black'
                        word_surface = font.render(word, True, color)
                        word_rect = word_surface.get_rect(topleft=(x_offset, y))
                        screen.blit(word_surface, word_rect.topleft)
                        words_rects.append((word_rect, word))
                        x_offset += word_rect.width + 10
                    y += 30

                if current_example['link']:
                    color = '#3A964B' if current_example['link'] in can_change_color else 'black'
                    link_surface = font.render(current_example['link'], True, color)
                    link_rect = link_surface.get_rect(topleft=(450, y))
                    screen.blit(link_surface, link_rect.topleft)
                    words_rects.append((link_rect, current_example['link']))
            
            if current_example['image'] == 'microsoft_email.png':
                color = '#3A964B' if current_example['sender'] in can_change_color else '#959595'
                sender_text = large_font.render(current_example['sender'], True, color)
                sender_rect = sender_text.get_rect(topleft=(380, 100))
                screen.blit(sender_text, sender_rect.topleft)
                words_rects.append((sender_rect, current_example['sender']))
                lines = current_example['text'].split('#')  
                y = 290
                words_before_empty_line = {'zákazník,', 'heslo.', 'pozdravom,', 'podpory.', 'dôvodov.'}
                for line in lines:
                    if line.strip():
                        x_offset = 310
                        words = line.strip().split()
                        for word in words:
                            color = '#3A964B' if word in can_change_color else 'black'
                            word_surface = smaller_font.render(word, True, color)
                            word_rect = word_surface.get_rect(topleft=(x_offset, y))
                            screen.blit(word_surface, word_rect.topleft)
                            words_rects.append((word_rect, word))
                            x_offset += word_rect.width + 10
                            if word in words_before_empty_line:
                                y += 20
                            elif word == 'hesla:':
                                y += 40
                        y += 20 

                if current_example['link']:
                    color = '#3A964B' if current_example['link'] in can_change_color else '#44A9DC'
                    link_surface = smaller_font.render(current_example['link'], True, color)
                    link_rect = link_surface.get_rect(topleft=(310, 440))
                    screen.blit(link_surface, link_rect.topleft)
                    words_rects.append((link_rect, current_example['link']))

            if current_example['image'] == 'instagram_message.png':
                color = '#3A964B' if current_example['sender'] in can_change_color else 'black'
                sender_text = smaller_font.render(current_example['sender'], True, color)
                sender_rect = sender_text.get_rect(topleft=(530, 165))
                screen.blit(sender_text, sender_rect.topleft)
                words_rects.append((sender_rect, current_example['sender']))
                lines = current_example['text'].split('#')  
                y = 260
                words_before_empty_line = {'Ahoj,', '4hodín:'}
                for line in lines:
                    if line.strip():
                        x_offset = 500
                        words = line.strip().split()
                        for word in words:
                            if word in can_change_color:
                                color = '#3A964B' 
                            else:
                                color = 'black'
                            word_surface = smaller_font.render(word, True, color)
                            word_rect = word_surface.get_rect(topleft=(x_offset, y))
                            screen.blit(word_surface, word_rect.topleft)
                            words_rects.append((word_rect, word))
                            x_offset += word_rect.width + 10
                            if word in words_before_empty_line:
                                y += 35
                        y += 20 

                if current_example['link']:
                    color = '#3A964B' if current_example['link'] in can_change_color else '#44A9DC'
                    link_surface = smaller_font.render(current_example['link'], True, color)
                    link_rect = link_surface.get_rect(topleft=(500, 480))
                    screen.blit(link_surface, link_rect.topleft)
                    words_rects.append((link_rect, current_example['link']))

            if len(can_change_color) == len(current_example['clickable_parts']) and not timer_started: # po oznaceni vsetkych podozrivych prvkov sa spusti casovac 
                remove_timer = pygame.time.get_ticks()  
                timer_started = True
                lock = True # zablokuje vstup hraca, aby sa nic nezmenilo pocas vymazania sprav
                
            if timer_started and pygame.time.get_ticks() - remove_timer > 1000: # ak uplynulo viac ako 1 sekunda, reset premennych, aktualizacia stavov chytenych ryb, odstrania sa chytene ryby zo zoznamu fishes
                current_example = None
                message_image = None
                message_image_rect = None
                if clicked_fish is not None:
                    caught_fish_positions.append((caught * 80, 10))
                    caught += 1
                    del fishes[clicked_fish]  
                    del phishing_examples[clicked_fish]  
                    clicked_fish = None
                lock = False # oblokuje sa vstup hraca, moze klikat dalej

        caught_fish_image = pygame.image.load('res/pictures/phishing/caught_fish.png') # vykreslenie chytenych ryb 
        for position in caught_fish_positions:
            screen.blit(caught_fish_image, position)

        if not fishes: # ak nie su ziadne ryby v hre (vsetky boli chytene), zobrazi sa obrazok next, pre pokracovanie do dalsej hry a hrac moze stlacit medzernik pre pokracovanie
            next_img = pygame.image.load('res/pictures/next.png')
            screen.blit(next_img, (380, 150))
            space_pressed = True

        pygame.display.flip() # aktualizacia obsahu obrazovky
        clock.tick(65) # obmedznie FPS
