import pygame

class Button:
    '''A flexible button class for pygame that supports images, text, or both with multi-line text support.'''
    
    def __init__(self, pos, image=None, text='', font_path="Assets/Source_files/fonts/font.ttf", font_size=10, base_color="black"):
        self.image = image
        self.x_pos, self.y_pos = pos
        self.base_color = base_color
        self.text_input = text.split('\n')  # Split text into multiple lines
        self.font = pygame.font.Font(font_path, font_size)
        
        # Render text lines
        self.text_surfaces = [self.font.render(line, True, self.base_color) for line in self.text_input]
        self.text_rects = [surf.get_rect() for surf in self.text_surfaces]
        
        # If an image is provided, use its dimensions; otherwise, use text dimensions
        if self.image:
            self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))
        else:
            width = max(rect.width for rect in self.text_rects)
            height = sum(rect.height for rect in self.text_rects)
            self.rect = pygame.Rect(self.x_pos, self.y_pos, width, height)
        
        # Adjust text positions
        y_offset = self.rect.top
        for rect in self.text_rects:
            rect.midtop = (self.rect.centerx, y_offset)
            y_offset += rect.height
    

    def update(self, screen):
        '''Draw the button (image + text if both are provided).'''
        if self.image:
            screen.blit(self.image, self.rect)
        for surf, rect in zip(self.text_surfaces, self.text_rects):
            screen.blit(surf, rect)
    

    def checkInput(self, position):
        '''Check if the given position is within the button's bounds.'''
        return self.rect.collidepoint(position)
    

    def changeColor(self, position, color):
        '''Change the text color if hovered.'''
        if self.checkInput(position):
            self.text_surfaces = [self.font.render(line, True, color) for line in self.text_input]
        else:
            self.text_surfaces = [self.font.render(line, True, self.base_color) for line in self.text_input]
