import pygame
import time
from programs.managers import password_games_manager
from programs.managers import phishing_games_manager
from programs.managers import sensitive_data_manager # import vsetkych managerov pre minihry


pygame.init() # inicializacia pygame a nastavenie okna a hlavnych premennych, nacitanie fontu a obrazkov
screen = pygame.display.set_mode((1300, 750))

category_width, category_height = 550, 120
x_pos = (screen.get_width() - category_width) // 2
font = pygame.font.Font('res/font/final_fantasy_36_font.ttf', 60)
inf_image = pygame.image.load('res/pictures/inf.png')
restart_image = pygame.transform.scale(pygame.image.load('res/pictures/restart.png'), (80, 80))

class Category: # trieda pre objekt Category - blok na ktory sa da klikat
    def __init__(self, x, y, color, text):
        self.rect = pygame.Rect(x, y, category_width, category_height)
        self.color = color
        self.original_color = color  
        self.outline = 'white'
        self.hovered = False
        self.text = text
        self.original_text = text  
        self.x = x
        self.y = y
        self.completed = False
        self.timer = None  

    def draw(self, screen):
        if self.completed and self.timer and time.time() - self.timer <= 1:    # ak je kategoria splnena a od posledneho kliknutia ubehla ≤ 1 sekunda, zmeni sa na chvilu farbu aj text aby sa indikovalo, ze kategoria je uz vyriesena
            new_color = '#7DAB7F' 
            new_text = 'VYRIEŠENÉ'
            pygame.draw.rect(screen, new_color, self.rect, border_radius=30)
            text_surface = font.render(new_text, True, 'white')
        else:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=30) # klasicke zobrazenie nevyriesenej kategorie
            text_surface = font.render(self.text, True, 'white')

        pygame.draw.rect(screen, self.outline, self.rect, 5, border_radius=30)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def hover(self, mouse_x, mouse_y): # ak sa kurzor nachadza nad tlacidlom, outline obdlznika (bloku/kategorie) sa zmeni na cierno
        self.hovered = self.rect.collidepoint(mouse_x, mouse_y)
        self.outline = 'black' if self.hovered else 'white'

    def click(self, mouse_x, mouse_y):
        return self.rect.collidepoint(mouse_x, mouse_y) # vrati True, ak sa kliklo na danu kategoriu


class Menu: # trieda pre cele menu
    def __init__(self):
        self.categories = [
            Category(x_pos, 200, '#2E294E', 'OSOBNÉ ÚDAJE'),
            Category(x_pos, 360, '#BE97C6', 'HESLÁ'),
            Category(x_pos, 520, '#4B5267', 'PHISHING')] # inicializacia kategorii

        self.inf_text_image = pygame.image.load('res/pictures/inf_text.png')  
        self.inf_text_displayed = False  # urcuje, ci sa maju zobrazit pravidla/informacie o hre

    def update(self, mouse_x, mouse_y): # ak nie su zobrazene pravidla, viem zmenit outline bloku
        if not self.inf_text_displayed:  
            for category in self.categories:
                category.hover(mouse_x, mouse_y)

    def click(self, mouse_x, mouse_y): # funkcia kontrolujuca klikanie 
        inf_rect = inf_image.get_rect(topleft=(10, 10))  
        inf_text_rect = self.inf_text_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

        if self.inf_text_displayed:  
            if not inf_text_rect.collidepoint(mouse_x, mouse_y): # ak su zobrazene pravidla, skryju sa ak je kliknute mimo ich plochy
                self.inf_text_displayed = False 
        else:
            if inf_rect.collidepoint(mouse_x, mouse_y): # ak sa kliklo na inf obrazok, zobrazia sa pravidla
                self.inf_text_displayed = True  
            elif restart_image.get_rect(topleft=(1200, 10)).collidepoint(mouse_x, mouse_y): # ak je kliknutie na restart tlacidlo, vyriesene kategorie sa oznacia ako nevyriesene a daju sa opat hrat
                for category in self.categories:
                    category.completed = False
                    category.timer = None
            else:
                for i, category in enumerate(self.categories): # spracovanie kliknutia na konkretnu kategoriu
                    if category.click(mouse_x, mouse_y):
                        if not category.completed:
                            if i == 0 and sensitive_data_manager.run(): # ak sa kliklo na prvu kategoriu a spustil sa sensitive_data_manager(), ktory vrati true, kategoria sa oznaci ako splnena
                                category.completed = True
                            elif i == 1 and password_games_manager.run(): # ak sa kliklo na druhu kategoriu a spustil sa password_games_manager(), ktory vrati true, kategoria sa oznaci ako splnena
                                category.completed = True
                            elif i == 2 and phishing_games_manager.run(): # ak sa kliklo na tretiu kategoriu a spustil sa phishing_games_manager(), ktory vrati true, kategoria sa oznaci ako splnena
                                category.completed = True
                        elif category.completed:     # opatovné kliknutie zobrazí zelenú animáciu "VYRIEŠENÉ", ak je kategoria splnena
                            category.timer = time.time()

    def draw(self, screen): # vykreslenie vsetkych prvkov v menu
        for category in self.categories:
            category.draw(screen)
            if category.completed: # ak je kategoria splnena, prida sa hviezdicka, na oznacenie
                star_image = pygame.image.load('res/pictures/star.png')
                screen.blit(star_image, (category.x + 485, category.y + 57))

        title_surf = font.render('VITAJTE V HRE', True, 'black') # nadpis
        title_rect = title_surf.get_rect(center=(screen.get_width() // 2, 50))
        screen.blit(title_surf, title_rect)
        screen.blit(inf_image, (10, 10)) # info tlacidlo
        screen.blit(restart_image, (1200, 10)) # reset tlacidlo

        if self.inf_text_displayed: # vykreslenie pravidiel
            inf_text_rect = self.inf_text_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(self.inf_text_image, inf_text_rect)

    def display(self):
        running = True
        while running: # hlavny cyklus
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.click(mouse_x, mouse_y)

            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.update(mouse_x, mouse_y)

            screen.fill('#EBEBEB')
            self.draw(screen)
            pygame.display.flip()

        pygame.quit()
