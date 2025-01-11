import pygame
import sys
import time
from typing import Tuple, Dict
from .snake import Snake
from .food import Food
import os
import json

class Game:
    def __init__(self, width: int = 800, height: int = 600):
        pygame.mixer.init()  # Ses sistemini başlat
        self.width = width
        self.height = height
        self.block_size = 20
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Yılan Oyunu - Klasik Mod")
        
        # Skor dosyası
        self.score_file = "data/highscore.json"
        os.makedirs(os.path.dirname(self.score_file), exist_ok=True)
        
        # En yüksek skoru yükle
        self.best_score = self.load_best_score()
        
        # Ses efektlerini yükle
        self.sounds_dir = "assets/sounds"
        os.makedirs(self.sounds_dir, exist_ok=True)
        
        # Varsayılan ses dosyalarını oluştur
        self.create_default_sounds()
        
        # Ses efektlerini yükle
        self.eat_sound = pygame.mixer.Sound(os.path.join(self.sounds_dir, "eat.wav"))
        self.crash_sound = pygame.mixer.Sound(os.path.join(self.sounds_dir, "crash.wav"))
        self.move_sound = pygame.mixer.Sound(os.path.join(self.sounds_dir, "move.wav"))
        
        # Ses seviyelerini ayarla
        self.eat_sound.set_volume(0.5)
        self.crash_sound.set_volume(0.3)
        self.move_sound.set_volume(0.1)
        
        # Ses durumu
        self.sound_enabled = True
        
        # Modern renk paleti
        self.BACKGROUND_COLOR = (17, 24, 39)  # Koyu lacivert
        self.TEXT_COLOR = (243, 244, 246)  # Açık gri
        self.GAME_OVER_COLOR = (239, 68, 68)  # Parlak kırmızı
        self.PAUSE_COLOR = (245, 158, 11)  # Turuncu
        self.WINDOW_COLOR = (31, 41, 55)  # Koyu gri-mavi
        self.BUTTON_COLOR = (16, 185, 129)  # Yeşil
        self.BUTTON_HOVER_COLOR = (5, 150, 105)  # Koyu yeşil
        self.SNAKE_COLOR = (52, 211, 153)  # Açık yeşil
        self.FOOD_COLOR = (248, 113, 113)  # Açık kırmızı
        self.BORDER_COLOR = (75, 85, 99)  # Gri
        
        # Yön tuşları
        self.direction_map = {
            pygame.K_UP: [0, -self.block_size],
            pygame.K_DOWN: [0, self.block_size],
            pygame.K_LEFT: [-self.block_size, 0],
            pygame.K_RIGHT: [self.block_size, 0],
            # WASD tuşları
            pygame.K_w: [0, -self.block_size],
            pygame.K_s: [0, self.block_size],
            pygame.K_a: [-self.block_size, 0],
            pygame.K_d: [self.block_size, 0]
        }
        
        # Oyun değişkenleri
        self.clock = pygame.time.Clock()
        
        # Ayarları yükle
        self.settings = self.load_settings()
        self.fps = self.settings.get('classic_fps', 10)  # Varsayılan 10 FPS
        
        # Oyunu başlat
        self.reset_game()

    def create_default_sounds(self):
        """Varsayılan ses dosyalarını oluştur"""
        import wave
        import struct
        import numpy as np
        
        # Yem yeme sesi (yüksek tonlu bip)
        if not os.path.exists(os.path.join(self.sounds_dir, "eat.wav")):
            samplerate = 44100
            duration = 0.1  # saniye
            frequency = 1000  # Hz
            t = np.linspace(0, duration, int(samplerate * duration))
            data = np.sin(2 * np.pi * frequency * t) * 32767
            data = data.astype(np.int16)
            
            with wave.open(os.path.join(self.sounds_dir, "eat.wav"), 'wb') as f:
                f.setnchannels(1)
                f.setsampwidth(2)
                f.setframerate(samplerate)
                f.writeframes(data.tobytes())
        
        # Çarpışma sesi (düşük tonlu bip)
        if not os.path.exists(os.path.join(self.sounds_dir, "crash.wav")):
            samplerate = 44100
            duration = 0.2  # saniye
            frequency = 500  # Hz
            t = np.linspace(0, duration, int(samplerate * duration))
            data = np.sin(2 * np.pi * frequency * t) * 32767
            data = data.astype(np.int16)
            
            with wave.open(os.path.join(self.sounds_dir, "crash.wav"), 'wb') as f:
                f.setnchannels(1)
                f.setsampwidth(2)
                f.setframerate(samplerate)
                f.writeframes(data.tobytes())
        
        # Hareket sesi (çok kısa bip)
        if not os.path.exists(os.path.join(self.sounds_dir, "move.wav")):
            samplerate = 44100
            duration = 0.05  # saniye
            frequency = 800  # Hz
            t = np.linspace(0, duration, int(samplerate * duration))
            data = np.sin(2 * np.pi * frequency * t) * 16383  # Daha düşük ses seviyesi
            data = data.astype(np.int16)
            
            with wave.open(os.path.join(self.sounds_dir, "move.wav"), 'wb') as f:
                f.setnchannels(1)
                f.setsampwidth(2)
                f.setframerate(samplerate)
                f.writeframes(data.tobytes())

    def reset_game(self) -> None:
        """Oyunu başlangıç durumuna getirir"""
        # Oyun nesnelerini oluştur
        start_pos = (self.width // 2, self.height // 2)
        self.snake = Snake(start_pos, self.block_size)
        self.snake.direction = [0, 0]  # Başlangıçta hareket etmesin
        self.food = Food(self.width, self.height, self.block_size)
        
        # Oyun değişkenleri
        self.score = 0
        self.game_over = False
        self.paused = False
        self.start_time = None
        self.elapsed_time = 0
        self.game_started = False

    def load_settings(self, settings: dict = None) -> dict:
        """Ayarları yükler"""
        if settings is not None:
            # Ses ayarlarını güncelle
            self.sound_enabled = settings.get('classic_sound_enabled', True)
            self.eat_sound.set_volume(settings.get('eat_sound_volume', 0.5))
            self.crash_sound.set_volume(settings.get('crash_sound_volume', 0.3))
            self.move_sound.set_volume(settings.get('move_sound_volume', 0.1))
            # FPS ayarını güncelle
            self.fps = settings.get('classic_fps', 10)
            return settings
            
        # Ayarlar verilmediyse dosyadan oku
        settings_file = "data/settings.json"
        try:
            with open(settings_file, 'r') as f:
                settings = json.load(f)
                self.sound_enabled = settings.get('classic_sound_enabled', True)
                self.eat_sound.set_volume(settings.get('eat_sound_volume', 0.5))
                self.crash_sound.set_volume(settings.get('crash_sound_volume', 0.3))
                self.move_sound.set_volume(settings.get('move_sound_volume', 0.1))
                self.fps = settings.get('classic_fps', 10)
                return settings
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                'classic_fps': 10,  # Varsayılan FPS
                'classic_sound_enabled': True,
                'eat_sound_volume': 0.5,
                'crash_sound_volume': 0.3,
                'move_sound_volume': 0.1
            }

    def play_sound(self, sound: pygame.mixer.Sound) -> None:
        """Ses efektini çal"""
        if self.sound_enabled:
            sound.play()

    def handle_input(self) -> str:
        """Kullanıcı girdilerini işler"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_best_score()  # Çıkmadan önce skoru kaydet
                return 'QUIT'
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.save_best_score()  # Menüye dönmeden önce skoru kaydet
                    return 'MENU'
                elif event.key == pygame.K_q:  # Q tuşu ile çıkış
                    self.save_best_score()
                    return 'QUIT'
                elif event.key == pygame.K_SPACE:  # SPACE tuşu ile duraklat/devam et
                    self.paused = not self.paused
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                elif event.key == pygame.K_m:  # Ses açma/kapama
                    self.sound_enabled = not self.sound_enabled
                elif not self.game_over and not self.paused:
                    old_direction = self.snake.direction
                    if event.key == pygame.K_UP and self.snake.direction != [0, self.block_size]:
                        self.snake.direction = [0, -self.block_size]
                    elif event.key == pygame.K_DOWN and self.snake.direction != [0, -self.block_size]:
                        self.snake.direction = [0, self.block_size]
                    elif event.key == pygame.K_LEFT and self.snake.direction != [self.block_size, 0]:
                        self.snake.direction = [-self.block_size, 0]
                    elif event.key == pygame.K_RIGHT and self.snake.direction != [-self.block_size, 0]:
                        self.snake.direction = [self.block_size, 0]
                    elif event.key == pygame.K_w and self.snake.direction != [0, self.block_size]:
                        self.snake.direction = [0, -self.block_size]
                    elif event.key == pygame.K_s and self.snake.direction != [0, -self.block_size]:
                        self.snake.direction = [0, self.block_size]
                    elif event.key == pygame.K_a and self.snake.direction != [self.block_size, 0]:
                        self.snake.direction = [-self.block_size, 0]
                    elif event.key == pygame.K_d and self.snake.direction != [-self.block_size, 0]:
                        self.snake.direction = [self.block_size, 0]
                    
                    # Yön değiştiyse hareket sesi çal
                    if old_direction != self.snake.direction:
                        self.play_sound(self.move_sound)
            
            # Oyun sonu ekranındaki butonlar için tıklama olayları
            if event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
                mouse_pos = pygame.mouse.get_pos()
                
                # Buton boyutları (draw_game_over_window metodundan)
                button_width = 320  # content_width - 40
                button_height = 50
                button_spacing = 20
                window_height = 400
                window_y = self.height//2 - window_height//2
                padding = 30
                
                button_start_y = window_y + window_height - (2 * button_height + button_spacing + padding)
                
                # Yeniden Oyna butonu için dikdörtgen
                replay_button = pygame.Rect(
                    self.width//2 - button_width//2,
                    button_start_y,
                    button_width,
                    button_height
                )
                
                # Menüye Dön butonu için dikdörtgen
                menu_button = pygame.Rect(
                    self.width//2 - button_width//2,
                    button_start_y + button_height + button_spacing,
                    button_width,
                    button_height
                )
                
                if replay_button.collidepoint(mouse_pos):
                    self.reset_game()
                elif menu_button.collidepoint(mouse_pos):
                    self.save_best_score()
                    return 'MENU'
        
        return None

    def update(self) -> None:
        """Oyun durumunu günceller"""
        if self.game_over or self.paused:
            return
        
        # Yılanı güncelle
        self.snake.update()
        
        # Çarpışma kontrolü
        if self.snake.check_collision(self.width, self.height):
            self.play_sound(self.crash_sound)
            self.game_over = True
            return
        
        # Yem yeme kontrolü
        if self.snake.body[0] == self.food.position:
            self.play_sound(self.eat_sound)
            self.score += 1
            if self.score > self.best_score:
                self.best_score = self.score
            self.snake.grow_snake()
            self.food.respawn(self.snake.body)
        
        # Zamanı güncelle
        if not self.start_time:
            self.start_time = time.time()
        self.elapsed_time = int(time.time() - self.start_time)

    def draw_game_over_window(self) -> None:
        """Oyun sonu penceresini çizer"""
        # Yarı saydam siyah arka plan
        s = pygame.Surface((self.width, self.height))
        s.set_alpha(160)
        s.fill((0, 0, 0))
        self.screen.blit(s, (0, 0))
        
        # Pencere boyutları
        window_width = 400
        window_height = 400  # Yüksekliği biraz daha artırdık
        window_x = self.width//2 - window_width//2
        window_y = self.height//2 - window_height//2
        
        # Pencere arka planı ve çerçevesi
        pygame.draw.rect(self.screen, self.WINDOW_COLOR, 
                        (window_x, window_y, window_width, window_height),
                        border_radius=10)  # Köşeleri yuvarladık
        pygame.draw.rect(self.screen, self.BORDER_COLOR, 
                        (window_x, window_y, window_width, window_height), 2,
                        border_radius=10)
        
        # İç kısım için padding
        padding = 30
        content_width = window_width - (padding * 2)
        
        # Başlık
        title_font = pygame.font.Font(None, 64)
        title = title_font.render('OYUN BİTTİ!', True, self.GAME_OVER_COLOR)
        title_rect = title.get_rect(center=(self.width//2, window_y + 60))
        self.screen.blit(title, title_rect)
        
        # Skor ve süre
        font = pygame.font.Font(None, 48)
        messages = [
            f'Skor: {self.score}',
            f'Süre: {self.elapsed_time} saniye'
        ]
        
        for i, message in enumerate(messages):
            text = font.render(message, True, self.TEXT_COLOR)
            text_rect = text.get_rect(center=(self.width//2, window_y + 140 + i * 50))
            self.screen.blit(text, text_rect)
        
        # Butonlar
        button_width = content_width - 40  # Buton genişliğini pencereye göre ayarla
        button_height = 50
        button_spacing = 20
        button_start_y = window_y + window_height - (2 * button_height + button_spacing + padding)
        
        buttons = {
            'Yeniden Oyna (R)': button_start_y,
            'Menüye Dön (ESC)': button_start_y + button_height + button_spacing
        }
        
        mouse_pos = pygame.mouse.get_pos()
        for text, y in buttons.items():
            button_rect = pygame.Rect(self.width//2 - button_width//2, y, button_width, button_height)
            color = self.BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else self.BUTTON_COLOR
            
            # Buton gölgesi
            shadow_rect = button_rect.copy()
            shadow_rect.y += 2
            pygame.draw.rect(self.screen, (0, 0, 0, 50), shadow_rect, border_radius=5)
            
            # Buton
            pygame.draw.rect(self.screen, color, button_rect, border_radius=5)
            pygame.draw.rect(self.screen, self.BORDER_COLOR, button_rect, 2, border_radius=5)
            
            # Buton metni
            text_surface = font.render(text, True, self.TEXT_COLOR)
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)

    def draw(self) -> None:
        """Oyunu ekrana çizer"""
        # Arka planı temizle
        self.screen.fill(self.BACKGROUND_COLOR)
        
        # Yılan ve yemi çiz
        self.snake.draw(self.screen, self.SNAKE_COLOR)  # Yılan rengini geçir
        self.food.draw(self.screen, self.FOOD_COLOR)    # Yem rengini geçir
        
        # Font ayarla
        font = pygame.font.Font(None, 36)
        
        # En yüksek skoru sol üstte göster
        best_score_text = font.render(f'En Yüksek Skor: {self.best_score}', True, self.TEXT_COLOR)
        self.screen.blit(best_score_text, (20, 20))
        
        # Mevcut skoru en yüksek skorun altında göster
        score_text = font.render(f'Skor: {self.score}', True, self.TEXT_COLOR)
        self.screen.blit(score_text, (20, 60))
        
        # Sağ üstte süreyi göster
        time_text = font.render(f'Süre: {self.elapsed_time}s', True, self.TEXT_COLOR)
        time_rect = time_text.get_rect()
        time_rect.right = self.width - 20
        time_rect.top = 20
        self.screen.blit(time_text, time_rect)
        
        # Başlangıç mesajını sadece oyun başlamadan önce göster
        if not self.game_started and self.snake.direction == [0, 0]:
            start_text = font.render('Başlamak için bir yön tuşuna basın', True, self.TEXT_COLOR)
            start_rect = start_text.get_rect(center=(self.width//2, self.height//2))
            self.screen.blit(start_text, start_rect)
        
        # Oyun durumu mesajları
        if self.game_over:
            self.draw_game_over_window()
        elif self.paused:
            s = pygame.Surface((self.width, self.height))
            s.set_alpha(128)
            s.fill((0, 0, 0))
            self.screen.blit(s, (0, 0))
            
            pause_text = font.render('OYUN DURAKLATILDI - SPACE ile Devam Et', True, self.PAUSE_COLOR)
            text_rect = pause_text.get_rect(center=(self.width/2, self.height/2))
            self.screen.blit(pause_text, text_rect)
        
        pygame.display.flip()

    def run(self) -> str:
        """Oyun döngüsünü çalıştırır"""
        while True:
            # Ayarları yeniden yükle
            settings_file = "data/settings.json"
            try:
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
                    self.fps = settings.get('classic_fps', 10)
                    self.sound_enabled = settings.get('classic_sound_enabled', True)
                    self.eat_sound.set_volume(settings.get('eat_sound_volume', 0.5))
                    self.crash_sound.set_volume(settings.get('crash_sound_volume', 0.3))
                    self.move_sound.set_volume(settings.get('move_sound_volume', 0.1))
            except (FileNotFoundError, json.JSONDecodeError):
                pass
            
            if not self.paused:
                self.update()
            
            self.draw()
            action = self.handle_input()
            
            if action:
                return action
            
            self.clock.tick(self.fps)  # FPS'i ayarlardan al

    def load_best_score(self) -> int:
        """En yüksek skoru yükle"""
        if os.path.exists(self.score_file):
            try:
                with open(self.score_file, 'r') as f:
                    data = json.load(f)
                    return data.get('best_score', 0)
            except:
                pass
        return 0

    def save_best_score(self) -> None:
        """En yüksek skoru kaydet"""
        with open(self.score_file, 'w') as f:
            json.dump({'best_score': self.best_score}, f) 