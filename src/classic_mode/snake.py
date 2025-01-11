from typing import List, Tuple
import pygame
import random

class Snake:
    def __init__(self, start_pos: Tuple[int, int], block_size: int = 20):
        self.block_size = block_size
        self.body = [start_pos]  # Yılanın vücut parçalarının pozisyonları
        self.direction = [block_size, 0]  # Başlangıçta sağa doğru hareket
        self.grow = False

    def update(self) -> None:
        """Yılanın pozisyonunu günceller"""
        new_head = (
            self.body[0][0] + self.direction[0],
            self.body[0][1] + self.direction[1]
        )
        
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        self.grow = False

    def grow_snake(self) -> None:
        """Yılanın uzamasını sağlar"""
        self.grow = True

    def change_direction(self, new_direction: List[int]) -> None:
        """Yılanın yönünü değiştirir"""
        # Zıt yöne gitmeyi engelle
        if (new_direction[0] != -self.direction[0] or new_direction[0] == 0) and \
           (new_direction[1] != -self.direction[1] or new_direction[1] == 0):
            self.direction = new_direction

    def check_collision(self, width: int, height: int) -> bool:
        """Duvarlar ve kendi vücuduyla çarpışma kontrolü"""
        head = self.body[0]
        
        # Duvarlarla çarpışma kontrolü
        if head[0] < 0 or head[0] >= width or head[1] < 0 or head[1] >= height:
            return True
            
        # Kendi vücuduyla çarpışma kontrolü
        if head in self.body[1:]:
            return True
            
        return False

    def draw(self, screen: pygame.Surface, color: Tuple[int, int, int] = (0, 255, 0)) -> None:
        """Yılanı ekrana çizer"""
        for i, segment in enumerate(self.body):
            # Baş kısmı için daha koyu bir renk kullan
            segment_color = (
                max(0, color[0] - 20),
                max(0, color[1] - 20),
                max(0, color[2] - 20)
            ) if i == 0 else color
            
            pygame.draw.rect(
                screen,
                segment_color,
                pygame.Rect(
                    segment[0],
                    segment[1],
                    self.block_size - 2,  # Bloklar arası boşluk için -2
                    self.block_size - 2
                ),
                border_radius=3  # Yuvarlatılmış köşeler
            ) 