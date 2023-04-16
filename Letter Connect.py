import pygame
from pygame import time
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(0.8*SCREEN_WIDTH)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Letter Connect')

clock = pygame.time.Clock()
FPS = 60

BG = (200, 128, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.SysFont('Futura', 25)
font_letters = pygame.font.SysFont('Futura', 40)
font_small = pygame.font.SysFont('Futura', 23)

enter_btn = pygame.image.load('enter.png').convert_alpha()
restart_btn = pygame.image.load('restart.png').convert_alpha()

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

class Line(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, end_x, end_y, color):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.start_pos = (self.start_x, self.start_y)
        self.end_pos = (self.end_x, self.end_y)
        self.color = color

    def draw(self, thickness, width=0):
        if width > 0:
            self.thickness = 0

        else:
            self.thickness = thickness
            
        pygame.draw.line(screen, self.color, self.start_pos, self.end_pos, self.thickness)

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), (int(height * scale))))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
            
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
    
class Game(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, end_x, end_y, color, thickness):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.color = color
        self.thickness = thickness
        self.is_mouse_button_pressed = 0
        self.circle_1 = ()
        self.circle_2 = () 
        self.circle_3 = ()           
        self.circle_4 = ()
        self.circle_5 = ()
        self.circle_6 = ()
        self.circle_7 = ()
        self.circle_8 = () 
        self.circle_9 = ()           
        self.circle_10 = ()
        self.circle_11 = ()
        self.circle_12 = ()
        self.circle_activated = False
        self.line = pygame.draw.line(screen, BG, (0, 0), (0, 0), self.is_mouse_button_pressed)
        self.target_circles = []
        self.activated_circles = []
        self.circle_1 = screen, BLACK, ((self.start_x, self.end_y  - ((self.end_y - self.start_y) - ((self.end_y - self.start_y)/3) + 55))), 7, 2
        self.circle_2 = screen, BLACK, (self.start_x, self.end_y  - ((self.end_y - self.start_y) - ((self.end_y - self.start_y)/1.5) + 55)), 7, 2
        self.circle_3 = screen, BLACK,(self.start_x, self.end_y - 55), 7, 2   
        self.circle_4 = screen, BLACK,(self.end_x  - ((self.end_x - self.start_x) - ((self.end_x - self.start_x)/3)) + 55, self.start_y), 7, 2
        self.circle_5 = screen, BLACK, (self.end_x  - ((self.end_x - self.start_x) - ((self.end_x - self.start_x)/1.5)) + 55, self.start_y), 7, 2
        self.circle_6 = screen, BLACK, (self.end_x, self.end_y  - ((self.end_y - self.start_y) - ((self.end_y - self.start_y)/3) + 55)), 7, 2
        self.circle_7 = screen, BLACK,(self.end_x, self.end_y  - ((self.end_y - self.start_y) - ((self.end_y - self.start_y)/1.5) + 55)), 7, 2
        self.circle_8 = screen, BLACK, (self.end_x, self.end_y - 55), 7, 2
        self.circle_9 = screen, BLACK, (self.end_x  - ((self.end_x - self.start_x) - ((self.end_x - self.start_x)/1.5) + 50), self.end_y), 7, 2     
        self.circle_10 = screen, BLACK, (self.end_x  - ((self.end_x - self.start_x) - ((self.end_x - self.start_x)/3) + 50), self.end_y), 7, 2
        self.circle_11 = screen, BLACK,  (self.start_x + 55, self.start_y), 7, 2
        self.circle_12 =  screen, BLACK,(self.end_x - 50, self.end_y), 7, 2
        self.width_list = []
        for i in range(12):
            self.width_list.append(2)

        self.last_circle_index = -1
        self.circle_activated_index = -1
        self.letters = ['A', 'C', 'H', 'D', 'L', 'N', 'B', 'Y', 'E', 'K', 'T', 'W']
        self.typed_letters = []
        self.all_typed_letters = []
        self.selected_circle = ()
        self.total_words = 0
        
    def draw(self):
        circles = []
        pygame.draw.rect(screen, WHITE, (self.start_x, self.start_y, (self.end_x - self.start_x), (self.end_y - self.start_y)))
        pygame.draw.line(screen, self.color, (self.start_x, self.start_y),\
                         (self.start_x, self.end_y  - ((self.end_y - self.start_y) - ((self.end_y - self.start_y)/3))), self.thickness)
        
        pygame.draw.line(screen, self.color, (self.start_x, self.end_y  - ((self.end_y - self.start_y) - ((self.end_y - self.start_y)/3))),\
                         (self.start_x, self.end_y  - ((self.end_y - self.start_y) - ((self.end_y - self.start_y)/1.5))), self.thickness)

        pygame.draw.line(screen, self.color, (self.start_x, self.end_y  - ((self.end_y - self.start_y) - ((self.end_y - self.start_y)/1.5))),\
                         (self.start_x, self.end_y), self.thickness)
        
        pygame.draw.line(screen, self.color, (self.start_x, self.start_y),\
                         (self.end_x  - ((self.end_x - self.start_x) - ((self.end_x - self.start_x)/3)), self.start_y), self.thickness)
        
        pygame.draw.line(screen, self.color, (self.end_x  - ((self.end_x - self.start_x) - ((self.end_x - self.start_x)/3)), self.start_y),\
                         (self.end_x  - ((self.end_x - self.start_x) - ((self.end_x - self.start_x)/1.5)), self.start_y), self.thickness)
        
        pygame.draw.line(screen, self.color, (self.end_x  - ((self.end_x - self.start_x) - ((self.end_x - self.start_x)/1.5)), self.start_y),\
                         (self.end_x, self.start_y), self.thickness)
    
        pygame.draw.line(screen, self.color, (self.end_x, self.start_y),\
                         (self.end_x, self.end_y  - ((self.end_y - self.start_y) - ((self.end_y - self.start_y)/3))), self.thickness)
        
        pygame.draw.line(screen, self.color, (self.end_x, self.end_y  - ((self.end_y - self.start_y) - ((self.end_y - self.start_y)/3))),\
                         (self.end_x, self.end_y  - ((self.end_y - self.start_y) - ((self.end_y - self.start_y)/1.5))), self.thickness)

        pygame.draw.line(screen, self.color, (self.end_x, self.end_y  - ((self.end_y - self.start_y) - ((self.end_y - self.start_y)/1.5))),\
                         (self.end_x, self.end_y), self.thickness)
        
        pygame.draw.line(screen, self.color, (self.start_x, self.end_y),\
                         (self.end_x  - ((self.end_x - self.start_x) - ((self.end_x - self.start_x)/3)), self.end_y), self.thickness)
        
        pygame.draw.line(screen, self.color, (self.end_x  - ((self.end_x - self.start_x) - ((self.end_x - self.start_x)/3)), self.end_y),\
                         (self.end_x  - ((self.end_x - self.start_x) - ((self.end_x - self.start_x)/1.5)), self.end_y), self.thickness)
        
        pygame.draw.line(screen, self.color, (self.end_x  - ((self.end_x - self.start_x) - ((self.end_x - self.start_x)/1.5)), self.end_y),\
                         (self.end_x, self.end_y), self.thickness)

                     
        pygame.draw.circle(screen, WHITE, ((self.start_x, self.end_y  - ((self.end_y - self.start_y) - ((self.end_y - self.start_y)/3) + 55))), 5)
        pygame.draw.circle(screen, WHITE, (self.start_x, self.end_y  - ((self.end_y - self.start_y) - ((self.end_y - self.start_y)/1.5) + 55)), 5)
        pygame.draw.circle(screen, WHITE,(self.start_x, self.end_y - 55), 5)
        pygame.draw.circle(screen, WHITE,(self.end_x  - ((self.end_x - self.start_x) - ((self.end_x - self.start_x)/3)) + 55, self.start_y), 5)
        pygame.draw.circle(screen, WHITE, (self.end_x  - ((self.end_x - self.start_x) - ((self.end_x - self.start_x)/1.5)) + 55, self.start_y), 5)
        
        pygame.draw.circle(screen, WHITE, (self.end_x, self.end_y  - ((self.end_y - self.start_y) - ((self.end_y - self.start_y)/3) + 55)), 5)
        pygame.draw.circle(screen, WHITE,(self.end_x, self.end_y  - ((self.end_y - self.start_y) - ((self.end_y - self.start_y)/1.5) + 55)), 5)
        pygame.draw.circle(screen, WHITE, (self.end_x, self.end_y - 55), 5)
        pygame.draw.circle(screen, WHITE, (self.end_x  - ((self.end_x - self.start_x) - ((self.end_x - self.start_x)/1.5) + 50), self.end_y), 5)
        pygame.draw.circle(screen, WHITE, (self.end_x  - ((self.end_x - self.start_x) - ((self.end_x - self.start_x)/3) + 50), self.end_y), 5)
        pygame.draw.circle(screen, WHITE,  (self.start_x + 55, self.start_y), 5)
        pygame.draw.circle(screen, WHITE,(self.end_x - 50, self.end_y), 5)

        self.circle_1 = screen, BLACK, ((self.start_x, self.end_y  - ((self.end_y - self.start_y) - ((self.end_y - self.start_y)/3) + 55))), 7, self.width_list[0]
        self.circle_2 = screen, BLACK, (self.start_x, self.end_y  - ((self.end_y - self.start_y) - ((self.end_y - self.start_y)/1.5) + 55)), 7, self.width_list[1]
        self.circle_3 = screen, BLACK,(self.start_x, self.end_y - 55), 7, self.width_list[2]
        self.circle_4 = screen, BLACK,(self.end_x  - ((self.end_x - self.start_x) - ((self.end_x - self.start_x)/3)) + 55, self.start_y), 7, self.width_list[3]
        self.circle_5 = screen, BLACK, (self.end_x  - ((self.end_x - self.start_x) - ((self.end_x - self.start_x)/1.5)) + 55, self.start_y), 7, self.width_list[4]
        self.circle_6 = screen, BLACK, (self.end_x, self.end_y  - ((self.end_y - self.start_y) - ((self.end_y - self.start_y)/3) + 55)), 7, self.width_list[5]
        self.circle_7 = screen, BLACK,(self.end_x, self.end_y  - ((self.end_y - self.start_y) - ((self.end_y - self.start_y)/1.5) + 55)), 7, self.width_list[6]
        self.circle_8 = screen, BLACK, (self.end_x, self.end_y - 55), 7, self.width_list[7]
        self.circle_9 = screen, BLACK, (self.end_x  - ((self.end_x - self.start_x) - ((self.end_x - self.start_x)/1.5) + 50), self.end_y), 7, self.width_list[8]   
        self.circle_10 = screen, BLACK, (self.end_x  - ((self.end_x - self.start_x) - ((self.end_x - self.start_x)/3) + 50), self.end_y), 7, self.width_list[9]
        self.circle_11 = screen, BLACK,  (self.start_x + 55, self.start_y), 7, self.width_list[10]
        self.circle_12 =  screen, BLACK,(self.end_x - 50, self.end_y), 7, self.width_list[11]

        circle_1_rect = pygame.draw.circle(self.circle_1[0], self.circle_1[1], self.circle_1[2], self.circle_1[3], self.circle_1[4])
        circle_2_rect = pygame.draw.circle(self.circle_2[0], self.circle_2[1], self.circle_2[2], self.circle_2[3], self.circle_2[4])
        circle_3_rect = pygame.draw.circle(self.circle_3[0], self.circle_3[1], self.circle_3[2], self.circle_3[3], self.circle_3[4])
        circle_4_rect = pygame.draw.circle(self.circle_4[0], self.circle_4[1], self.circle_4[2], self.circle_4[3], self.circle_4[4])
        circle_5_rect = pygame.draw.circle(self.circle_5[0], self.circle_5[1], self.circle_5[2], self.circle_5[3], self.circle_5[4])
        circle_6_rect = pygame.draw.circle(self.circle_6[0], self.circle_6[1], self.circle_6[2], self.circle_6[3], self.circle_6[4])
        circle_7_rect = pygame.draw.circle(self.circle_7[0], self.circle_7[1], self.circle_7[2], self.circle_7[3], self.circle_7[4])
        circle_8_rect = pygame.draw.circle(self.circle_8[0], self.circle_8[1], self.circle_8[2], self.circle_8[3], self.circle_8[4])
        circle_9_rect = pygame.draw.circle(self.circle_9[0], self.circle_9[1], self.circle_9[2], self.circle_9[3], self.circle_9[4])
        circle_10_rect = pygame.draw.circle(self.circle_10[0], self.circle_10[1], self.circle_10[2], self.circle_10[3], self.circle_10[4])
        circle_11_rect = pygame.draw.circle(self.circle_11[0], self.circle_11[1], self.circle_11[2], self.circle_11[3], self.circle_11[4])
        circle_12_rect = pygame.draw.circle(self.circle_12[0], self.circle_12[1], self.circle_12[2], self.circle_12[3], self.circle_12[4])

        circles.append(circle_1_rect)
        circles.append(circle_2_rect)
        circles.append(circle_3_rect)
        circles.append(circle_4_rect)
        circles.append(circle_5_rect)
        circles.append(circle_6_rect)
        circles.append(circle_7_rect)
        circles.append(circle_8_rect)
        circles.append(circle_9_rect)
        circles.append(circle_10_rect)
        circles.append(circle_11_rect)
        circles.append(circle_12_rect)

        if self.circle_activated and self.selected_circle == ():
            self.line = pygame.draw.line(screen, BG, (self.circle_activated.x, self.circle_activated.y), (self.mouse_x, self.mouse_y), self.is_mouse_button_pressed)
        
        elif self.circle_activated == self.selected_circle and self.circle_activated:
            self.line = pygame.draw.line(screen, BG, (self.circle_activated.x, self.circle_activated.y), (self.mouse_x, self.mouse_y), self.is_mouse_button_pressed)

        if self.activated_circles:
            for circle in range(len(self.target_circles)):
                    self.line = pygame.draw.line(screen, BG, (self.activated_circles[circle].x, self.activated_circles[circle].y), (self.target_circles[circle].x, self.target_circles[circle].y), 3)

        return circles

    def check_same_line(self, i):
        if self.letters[self.circle_activated_index] == 'A':
            if self.letters[i] == 'C':
                return False
            
            elif self.letters[i] == 'H':
                return False
            
            else:
                return True
        elif self.letters[self.circle_activated_index] == 'C':
            if self.letters[i] == 'A':
                return False
            
            elif self.letters[i] == 'H':
                return False
            
            else:
                return True

        elif self.letters[self.circle_activated_index] == 'H':
            if self.letters[i] == 'A':
                return False
            
            elif self.letters[i] == 'C':
                return False
            
            else:
                return True
            
        elif self.letters[self.circle_activated_index] == 'T':
            if self.letters[i] == 'D':
                return False
            
            elif self.letters[i] == 'L':
                return False
            
            else:
                return True
        
            
        elif self.letters[self.circle_activated_index] == 'D':
            if self.letters[i] == 'T':
                return False
            
            elif self.letters[i] == 'L':
                return False
            
            else:
                return True
        elif self.letters[self.circle_activated_index] == 'L':
            if self.letters[i] == 'D':
                return False
            
            elif self.letters[i] == 'T':
                return False
            
            else:
                return True
        elif self.letters[self.circle_activated_index] == 'N':
            if self.letters[i] == 'B':
                return False
            
            elif self.letters[i] == 'Y':
                return False
            
            else:
                return True
            
        elif self.letters[self.circle_activated_index] == 'B':
            if self.letters[i] == 'Y':
                return False
            
            elif self.letters[i] == 'N':
                return False
            
            else:
                return True
            
        elif self.letters[self.circle_activated_index] == 'Y':
            if self.letters[i] == 'N':
                return False
            
            elif self.letters[i] == 'B':
                return False
            
            else:
                return True
            
        elif self.letters[self.circle_activated_index] == 'W':
            if self.letters[i] == 'E':
                return False
            
            elif self.letters[i] == 'K':
                return False
            
            else:
                return True
            
        elif self.letters[self.circle_activated_index] == 'E':
            if self.letters[i] == 'K':
                return False
            
            elif self.letters[i] == 'W':
                return False
            
            else:
                return True
        
        elif self.letters[self.circle_activated_index] == 'K':
            if self.letters[i] == 'W':
                return False
            
            elif self.letters[i] == 'E':
                return False
            
            else:
                return True
        else: 
            return False
            
    def update(self, circles):
        if pygame.mouse.get_pressed(3)[0] == True:
            circles = circles

            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
            i = 0
            for circle in circles:
                if circle.colliderect(self.mouse_x, self.mouse_y, 7, 7):
                    if circle == self.circle_activated or self.circle_activated == ():
                            self.circle_activated = circle
                            self.is_mouse_button_pressed = 3
                            self.circle_activated_index = i

                    elif self.check_same_line(i) and self.circle_activated and self.selected_circle == ():
                        
                        self.activated_circles.append(self.circle_activated)

                        self.target_circles.append(circle)

                        self.last_circle_index = i 

                        if self.letters[self.circle_activated_index] not in self.typed_letters and self.circle_activated_index != -1:
                            self.typed_letters.append(self.letters[self.circle_activated_index])

                            
                        self.typed_letters.append(self.letters[i])
                        if self.letters[self.circle_activated_index] not in self.all_typed_letters:
                            self.all_typed_letters.append(self.letters[self.circle_activated_index])

                        self.all_typed_letters.append(self.letters[i])

                        self.circle_activated = ()
                        self.is_mouse_button_pressed = 0
                        self.width_list[i] = 0
                        if self.last_circle_index != -1:
                            self.width_list[self.last_circle_index] = 2
                        self.selected_circle = self.target_circles[len(self.target_circles)-1]

                    elif self.check_same_line(i) and self.circle_activated == self.selected_circle and self.circle_activated:
                        self.activated_circles.append(self.circle_activated)

                        self.target_circles.append(circle)

                        self.last_circle_index = i 

                        if self.letters[self.circle_activated_index] not in self.typed_letters and self.circle_activated_index != -1:
                            self.typed_letters.append(self.letters[self.circle_activated_index])

                            
                        self.typed_letters.append(self.letters[i])
                        if self.letters[self.circle_activated_index] not in self.all_typed_letters:
                            self.all_typed_letters.append(self.letters[self.circle_activated_index])

                        self.all_typed_letters.append(self.letters[i])

                        self.circle_activated = ()
                        self.is_mouse_button_pressed = 0
                        self.width_list[i] = 0
                        if self.last_circle_index != -1:
                            self.width_list[self.last_circle_index] = 2
                        self.selected_circle = self.target_circles[len(self.target_circles)-1]

                i += 1

                
        else:
            self.circle_activated = ()
            self.is_mouse_button_pressed = 0

    def enter(self):
        word = ''
        for letter in self.typed_letters:
            word += letter
        file = open('20k.txt','r')
        words = file.readlines()
        word = word.lower()

        file.close()

        if word + '\n' in words:

            self.selected_circle = self.target_circles[len(self.target_circles)-1]
            self.typed_letters = []
            self.total_words += 1

