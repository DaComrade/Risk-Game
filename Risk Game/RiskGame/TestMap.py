import pygame

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
window_width = 1600
window_height = 1062
window = pygame.display.set_mode((window_width, window_height))

# Set the title of the window
pygame.display.set_caption("Risk Game")

# Load the world map image
map_image_path = r'C:\Users\willi\Downloads\RiskMap.jpg'
map_image = pygame.image.load(map_image_path)
map_image = pygame.transform.scale(map_image, (window_width, window_height))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Print the coordinates of the mouse click
            print(pygame.mouse.get_pos())

    # Draw the map
    window.blit(map_image, (0, 0))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()