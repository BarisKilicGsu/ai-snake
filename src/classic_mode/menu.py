import pygame
from typing import List, Tuple, Dict

class Menu:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Yılan Oyunu - Ana Menü")
        
        # Modern renk paleti (Game sınıfı ile aynı)
        self.BACKGROUND_COLOR = (17, 24, 39)  # Koyu lacivert
        self.TEXT_COLOR = (243, 244, 246)  # Açık gri
        self.BUTTON_COLOR = (16, 185, 129)  # Yeşil
        self.BUTTON_HOVER_COLOR = (5, 150, 105)  # Koyu yeşil
        self.BORDER_COLOR = (75, 85, 99)  # Gri
        self.EXIT_BUTTON_COLOR = (239, 68, 68)  # Parlak kırmızı
        self.EXIT_BUTTON_HOVER_COLOR = (220, 38, 38)  # Koyu kırmızı
        self.TITLE_COLOR = (16, 185, 129)  # Başlık için yeşil
        self.TITLE_BG_COLOR = (31, 41, 55)  # Başlık arka planı için koyu gri-mavi
        self.SCROLL_BG_COLOR = (31, 41, 55)  # Scroll bar arka plan rengi
        self.SCROLL_FG_COLOR = (75, 85, 99)  # Scroll bar rengi
        
        # Scroll değişkenleri
        self.scroll_y = 0
        self.scroll_speed = 30
        self.max_scroll = 0
        
        # Buton alanı (viewport)
        viewport_top = height * 0.35  # Başlığın altında başlasın
        viewport_height = height * 0.55  # Ekranın %55'i kadar yükseklik
        self.viewport = pygame.Rect(
            width * 0.2,  # Sol kenardan %20 içeride
            viewport_top,
            width * 0.6,  # Genişliğin %60'ı kadar
            viewport_height
        )
        
        # Scroll bar
        scroll_bar_width = 10
        self.scroll_bar_bg = pygame.Rect(
            self.viewport.right + 10,  # Viewport'un sağında
            self.viewport.top,
            scroll_bar_width,
            self.viewport.height
        )
        self.scroll_bar = pygame.Rect(
            self.scroll_bar_bg.x,
            self.scroll_bar_bg.y,
            scroll_bar_width,
            self.viewport.height  # Başlangıçta tam yükseklik
        )
        
        # Menü butonları
        self.button_width = self.viewport.width - 40  # Viewport'dan biraz dar
        self.button_height = 60
        self.button_spacing = 20
        
        # Başlık için y pozisyonu
        self.title_y = height * 0.2
        
        # Butonları oluştur
        self.create_buttons()
        
        self.font = pygame.font.Font(None, 48)
        self.title_font = pygame.font.Font(None, 82)

    def create_buttons(self):
        """Butonları oluştur"""
        self.buttons = {}
        button_positions = ['Klasik Mod', 'AI Mod', 'Kontroller', 'Ayarlar', 'Çıkış']
        
        # Tüm butonların toplam yüksekliğini hesapla
        total_height = len(button_positions) * self.button_height + (len(button_positions) - 1) * self.button_spacing
        
        # İlk butonun y pozisyonunu hesapla (ortala)
        start_y = 0
        
        for i, text in enumerate(button_positions):
            self.buttons[text] = pygame.Rect(
                (self.viewport.width - self.button_width) // 2,  # Viewport içinde yatayda ortala
                start_y + i * (self.button_height + self.button_spacing),  # Viewport içinde dikeyde sırala
                self.button_width,
                self.button_height
            )

    def handle_input(self) -> str:
        """Kullanıcı girdilerini işler"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'QUIT'
            
            # Mouse wheel olaylarını yakala
            if event.type == pygame.MOUSEWHEEL:
                if self.viewport.collidepoint(pygame.mouse.get_pos()):
                    self.scroll_y = min(0, max(self.scroll_y + event.y * self.scroll_speed, -self.max_scroll))
                    self.update_scroll_bar()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Sol tık
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Sadece viewport içindeyse buton tıklamalarını kontrol et
                    if self.viewport.collidepoint(mouse_pos):
                        # Mouse pozisyonunu viewport koordinatlarına çevir
                        viewport_mouse_x = mouse_pos[0] - self.viewport.x
                        viewport_mouse_y = mouse_pos[1] - self.viewport.y - self.scroll_y
                        
                        for text, button in self.buttons.items():
                            if button.collidepoint(viewport_mouse_x, viewport_mouse_y):
                                if text == 'Çıkış':
                                    return 'QUIT'
                                return text
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'QUIT'
                    
        return None

    def update_scroll_bar(self):
        """Scroll bar pozisyonunu güncelle"""
        if self.max_scroll > 0:
            # Scroll bar yüksekliğini hesapla
            visible_ratio = self.viewport.height / (self.viewport.height + self.max_scroll)
            self.scroll_bar.height = max(20, self.scroll_bar_bg.height * visible_ratio)
            
            # Scroll bar pozisyonunu hesapla
            scroll_ratio = -self.scroll_y / self.max_scroll
            max_scroll_bar_y = self.scroll_bar_bg.bottom - self.scroll_bar.height
            self.scroll_bar.y = self.scroll_bar_bg.top + (max_scroll_bar_y - self.scroll_bar_bg.top) * scroll_ratio

    def draw(self) -> None:
        """Menüyü ekrana çizer"""
        self.screen.fill(self.BACKGROUND_COLOR)
        
        # Başlık için gölge efekti
        title = self.title_font.render('YILAN OYUNU', True, self.TITLE_COLOR)
        title_rect = title.get_rect(center=(self.width//2, self.title_y))
        
        # Başlık arka planı
        padding = 40
        title_bg = pygame.Surface((title.get_width() + padding * 2, title.get_height() + padding))
        title_bg.fill(self.TITLE_BG_COLOR)
        title_bg_rect = title_bg.get_rect(center=(self.width//2, self.title_y))
        
        # Başlık arka plan gölgesi
        shadow_rect = title_bg_rect.copy()
        shadow_rect.y += 4
        pygame.draw.rect(self.screen, (0, 0, 0, 50), shadow_rect, border_radius=15)
        
        # Başlık arka planını çiz
        pygame.draw.rect(self.screen, self.TITLE_BG_COLOR, title_bg_rect, border_radius=15)
        pygame.draw.rect(self.screen, self.BORDER_COLOR, title_bg_rect, 3, border_radius=15)
        
        # Başlık gölgesi
        shadow_offset = 2
        title_shadow = self.title_font.render('YILAN OYUNU', True, (0, 0, 0))
        shadow_rect = title_rect.copy()
        shadow_rect.x += shadow_offset
        shadow_rect.y += shadow_offset
        self.screen.blit(title_shadow, shadow_rect)
        
        # Başlığı çiz
        self.screen.blit(title, title_rect)
        
        # Viewport alanını çiz
        pygame.draw.rect(self.screen, self.TITLE_BG_COLOR, self.viewport, border_radius=10)
        pygame.draw.rect(self.screen, self.BORDER_COLOR, self.viewport, 2, border_radius=10)
        
        # Scroll bar arka planını çiz
        pygame.draw.rect(self.screen, self.SCROLL_BG_COLOR, self.scroll_bar_bg, border_radius=5)
        
        # Mouse pozisyonunu viewport koordinatlarına çevir
        mouse_pos = pygame.mouse.get_pos()
        if self.viewport.collidepoint(mouse_pos):
            viewport_mouse_x = mouse_pos[0] - self.viewport.x
            viewport_mouse_y = mouse_pos[1] - self.viewport.y - self.scroll_y
        else:
            viewport_mouse_x = -1
            viewport_mouse_y = -1
        
        # Viewport için surface oluştur
        viewport_surface = pygame.Surface((self.viewport.width, self.viewport.height))
        viewport_surface.fill(self.TITLE_BG_COLOR)
        
        # Maksimum scroll değerini hesapla
        last_button = list(self.buttons.values())[-1]
        content_height = last_button.bottom + self.button_spacing
        self.max_scroll = max(0, content_height - self.viewport.height)
        
        # Butonları viewport surface'ine çiz
        for text, button in self.buttons.items():
            # Butonun scroll edilmiş pozisyonu
            scrolled_button = button.copy()
            scrolled_button.y += self.scroll_y
            
            # Viewport içinde görünür alan kontrolü
            if scrolled_button.bottom > 0 and scrolled_button.top < self.viewport.height:
                # Buton renklerini belirle
                if text == 'Çıkış':
                    default_color = self.EXIT_BUTTON_COLOR
                    hover_color = self.EXIT_BUTTON_HOVER_COLOR
                else:
                    default_color = self.BUTTON_COLOR
                    hover_color = self.BUTTON_HOVER_COLOR
                
                # Hover efekti için kontrol
                color = hover_color if button.collidepoint(viewport_mouse_x, viewport_mouse_y) else default_color
                
                # Buton gölgesi
                shadow_rect = scrolled_button.copy()
                shadow_rect.y += 3
                pygame.draw.rect(viewport_surface, (0, 0, 0, 50), shadow_rect, border_radius=10)
                
                # Buton arka planı
                pygame.draw.rect(viewport_surface, color, scrolled_button, border_radius=10)
                pygame.draw.rect(viewport_surface, self.BORDER_COLOR, scrolled_button, 2, border_radius=10)
                
                # Buton metni
                text_surface = self.font.render(text, True, self.TEXT_COLOR)
                text_rect = text_surface.get_rect(center=scrolled_button.center)
                viewport_surface.blit(text_surface, text_rect)
        
        # Viewport surface'ini ekrana çiz
        self.screen.blit(viewport_surface, self.viewport)
        
        # Scroll bar'ı güncelle ve çiz
        self.update_scroll_bar()
        pygame.draw.rect(self.screen, self.SCROLL_FG_COLOR, self.scroll_bar, border_radius=5)
        
        pygame.display.flip()

    def run(self) -> str:
        """Menüyü çalıştırır ve seçilen modu döndürür"""
        while True:
            self.draw()
            action = self.handle_input()
            
            if action:
                return action 