def draw_letters():
    if 'L' in box.all_typed_letters:
        l_colour = BLACK
    else:
        l_colour = WHITE
    if 'N' in box.all_typed_letters:
        n_colour = BLACK
    else:
        n_colour = WHITE
    if 'B' in box.all_typed_letters:
        b_colour = BLACK
    else:
        b_colour = WHITE
    if 'Y' in box.all_typed_letters:
        y_colour = BLACK
    else:
        y_colour = WHITE
    if 'W' in box.all_typed_letters:
        w_colour = BLACK
    else:
        w_colour = WHITE
    if 'E' in box.all_typed_letters:
        e_colour = BLACK
    else:
        e_colour = WHITE
    if 'K' in box.all_typed_letters:
        k_colour = BLACK
    else:
        k_colour = WHITE
    if 'A' in box.all_typed_letters:
        a_colour = BLACK
    else:
        a_colour = WHITE
    if 'C' in box.all_typed_letters:
        c_colour = BLACK
    else:
        c_colour = WHITE
    if 'H' in box.all_typed_letters:
        h_colour = BLACK
    else:
        h_colour = WHITE
    if 'T' in box.all_typed_letters:
        t_colour = BLACK
    else:
        t_colour = WHITE
    if 'D' in box.all_typed_letters:
        d_colour = BLACK
    else:
        d_colour = WHITE

    draw_text('A', font_letters, a_colour, 383, 248)
    draw_text('C', font_letters, c_colour, 383, 353)
    draw_text('H', font_letters, h_colour, 383, 463)
    draw_text('T', font_letters, t_colour, 463, 158)
    draw_text('D', font_letters, d_colour, 573, 158)
    draw_text('L', font_letters, l_colour, 683, 158)
    draw_text('N', font_letters, n_colour, 768, 238)
    draw_text('B', font_letters, b_colour, 768, 352)
    draw_text('Y', font_letters, y_colour, 768, 462)
    draw_text('W', font_letters, w_colour, 688, 552)
    draw_text('E', font_letters, e_colour, 583, 552)
    draw_text('K', font_letters, k_colour, 475, 552)

