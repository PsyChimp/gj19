import pygame
from pygame.locals import *

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

    def draw(self, surface):
        pygame.draw.rect(surface, self.colors[self.state], self.rect)
        if self.state == "hovered":
            surface.blit(self.text_surf, self.text_pos)



if __name__ == "__main__":
    def foo():
        print("bar")

    pygame.init()

    screen = pygame.display.set_mode((512, 224))
    font = pygame.font.SysFont("KenneyPixelRegular.ttf", 16)
    font2 = pygame.font.SysFont("KenneyPixelRegular.ttf", 32)
    h = font.get_height()

    colors = {
        "default": (51, 153, 255),
        "hovered": (0, 128, 255),
        "clicked": (0, 102, 204),
        "disabled": (128, 128, 128),
        "text": (0, 0, 0)}

    buttons = [
        Button(pygame.Rect(32, 64, 128, 128), colors, font, "Button 1", foo),
        Button(pygame.Rect(192, 64, 128, 128), colors, font, "Button 2", foo),
        Button(pygame.Rect(352, 64, 128, 128), colors, font, "Button 3", foo)]


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
        for b in buttons:
            b.draw(screen)
        pygame.display.flip()

    pygame.quit()
