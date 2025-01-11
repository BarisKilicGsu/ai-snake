from typing import List, Tuple
import pygame
import random

class Food:
    def __init__(self, width: int, height: int, block_size: int = 20):
        self.block_size = block_size
        self.width = width
        self.height = height
        self.position = self.generate_position()

    def generate_position(self) -> Tuple[int, int]:
        """Yem için random pozisyon oluşturur"""
        x = random.randrange(0, self.width, self.block_size)
        y = random.randrange(0, self.height, self.block_size)
        return (x, y)

    def respawn(self, snake_body: List[Tuple[int, int]]) -> None:
        """Yemi yeni bir konuma taşır (yılanın üzerine gelmeyecek şekilde)"""
        while True:
            new_pos = self.generate_position()
            if new_pos not in snake_body:
                self.position = new_pos
                break

    def draw(self, screen: pygame.Surface, color: Tuple[int, int, int] = (255, 0, 0)) -> None:
        """Yemi ekrana çizer"""
        # Ana yem şekli
        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(
                self.position[0],
                self.position[1],
                self.block_size - 2,
                self.block_size - 2
            ),
            border_radius=5  # Yuvarlatılmış köşeler
        )
        
        # Parlama efekti (daha açık renk)
        highlight_color = (
            min(255, color[0] + 50),
            min(255, color[1] + 50),
            min(255, color[2] + 50)
        )
        pygame.draw.circle(
            screen,
            highlight_color,
            (self.position[0] + 5, self.position[1] + 5),
            2
        ) 