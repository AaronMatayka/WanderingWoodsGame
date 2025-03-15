# Button class for main menu
import pygame

from src import universal_variables

pygame.init()

class Button:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = universal_variables.BUTTON_BG_COLOR  # Dark Blue
        self.hover_color = universal_variables.BUTTON_BG_HOVER_COLOR  # Light Blue
        self.font = universal_variables.BUTTON_FONT
        self.text_surf = self.font.render(text, True, universal_variables.BUTTON_TEXT_COLOR)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        # If the mouse is hovering over the button, change its bg color to hover color, otherwise paint normally
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        screen.blit(self.text_surf, self.text_rect)

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
