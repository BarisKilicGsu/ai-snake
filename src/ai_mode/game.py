import pygame
import sys
import time
import os
import json
from typing import Tuple, Dict
from src.classic_mode.snake import Snake
from src.classic_mode.food import Food
from .dqn_agent import DQNAgent

class AIGame:
    def __init__(self, width: int = 800, height: int = 600):
        pygame.mixer.init()  # Ses sistemini başlat
        self.width = width
        self.height = height
        self.block_size = 20
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Yılan Oyunu - AI Modu")
        
        # Oyun hızı ayarları
        self.speed = 10  # Başlangıç hızı
        self.min_speed = 5  # Minimum hız
        self.max_speed = 120  # Maksimum hız
        self.current_fps = self.speed  # Mevcut FPS
        
        # Ses efektlerini yükle
        self.sounds_dir = "assets/sounds"
        os.makedirs(self.sounds_dir, exist_ok=True)
        
        # Varsayılan ses dosyaları oluştur
        self.create_default_sounds()
        
        # Ses efektlerini yükle
        self.eat_sound = pygame.mixer.Sound(os.path.join(self.sounds_dir, "eat.wav"))
        self.crash_sound = pygame.mixer.Sound(os.path.join(self.sounds_dir, "crash.wav"))
        self.move_sound = pygame.mixer.Sound(os.path.join(self.sounds_dir, "move.wav"))
        
        # Ayarları yükle
        self.settings = self.load_settings()
        self.sound_enabled = self.settings.get('ai_sound_enabled', True)
        self.eat_sound.set_volume(self.settings.get('eat_sound_volume', 0.5))
        self.crash_sound.set_volume(self.settings.get('crash_sound_volume', 0.3))
        self.move_sound.set_volume(self.settings.get('move_sound_volume', 0.1))
        
        # Modern renk paleti (klasik mod ile aynı)
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
        
        # AI ajanını oluştur
        self.state_size = 12  # 4 yön + 4 yemek konumu + 4 tehlike
        self.action_size = 4  # Yukarı, Aşağı, Sol, Sağ
        self.agent = DQNAgent(self.state_size, self.action_size)
        
        # Model ve eğitim verilerinin yolları
        self.models_dir = "models"
        os.makedirs(self.models_dir, exist_ok=True)
        self.model_path = os.path.join(self.models_dir, "snake_ai_model.pth")
        self.training_data_path = os.path.join(self.models_dir, "training_data.json")
        
        # Eğitim verilerini yükle
        self.training_data = self.load_training_data()
        self.best_score = self.training_data['best_score']  # En iyi skoru yükle
        
        # Model dosyası varsa yükle
        if os.path.exists(self.model_path):
            self.agent.load(self.model_path)
        
        self.reset_game()
        
        # Yön haritası (AI aksiyonları için)
        self.action_map = {
            0: [0, -self.block_size],  # Yukarı
            1: [0, self.block_size],   # Aşağı
            2: [-self.block_size, 0],  # Sol
            3: [self.block_size, 0]    # Sağ
        }

    def reset_game(self) -> None:
        """Oyunu başlangıç durumuna getirir"""
        start_pos = (self.width // 2, self.height // 2)
        self.snake = Snake(start_pos, self.block_size)
        self.food = Food(self.width, self.height, self.block_size)
        
        self.score = 0
        self.paused = False
        self.training = True
        self.clock = pygame.time.Clock()
        self.start_time = time.time()
        self.elapsed_time = 0
        self.episode_rewards = 0
        self.total_episodes = 0  # Bu sayaç her oyun başladığında sıfırlanacak

    def load_training_data(self) -> Dict:
        """Eğitim verilerini yükle"""
        if os.path.exists(self.training_data_path):
            try:
                with open(self.training_data_path, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            'total_episodes': 0,
            'best_score': 0,
            'average_scores': [],
            'training_time': 0
        }

    def save_training_data(self) -> None:
        """Eğitim verilerini kaydet"""
        current_data = {
            'total_episodes': self.training_data['total_episodes'] + self.total_episodes,
            'best_score': max(self.training_data['best_score'], self.best_score),
            'average_scores': self.training_data['average_scores'] + [self.score],
            'training_time': self.training_data['training_time'] + self.elapsed_time
        }
        
        with open(self.training_data_path, 'w') as f:
            json.dump(current_data, f)

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

    def play_sound(self, sound: pygame.mixer.Sound) -> None:
        """Ses efektini çal"""
        if self.sound_enabled:
            sound.play()

    def handle_input(self) -> str:
        """Kullanıcı girdilerini işler"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'QUIT'
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'MENU'
                elif event.key == pygame.K_q:  # Q tuşu ile çıkış
                    return 'QUIT'
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_m:  # Ses açma/kapama
                    self.sound_enabled = not self.sound_enabled
                elif event.key == pygame.K_UP:  # Hızı artır
                    self.speed = min(self.speed + 5, self.max_speed)
                elif event.key == pygame.K_DOWN:  # Hızı azalt
                    self.speed = max(self.speed - 5, self.min_speed)
        
        return None

    def update(self) -> None:
        """Oyun durumunu günceller"""
        if self.paused:
            return

        # Mevcut durumu al
        state = self.agent.get_state(
            self.snake.body[0],
            self.snake.body,
            self.food.position,
            self.width,
            self.height
        )
        
        # AI'nin aksiyonunu al
        action = self.agent.act(state, self.training)
        
        # Yılanın yönünü değiştir
        old_direction = self.snake.direction
        self.snake.direction = self.action_map[action]
        
        # Yön değiştiyse hareket sesi çal
        if old_direction != self.snake.direction:
            self.play_sound(self.move_sound)
        
        # Önceki pozisyonu kaydet
        old_distance = ((self.snake.body[0][0] - self.food.position[0])**2 + 
                       (self.snake.body[0][1] - self.food.position[1])**2)**0.5
        
        # Yılanı güncelle
        self.snake.update()
        
        # Yeni pozisyonu al
        new_distance = ((self.snake.body[0][0] - self.food.position[0])**2 + 
                       (self.snake.body[0][1] - self.food.position[1])**2)**0.5
        
        # Ödül hesapla
        reward = 0
        done = False
        
        # Çarpışma kontrolü
        if self.snake.check_collision(self.width, self.height):
            self.play_sound(self.crash_sound)
            reward = -10
            done = True
            self.total_episodes += 1
            # Modeli ve verileri kaydet
            if self.training:
                self.agent.save(self.model_path)
                self.save_training_data()
            # Oyunu otomatik olarak yeniden başlat
            self.reset_game()
        
        # Yem yeme kontrolü
        elif self.snake.body[0] == self.food.position:
            self.play_sound(self.eat_sound)
            reward = 10
            self.score += 1
            if self.score > self.best_score:
                self.best_score = self.score
            self.snake.grow_snake()
            self.food.respawn(self.snake.body)
        
        # Yeme yaklaşma/uzaklaşma kontrolü
        else:
            reward = 0.1 if new_distance < old_distance else -0.1
        
        self.episode_rewards += reward
        
        # Yeni durumu al
        next_state = self.agent.get_state(
            self.snake.body[0],
            self.snake.body,
            self.food.position,
            self.width,
            self.height
        )
        
        # Deneyimi hafızaya ekle ve eğit
        if self.training:
            self.agent.remember(state, action, reward, next_state, done)
            self.agent.replay()
        
        # Zamanı güncelle
        self.elapsed_time = int(time.time() - self.start_time)

    def draw(self) -> None:
        """Oyunu ekrana çizer"""
        self.screen.fill(self.BACKGROUND_COLOR)
        
        # Yılan ve yemi çiz
        self.snake.draw(self.screen, self.SNAKE_COLOR)
        self.food.draw(self.screen, self.FOOD_COLOR)
        
        # Font ayarla
        font = pygame.font.Font(None, 36)
        
        # Bilgileri göster
        info_texts = [
            f'Skor: {self.score}',
            f'En İyi Skor: {self.best_score}',
            f'Süre: {self.elapsed_time}s',
            f'Episode: {self.total_episodes}',
            f'Eğitim: {"Açık" if self.training else "Kapalı"}',
            f'Hız: {self.speed} FPS',
            f'Ses: {"Açık" if self.sound_enabled else "Kapalı"}'
        ]
        
        for i, text in enumerate(info_texts):
            text_surface = font.render(text, True, self.TEXT_COLOR)
            self.screen.blit(text_surface, (20, 20 + i * 30))
        
        # Duraklatma mesajı
        if self.paused:
            s = pygame.Surface((self.width, self.height))
            s.set_alpha(128)
            s.fill((0, 0, 0))
            self.screen.blit(s, (0, 0))
            
            pause_text = font.render('DURAKLATILDI - SPACE ile Devam Et', True, self.PAUSE_COLOR)
            text_rect = pause_text.get_rect(center=(self.width/2, self.height/2))
            self.screen.blit(pause_text, text_rect)
        
        pygame.display.flip()

    def run(self) -> str:
        """Ana oyun döngüsü"""
        while True:
            # Ayarları yeniden yükle
            settings_file = "data/settings.json"
            try:
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
                    self.sound_enabled = settings.get('ai_sound_enabled', True)
                    self.eat_sound.set_volume(settings.get('eat_sound_volume', 0.5))
                    self.crash_sound.set_volume(settings.get('crash_sound_volume', 0.3))
                    self.move_sound.set_volume(settings.get('move_sound_volume', 0.1))
            except (FileNotFoundError, json.JSONDecodeError):
                pass
            
            action = self.handle_input()
            if action:
                return action
            
            self.update()
            self.draw()
            self.clock.tick(self.speed)  # Hız ayarına göre FPS'i güncelle

    def load_settings(self, settings: dict = None) -> dict:
        """Ayarları yükler"""
        if settings is not None:
            return settings
            
        # Ayarlar verilmediyse dosyadan oku
        settings_file = "data/settings.json"
        try:
            with open(settings_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                'ai_sound_enabled': True,
                'eat_sound_volume': 0.5,
                'crash_sound_volume': 0.3,
                'move_sound_volume': 0.1
            } 