dash = Line(100, 200, 350, 200, BLACK)
dash2 = Line(225, 160, 225, 175, BLACK)
enter_button = Button(125, 275, enter_btn, 0.5)
restart_button = Button(225, 275, restart_btn, 0.4)
box = Game(420, 200, 750, 530, BLACK, 3)
current_time = 0
run = True

while run:
    clock.tick(FPS)
    screen.fill(BG)
    dash.draw(3)
    dash2.draw(3, current_time%(FPS/2))
    draw_text('Try to solve in 5 words', font, BLACK, 135, 225)
    if box.total_words == 1:
        draw_text(f'You have solved in {box.total_words} word', font_small, BLACK, 130, 425)
    elif box.total_words != 0:
        draw_text(f'You have solved in {box.total_words} words', font_small, BLACK, 130, 425)
    for i in range(len(box.typed_letters)):
        letter_pos = 225 - (-i * 25) - 125
        draw_text(box.typed_letters[i], font, BLACK, letter_pos, 160)

    circles = box.draw()

    draw_letters()
    if enter_button.draw(screen):
        box.enter()

    if restart_button.draw(screen):
        box.__init__(420, 200, 750, 530, BLACK, 3)

    box.update(circles)

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            run = False
    
    current_time = time.get_ticks()
    pygame.display.update()


pygame.quit()