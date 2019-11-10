import pygame
from pygame.locals import *
import random



class Button(object):
    def __init__(self, rect, colors, font, text, on_click, *args):

        self.rect = rect
        self.colors = colors
        self.text_surf = font.render(text, True, colors["text"])
        dims = self.text_surf.get_size()
        self.text_pos = (
            self.rect.centerx - dims[0] / 2,
            self.rect.centery - dims[1] / 2)
        self.on_click = on_click
        self.args = args
        self.state = "default"

    def handle_event(self, event):
        if self.state == "disabled":
            return
        self.state = "default"
        mpos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mpos):
            self.state = "hovered"
        if self.state == "hovered":
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                self.state = "clicked"
                self.on_click(*self.args)
        if event.type == MOUSEBUTTONUP:
            self.state = "default"

    def draw(self, surface, image):
        pygame.draw.rect(surface, self.colors[self.state], self.rect,6)
        surface.blit(image, self.rect)
        if self.state == "hovered":
            pygame.draw.rect(surface, (24, 37, 46), self.rect)
            surface.blit(self.text_surf, self.text_pos)


if __name__ == "__main__":
    def foo():
        print("bar")

    pygame.init()
    counter = 0




    screen = pygame.display.set_mode((518, 230))
    background = pygame.image.load("./img/ui/Item Boxes.png")
    icon1 = pygame.image.load("./img/icons/1_attack_big.png")
    icon2 = pygame.image.load("./img/icons/1hp_big.png")
    icon3 = pygame.image.load("./img/icons/blur_vision_big.png")
    icon4 = pygame.image.load("./img/icons/no_vision_big.png")
    icon5 = pygame.image.load("./img/icons/slow_mov_speed_big.png")
    icon6 = pygame.image.load("./img/icons/timer_big.png")
    icon7 = pygame.image.load("./img/icons/extra_room_big.png")
    icon8 = pygame.image.load("./img/icons/plus_acid_big.png")
    icon9 = pygame.image.load("./img/icons/plus_enemy_attack_big.png")
    icon10 = pygame.image.load("./img/icons/plus_enemy_health_big.png")
    icon11 = pygame.image.load("./img/icons/plus_enemy_speed_big.png")
    icon12 = pygame.image.load("./img/icons/no_dash_big.png")
    font = pygame.font.Font("./font/Kenney Pixel.ttf", 32)
    font2 = pygame.font.Font("./font/Kenney Pixel.ttf", 64)
    h = font.get_height()

    colors = {
        "default": (79, 182, 166),
        "hovered": (0, 128, 255),
        "clicked": (0, 102, 204),
        "disabled": (128, 128, 128),
        "text": (255, 255, 255)}
    i = random.randint(0, 11)
    j = random.randint(0, 11)
    w = random.randint(0, 11)
    if i == j:
        while i == j:
            i = random.randint(0, 11)
            j = random.randint(0, 11)
    elif i == w:
        while i == w:
            i = random.randint(0, 11)
            w = random.randint(0, 11)
    elif j == w:
        while j == w:
            j = random.randint(0, 11)
            w = random.randint(0, 11)
    numbers = [
        i, j, w
    ]
    if numbers[0] == 0:
        text1 = "One attack"
    elif numbers[0] == 1:
        text1 = "Have one HP"
    elif numbers[0] == 2:
        text1 = "Blur Vision"
    elif numbers[0] == 3:
        text1 = "No Vision"
    elif numbers[0] == 4:
        text1 = "Slow Move"
    elif numbers[0] == 5:
        text1 = "Less Timer"
    elif numbers[0] == 6:
        text1 = "Extra Room"
    elif numbers[0] == 7:
        text1 = "Plus ACID!"
    elif numbers[0] == 8:
        text1 = "Enemy Atk up"
    elif numbers[0] == 9:
        text1 = "Enemy HP up"
    elif numbers[0] == 10:
        text1 = "Enemy Spd up"
    elif numbers[0] == 11:
        text1 = "No Dash"
    else:
        text1 = "error"
    if numbers[1] == 0:
        text2 = "One attack"
    elif numbers[1] == 1:
        text2 = "Have one HP"
    elif numbers[1] == 2:
        text2 = "Blur Vision"
    elif numbers[1] == 3:
        text2 = "No Vision"
    elif numbers[1] == 4:
        text2 = "Slow Move"
    elif numbers[1] == 5:
        text2 = "Less Timer"
    elif numbers[1] == 6:
        text2 = "Extra Room"
    elif numbers[1] == 7:
        text2 = "Plus ACID!"
    elif numbers[1] == 8:
        text2 = "Enemy Atk up"
    elif numbers[1] == 9:
        text2 = "Enemy HP up"
    elif numbers[1] == 10:
        text2 = "Enemy Spd up"
    elif numbers[1] == 11:
        text2 = "No Dash"
    else:
        text2 = "error"
    if numbers[2] == 0:
        text3 = "One attack"
    elif numbers[2] == 1:
        text3 = "Have one HP"
    elif numbers[2] == 2:
        text3 = "Blur Vision"
    elif numbers[2] == 3:
        text3 = "No Vision"
    elif numbers[2] == 4:
        text3 = "Slow Move"
    elif numbers[2] == 5:
        text3 = "Less Timer"
    elif numbers[2] == 6:
        text3 = "Extra Room"
    elif numbers[2] == 7:
        text3 = "Plus ACID!"
    elif numbers[2] == 8:
        text3 = "Enemy Atk up"
    elif numbers[2] == 9:
        text3 = "Enemy HP up"
    elif numbers[2] == 10:
        text3 = "Enemy Spd up"
    elif numbers[2] == 11:
        text3 = "No Dash"
    else:
        text3 = "error"
    text4 = font2.render("Choose Your Fate", True, (255, 255, 255))
    icons = [
        icon1, icon2, icon3, icon4, icon5, icon6, icon7, icon8, icon9, icon10, icon11, icon12
    ]
    buttons = [
        Button(pygame.Rect(32, 64, 128, 128), colors, font, text1, foo),
        Button(pygame.Rect(192, 64, 128, 128), colors, font, text2, foo),
        Button(pygame.Rect(352, 64, 128, 128), colors, font, text3, foo)]


    while True:
        e = pygame.event.poll()
        if e.type == QUIT:
            break
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                break

        for b in buttons:
            b.handle_event(e)

        screen.fill((255, 255, 255))
        screen.blit(background,(0,0))

        for b in buttons:
            b.draw(screen, icons[numbers[counter]])
            counter += 1
            if counter >= 3:
                counter = 0
        screen.blit(text4, (80, 0))
        pygame.display.flip()

    pygame.quit()
