import pygame

grey = (38, 36, 36)
white = (242,242,242)
dark_brown = (74, 63, 54)
space_per_line = 200
space_per_box = 67
difficulty_levels = ['Easy', 'Medium', 'Hard']
space_between_buttons = 180
pygame.init()
header = pygame.font.Font('assets/MabryPro-Regular.ttf', 50) #header font and size being set
subheader = pygame.font.Font('assets/MabryPro-Regular.ttf',28) #subheader font and size being set
cell_font = pygame.font.Font('assets/MabryPro-Regular.ttf', 30) # Font for cell numbers
sketch_font = pygame.font.Font('assets/MabryPro-Regular.ttf', 20) # Font for sketched numbers
screen = pygame.display.set_mode((600,600))
current_screen = 'Main Menu'
