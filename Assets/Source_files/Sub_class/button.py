import pygame

class Button:
    '''A flexible button class for pygame that supports images, text, or both with multi-line text support.'''
    
    def __init__(self, pos, image=None, text='', font_path="Assets/Source_files/fonts/font.ttf", font_size=10, base_color="black", 
                 hover_color=(100, 100, 255), animation_speed=5):
        self.image = image
        self.x_pos, self.y_pos = pos
        self.base_color = base_color
        self.hover_color = hover_color
        self.current_color = base_color
        self.animation_speed = animation_speed
        self.is_hovered = False
        self.scale_factor = 1.0
        self.target_scale = 1.0
        self.text_input = text.split('\n')  # Split text into multiple lines
        self.font = pygame.font.Font(font_path, font_size)
        
        # Render text lines
        self.text_surfaces = [self.font.render(line, True, self.current_color) for line in self.text_input]
        self.text_rects = [surf.get_rect() for surf in self.text_surfaces]
        
        # If an image is provided, use its dimensions; otherwise, use text dimensions
        if self.image:
            self.original_image = self.image.copy()
            self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))
        else:
            width = max(rect.width for rect in self.text_rects)
            height = sum(rect.height for rect in self.text_rects)
            self.rect = pygame.Rect(self.x_pos, self.y_pos, width, height)
            
        self.original_rect = self.rect.copy()
        self.update_text_positions()

    def update_text_positions(self):
        '''Update text positions based on the current button rect.'''
        if len(self.text_rects) == 1:
            # If there's only one line, center it inside the button
            self.text_rects[0].center = self.rect.center
        else:
            y_offset = self.rect.top
            for rect in self.text_rects:
                rect.midtop = (self.rect.centerx, y_offset)
                y_offset += rect.height

    def update(self, screen, dt=1/60):
        '''Draw the button with animations.'''
        # Handle scaling animation
        if self.is_hovered and self.scale_factor < 1.1:
            self.scale_factor += self.animation_speed * dt
            if self.scale_factor > 1.1:
                self.scale_factor = 1.1
        elif not self.is_hovered and self.scale_factor > 1.0:
            self.scale_factor -= self.animation_speed * dt
            if self.scale_factor < 1.0:
                self.scale_factor = 1.0
                
        # Handle color animation
        if self.is_hovered:
            self.current_color = self.interpolate_color(self.current_color, self.hover_color, dt * self.animation_speed)
        else:
            self.current_color = self.interpolate_color(self.current_color, self.base_color, dt * self.animation_speed)
        
        # Update text with current color
        self.text_surfaces = [self.font.render(line, True, self.current_color) for line in self.text_input]
        
        # Apply scaling
        if self.image:
            width = int(self.original_image.get_width() * self.scale_factor)
            height = int(self.original_image.get_height() * self.scale_factor)
            scaled_image = pygame.transform.smoothscale(self.original_image, (width, height))
            
            # Keep the button centered at its original position while scaling
            new_rect = scaled_image.get_rect(center=self.original_rect.center)
            self.rect = new_rect
            screen.blit(scaled_image, self.rect)
        else:
            width = int(self.original_rect.width * self.scale_factor)
            height = int(self.original_rect.height * self.scale_factor)
            new_rect = pygame.Rect(0, 0, width, height)
            new_rect.center = self.original_rect.center
            self.rect = new_rect
        
        # Update text positions with the new rect
        self.update_text_positions()
        
        # Render text
        for surf, rect in zip(self.text_surfaces, self.text_rects):
            screen.blit(surf, rect)

    def interpolate_color(self, current_color, target_color, amount):
        '''Smoothly transition between colors.'''
        if isinstance(current_color, str) or isinstance(target_color, str):
            return target_color  # Skip interpolation if using named colors
            
        r = int(current_color[0] + (target_color[0] - current_color[0]) * amount)
        g = int(current_color[1] + (target_color[1] - current_color[1]) * amount)
        b = int(current_color[2] + (target_color[2] - current_color[2]) * amount)
        return max(0, min(r, 255)), max(0, min(g, 255)), max(0, min(b, 255))

    def checkInput(self, position):
        '''Check if the given position is within the button's bounds.'''
        return self.rect.collidepoint(position)

    def changeColor(self, position, hover_color=None):
        '''Handle hover state.'''
        was_hovered = self.is_hovered
        self.is_hovered = self.checkInput(position)
        
        if hover_color and self.is_hovered != was_hovered:
            # Update hover color if provided
            self.hover_color = hover_color