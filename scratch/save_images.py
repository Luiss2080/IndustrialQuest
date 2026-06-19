import os
import pygame

def main():
    pygame.init()
    # Create windowless surface for drawing
    pygame.display.set_mode((1, 1), pygame.NOFRAME)
    
    dest_dir = os.path.join("recursos", "imagenes")
    os.makedirs(dest_dir, exist_ok=True)
    
    # 1. corazon.png: Detailed pixel-art red heart
    surf_corazon = pygame.Surface((32, 32), pygame.SRCALPHA)
    # Circle left
    pygame.draw.circle(surf_corazon, (220, 35, 35), (10, 11), 8)
    # Circle right
    pygame.draw.circle(surf_corazon, (220, 35, 35), (22, 11), 8)
    # Triangle bottom
    pygame.draw.polygon(surf_corazon, (220, 35, 35), [(2, 13), (30, 13), (16, 27)])
    # Inner shadow (depth)
    pygame.draw.circle(surf_corazon, (160, 20, 20), (10, 13), 6)
    pygame.draw.circle(surf_corazon, (160, 20, 20), (22, 13), 6)
    pygame.draw.polygon(surf_corazon, (160, 20, 20), [(4, 14), (28, 14), (16, 25)])
    # White highlight pixel-art
    pygame.draw.rect(surf_corazon, (255, 255, 255), (7, 7, 4, 4), border_radius=1)
    pygame.draw.rect(surf_corazon, (255, 255, 255), (19, 7, 4, 4), border_radius=1)
    pygame.image.save(surf_corazon, os.path.join(dest_dir, "corazon.png"))
    print("Saved corazon.png")

    # 2. estrella.png: Gold star
    surf_estrella = pygame.Surface((32, 32), pygame.SRCALPHA)
    puntos = [
        (16, 2), (20, 11), (30, 11), (22, 18),
        (25, 28), (16, 22), (7, 28), (10, 18),
        (2, 11), (12, 11)
    ]
    pygame.draw.polygon(surf_estrella, (255, 215, 0), puntos) # Gold
    pygame.draw.polygon(surf_estrella, (180, 140, 10), puntos, 2) # Bronze border
    # Highlight
    pygame.draw.circle(surf_estrella, (255, 255, 200), (16, 14), 4)
    pygame.image.save(surf_estrella, os.path.join(dest_dir, "estrella.png"))
    print("Saved estrella.png")

    # 3. Boton.png: Textured wood button
    surf_boton = pygame.Surface((200, 50))
    surf_boton.fill((160, 110, 65))
    pygame.draw.rect(surf_boton, (90, 55, 30), (0, 0, 200, 50), 3) # Outer dark wood border
    # Clavos (screws/rivets in corners)
    pygame.draw.circle(surf_boton, (80, 80, 80), (8, 8), 3)
    pygame.draw.circle(surf_boton, (80, 80, 80), (192, 8), 3)
    pygame.draw.circle(surf_boton, (80, 80, 80), (8, 42), 3)
    pygame.draw.circle(surf_boton, (80, 80, 80), (192, 42), 3)
    pygame.image.save(surf_boton, os.path.join(dest_dir, "Boton.png"))
    print("Saved Boton.png")
    
    pygame.quit()

if __name__ == "__main__":
    main()
