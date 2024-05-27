import pygame
pygame.init()
display = None

# Ekran boyut ataması
def init(screen):
    global display
    display = screen

# Button Olusturma
class Button:
    def __init__(self, x, y, w, h, action=None, colorNotActive=(189, 195, 199), colorActive=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.colorActive = colorActive
        self.colorNotActive = colorNotActive

        self.action = action

        self.font = None
        self.text = None
        self.text_pos = None

    def add_text(self, text, size=20, font="Times New Roman", text_color=(0, 0, 0)):
        self.font = pygame.font.Font(font, size)
        self.text = self.font.render(text, True, text_color)
        self.text_pos = self.text.get_rect()

        self.text_pos.center = (self.x + self.w/2, self.y + self.h/2)

    def draw(self):
        if self.isActive():
            if not self.colorActive == None:
                pygame.draw.rect(display, self.colorActive, (self.x, self.y, self.w, self.h))
        else:
            pygame.draw.rect(display, self.colorNotActive, (self.x, self.y, self.w, self.h))

        if self.text:
            display.blit(self.text, self.text_pos)

    def isActive(self):
        pos = pygame.mouse.get_pos()

        if (self.x < pos[0] < self.x + self.w) and (self.y < pos[1] < self.y + self.h):
            return True
        else:
            return False

class Label(Button):
    def draw(self):
        if self.text:
            display.blit(self.text, self.text_pos)
"""

import pygame 
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()
display = None

def init(screen):
    global display
    display = screen
    # OpenGL ile ilgili ayarları yapalım
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glClearColor(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluOrtho2D(0, display.get_width(), display.get_height(), 0)

class Button:
    def __init__(self, x, y, w, h, action=None, colorNotActive=(189, 195, 199, 255), colorActive=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.colorActive = colorActive
        self.colorNotActive = colorNotActive

        self.action = action

        self.font = None
        self.text = None
        self.text_pos = None

    def add_text(self, text, size=20, font="Times New Roman", text_color=(0, 0, 0)):
        self.font = pygame.font.Font(pygame.font.match_font(font), size)
        self.text = self.font.render(text, True, text_color)
        self.text_pos = self.text.get_rect()

        self.text_pos.center = (self.x + self.w/2, self.y + self.h/2)

    def draw(self):
        if self.isActive():
            if self.colorActive is not None:
                self.draw_rect(self.colorActive)
        else:
            self.draw_rect(self.colorNotActive)

        if self.text:
            display.blit(self.text, self.text_pos)

    def draw_rect(self, color):
        glColor4f(color[0]/255.0, color[1]/255.0, color[2]/255.0, color[3]/255.0 if len(color) == 4 else 1.0)
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.w, self.y)
        glVertex2f(self.x + self.w, self.y + self.h)
        glVertex2f(self.x, self.y + self.h)
        glEnd()

    def isActive(self):
        pos = pygame.mouse.get_pos()

        if (self.x < pos[0] < self.x + self.w) and (self.y < pos[1] < self.y + self.h):
            return True
        else:
            return False

class Label(Button):
    def draw(self):
        if self.text:
            display.blit(self.text, self.text_pos)

# Pygame ekranı oluşturma ve OpenGL başlatma
pygame.display.set_mode((800, 600), pygame.DOUBLEBUF | pygame.OPENGL)
init(pygame.display.get_surface())

button = Button(100, 100, 200, 50, colorActive=(231, 76, 60, 255))
button.add_text("Click Me")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    button.draw()
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
"""