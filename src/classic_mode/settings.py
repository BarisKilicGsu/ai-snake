import pygame
import json
import os
from typing import Dict

class Settings:
    def __init__(self, width: int = 800, height: int = 600):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Yılan Oyunu - Ayarlar")
        
        # Renkler
        self.BACKGROUND_COLOR = (17, 24, 39)  # Koyu lacivert
        self.TEXT_COLOR = (243, 244, 246)  # Açık gri
        self.SLIDER_COLOR = (16, 185, 129)  # Yeşil
        self.SLIDER_BG_COLOR = (75, 85, 99)  # Gri
        self.BUTTON_COLOR = (16, 185, 129)  # Yeşil
        self.BUTTON_HOVER_COLOR = (5, 150, 105)  # Koyu yeşil
        
        # Ayarlar dosyası
        self.settings_file = "data/settings.json"
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        
        # Varsayılan ayarlar
        self.default_settings = {
            'eat_sound_volume': 0.5,
            'crash_sound_volume': 0.3,
            'move_sound_volume': 0.1,
            'classic_sound_enabled': True,
            'ai_sound_enabled': True,
            'classic_fps': 10  # Klasik mod için varsayılan FPS
        }
        
        # Ayarları yükle
        self.settings = self.load_settings()
        
        # Slider özellikleri
        self.slider_width = 200
        self.slider_height = 10
        self.button_radius = 10
        self.active_slider = None
        
        # Font
        self.font = pygame.font.Font(None, 36)

    def load_settings(self) -> Dict:
        """Ayarları yükle"""
        settings = self.default_settings.copy()
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    saved_settings = json.load(f)
                    # Mevcut ayarları güncelle, eksik olanları varsayılan değerlerle bırak
                    settings.update(saved_settings)
            except:
                pass
        return settings

    def save_settings(self) -> None:
        """Ayarları kaydet"""
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f)

    def draw_slider(self, x: int, y: int, value: float, label: str) -> pygame.Rect:
        """Slider çizer ve dikdörtgenini döndürür"""
        # Etiketi çiz
        text = self.font.render(label, True, self.TEXT_COLOR)
        text_rect = text.get_rect(x=x, y=y)
        self.screen.blit(text, text_rect)
        
        # Slider arka planı
        slider_rect = pygame.Rect(x, y + 30, self.slider_width, self.slider_height)
        pygame.draw.rect(self.screen, self.SLIDER_BG_COLOR, slider_rect)
        
        # Slider değeri
        value = max(0.0, min(1.0, value))  # Değeri 0-1 arasında sınırla
        filled_width = max(0, min(int(self.slider_width * value), self.slider_width))
        if filled_width > 0:  # Sadece pozitif genişlik varsa çiz
            filled_rect = pygame.Rect(x, y + 30, filled_width, self.slider_height)
            pygame.draw.rect(self.screen, self.SLIDER_COLOR, filled_rect)
        
        # Slider düğmesi
        button_x = x + filled_width
        button_x = max(x, min(button_x, x + self.slider_width))
        button_y = y + 30 + self.slider_height//2
        pygame.draw.circle(self.screen, self.SLIDER_COLOR, (int(button_x), int(button_y)), self.button_radius)
        
        # Değeri göster
        if label == "Klasik Mod FPS":
            fps_value = int(value * 55 + 5)  # 5-60 FPS aralığı
            fps_value = max(5, min(60, fps_value))  # FPS değerini sınırla
            value_text = self.font.render(f"{fps_value}", True, self.TEXT_COLOR)
        else:
            value_text = self.font.render(f"{int(value * 100)}%", True, self.TEXT_COLOR)
        value_text_rect = value_text.get_rect(x=x + self.slider_width + 20, centery=y + 30 + self.slider_height//2)
        self.screen.blit(value_text, value_text_rect)
        
        return slider_rect

    def handle_slider(self, pos: tuple, rect: pygame.Rect, name: str) -> None:
        """Slider değerini günceller"""
        if rect.collidepoint(pos):
            # Mouse pozisyonunu slider sınırları içinde tut
            x = max(rect.left, min(pos[0], rect.right))
            
            # Değeri 0-1 aralığında hesapla
            value = (x - rect.left) / self.slider_width
            value = max(0, min(1, value))
            
            if name == 'classic_fps':
                # FPS değerini 5-60 aralığında tut
                fps = int(value * 55 + 5)
                fps = max(5, min(60, fps))
                # FPS değerini tekrar 0-1 aralığına dönüştür
                value = (fps - 5) / 55
            
            self.settings[name] = value

    def run(self) -> str:
        """Ayarlar menüsünü çalıştırır"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            slider_rects = {}
            self.screen.fill(self.BACKGROUND_COLOR)
            
            # Başlık
            title = self.font.render("Ses Ayarları", True, self.TEXT_COLOR)
            title_rect = title.get_rect(center=(self.width/2, 50))
            self.screen.blit(title, title_rect)
            
            # Sliderları çiz
            y_start = 100  # Başlangıç y pozisyonunu yukarı çektik
            y_spacing = 70  # Elemanlar arası boşluğu azalttık
            
            slider_rects['eat_sound_volume'] = self.draw_slider(
                self.width//2 - self.slider_width//2, y_start, 
                self.settings['eat_sound_volume'], "Yem Sesi")
            
            slider_rects['crash_sound_volume'] = self.draw_slider(
                self.width//2 - self.slider_width//2, y_start + y_spacing, 
                self.settings['crash_sound_volume'], "Çarpışma Sesi")
            
            slider_rects['move_sound_volume'] = self.draw_slider(
                self.width//2 - self.slider_width//2, y_start + y_spacing * 2, 
                self.settings['move_sound_volume'], "Hareket Sesi")
            
            # Klasik Mod FPS ayarı
            fps_value = (self.settings.get('classic_fps', 10) - 5) / 55  # 5-60 FPS aralığını 0-1'e dönüştür
            slider_rects['classic_fps'] = self.draw_slider(
                self.width//2 - self.slider_width//2, y_start + y_spacing * 3,
                fps_value, "Klasik Mod FPS")
            
            # Butonlar için y pozisyonları
            button_y_start = y_start + y_spacing * 4
            button_spacing = 60
            
            # Klasik Mod ses açma/kapama butonu
            classic_sound_text = f"Klasik Mod Ses: {'Açık' if self.settings['classic_sound_enabled'] else 'Kapalı'}"
            classic_sound_button = pygame.Rect(self.width//2 - 150, button_y_start, 300, 40)
            pygame.draw.rect(self.screen, self.BUTTON_COLOR, classic_sound_button)
            text = self.font.render(classic_sound_text, True, self.TEXT_COLOR)
            text_rect = text.get_rect(center=classic_sound_button.center)
            self.screen.blit(text, text_rect)
            
            # AI Mod ses açma/kapama butonu
            ai_sound_text = f"AI Mod Ses: {'Açık' if self.settings['ai_sound_enabled'] else 'Kapalı'}"
            ai_sound_button = pygame.Rect(self.width//2 - 150, button_y_start + button_spacing, 300, 40)
            pygame.draw.rect(self.screen, self.BUTTON_COLOR, ai_sound_button)
            text = self.font.render(ai_sound_text, True, self.TEXT_COLOR)
            text_rect = text.get_rect(center=ai_sound_button.center)
            self.screen.blit(text, text_rect)
            
            # Geri dön butonu
            back_button = pygame.Rect(self.width//2 - 100, button_y_start + button_spacing * 2, 200, 40)
            pygame.draw.rect(self.screen, self.BUTTON_COLOR, back_button)
            text = self.font.render("Geri Dön", True, self.TEXT_COLOR)
            text_rect = text.get_rect(center=back_button.center)
            self.screen.blit(text, text_rect)
            
            pygame.display.flip()
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_settings()
                    return "QUIT"
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Sol tık
                        if classic_sound_button.collidepoint(event.pos):
                            self.settings['classic_sound_enabled'] = not self.settings['classic_sound_enabled']
                        elif ai_sound_button.collidepoint(event.pos):
                            self.settings['ai_sound_enabled'] = not self.settings['ai_sound_enabled']
                        elif back_button.collidepoint(event.pos):
                            self.save_settings()
                            return "MENU"
                        else:
                            # Slider kontrolü
                            for name, rect in slider_rects.items():
                                if rect.collidepoint(event.pos):
                                    self.active_slider = name
                                    self.handle_slider(event.pos, rect, name)
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Sol tık
                        self.active_slider = None
                
                elif event.type == pygame.MOUSEMOTION:
                    # Aktif slider varsa güncelle
                    if self.active_slider and self.active_slider in slider_rects:
                        self.handle_slider(event.pos, slider_rects[self.active_slider], self.active_slider)
                        if self.active_slider == 'classic_fps':
                            # FPS değerini 5-60 aralığına dönüştür
                            self.settings['classic_fps'] = int(self.settings[self.active_slider] * 55 + 5)
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.save_settings()
                        return "MENU"
            
            clock.tick(60)
        
        return None 