import pygame
import random

class Fish: # trieda pre objekt ryba
    def __init__(self, image_paths, x, y, move_speed, frame_delay, resize=True, resize_width=50, resize_height=50): 
        self.org_images = [pygame.image.load(path) for path in image_paths] # nacitanie obrazkov pre animaciu

        if resize: # moznost zmenenie velkosti
            self.new_size = (resize_width, resize_height)
            self.images = [pygame.transform.scale(image, self.new_size) for image in self.org_images]
        else:
            self.images = self.org_images
            frame_width, frame_height = self.org_images[0].get_size()
            self.new_size = (frame_width, frame_height)

        self.flipped_images = [pygame.transform.flip(image, True, False) for image in self.images] # prevratenie obrazkov pre opacny smer pohybu

        self.x = x
        self.y = y
        self.move_speed = move_speed
        self.flipped = move_speed < 0
        self.current_frame = 0
        self.frame_delay = frame_delay
        self.frame_counter = 0

        self.rect = pygame.Rect(self.x, self.y, *self.new_size) 

    def update(self, screen_width): 
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay: # animacia ryby
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.frame_counter = 0

        self.x += self.move_speed # pohyb ryby a odraz od okrajov, zmenenie smeru
        if self.x + self.new_size[0] > screen_width or self.x < 0:
            self.move_speed = -self.move_speed
            self.flipped = not self.flipped

        self.rect.topleft = (self.x, self.y)

    def draw(self, screen): # vykreslenie
        if self.flipped:
            current_image = self.flipped_images[self.current_frame]
        else:
            current_image = self.images[self.current_frame]
        screen.blit(current_image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.new_size[0], self.new_size[1]) # vrati objekt z pygame Rect, pre kolizie
    
class Bubble: # trieda pre objekt Bublina
    def __init__(self, screen_width, screen_height, number_of_bubbles, bubble_image_path, min_speed=1, max_speed=3, min_size=20, max_size=50):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bubbles = []
        self.bubble_image = pygame.image.load(bubble_image_path) # nacitanie obrazku

        for i in range(number_of_bubbles): # generovanie nahodnych bublin 
            size = random.randint(min_size, max_size)
            resized_image = pygame.transform.scale(self.bubble_image, (size, size))
            x = random.randint(0, screen_width - size)
            y = random.randint(100, screen_height -100)
            speed = random.randint(min_speed, max_speed)
            self.bubbles.append([x, y, size, speed, resized_image])  

    def update(self): # pohyb bublin horizontalne
        for bubble in self.bubbles:
            bubble[1] -= bubble[3]  
            if bubble[1] + bubble[2] < 0:
                bubble[1] = self.screen_height + bubble[2]
                bubble[0] = random.randint(0, self.screen_width - bubble[2])
                bubble[3] = random.randint(1, 3)

    def draw(self, screen): # vykreslenie vsetkych bublin
        for bubble in self.bubbles:
            screen.blit(bubble[4], (int(bubble[0]), int(bubble[1])))

class TextPhishing: # trieda pre interaktivny text, ktory sa vyuziva v hre v kategorii phishing
    def __init__(self, first_image_path, arrow_image_path, third_image_path, x, y, screen):
        self.x = x
        self.y = y
        self.first_image = pygame.image.load(first_image_path)
        self.arrow_image = pygame.transform.scale(pygame.image.load(arrow_image_path), (110, 80))
        self.third_image = pygame.image.load(third_image_path)
        self.arrow_rect = self.arrow_image.get_rect()
        self.arrow_clicked = False
        self.screen = screen
    
    def draw(self, screen): # vykreslenie prveho obrazku
        screen.blit(self.first_image, (self.x, self.y))
        arrow_x = self.x + self.first_image.get_width() - 130
        arrow_y = self.y + self.first_image.get_height() - 100
        
        if not self.arrow_clicked: # ak nie je kliknuta sipka, vykreslim ju
            screen.blit(self.arrow_image, (arrow_x, arrow_y))
            self.arrow_rect.topleft = (arrow_x, arrow_y)
        if self.arrow_clicked: # ak je, vykreslim novy obrazok
            screen.blit(self.third_image, (self.x, self.y))  

    def check_arrow_click(self, mouse_pos): # kontrola ci je kliknuty obrazok so sipkou
        if self.arrow_rect.collidepoint(mouse_pos):
            self.arrow_clicked = True
    
    def run(self, screen): # hlavny cyklus
        running = True
        while running:
            screen.fill('#EBEBEB')  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: 
                        self.check_arrow_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.arrow_clicked:
                            return

            self.draw(screen)
            pygame.display.flip()
