import pygame

class Controls:
    def __init__(self, width: int = 800, height: int = 600):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Yılan Oyunu - Kontroller")
        
        # Modern renk paleti (diğer sınıflarla aynı)
        self.BACKGROUND_COLOR = (17, 24, 39)  # Koyu lacivert
        self.TEXT_COLOR = (243, 244, 246)  # Açık gri
        self.BUTTON_COLOR = (16, 185, 129)  # Yeşil
        self.BUTTON_HOVER_COLOR = (5, 150, 105)  # Koyu yeşil
        self.BORDER_COLOR = (75, 85, 99)  # Gri
        self.TITLE_COLOR = (16, 185, 129)  # Başlık için yeşil
        self.TITLE_BG_COLOR = (31, 41, 55)  # Başlık arka planı için koyu gri-mavi
        self.SCROLL_BG_COLOR = (31, 41, 55)  # Scroll bar arka plan rengi
        self.SCROLL_FG_COLOR = (75, 85, 99)  # Scroll bar rengi
        
        # Scroll değişkenleri
        self.scroll_y = 0
        self.scroll_speed = 30
        self.max_scroll = 0
        
        # Viewport (içerik alanı)
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
        
        # Font ayarları
        self.title_font = pygame.font.Font(None, 64)
        self.subtitle_font = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 36)
        
        # Kontrol tuşları ve açıklamaları
        self.controls = {
            'Klasik Mod Kontrolleri': {
                'Yön Tuşları / WASD': 'Yılanı hareket ettir',
                'SPACE': 'Oyunu duraklat/devam et',
                'M': 'Sesi aç/kapat',
                'ESC': 'Ana menüye dön',
                'Q': 'Oyundan çık'
            },
            'AI Mod Kontrolleri': {
                'SPACE': 'Oyunu başlat/durdur',
                'Yukarı Ok': 'Hızı artır',
                'Aşağı Ok': 'Hızı azalt',
                'M': 'Sesi aç/kapat',
                'ESC': 'Ana menüye dön',
                'Q': 'Oyundan çık'
            },
            'Oyun Sonu Kontrolleri': {
                'R': 'Yeniden oyna',
                'ESC': 'Ana menüye dön',
                'Q': 'Oyundan çık'
            }
        }
        
        # Geri dön butonu
        button_width = 200
        button_height = 50
        self.back_button = pygame.Rect(
            width//2 - button_width//2,
            height - 100,
            button_width,
            button_height
        )

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
                mouse_pos = pygame.mouse.get_pos()
                if self.back_button.collidepoint(mouse_pos):
                    return 'MENU'
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'MENU'
        
        return None

    def draw(self) -> None:
        """Kontroller menüsünü çizer"""
        self.screen.fill(self.BACKGROUND_COLOR)
        
        # Başlık (scroll etkilemez)
        title = self.title_font.render('KONTROLLER', True, self.TITLE_COLOR)
        title_rect = title.get_rect(center=(self.width//2, 60))
        
        # Başlık arka planı
        padding = 40
        title_bg = pygame.Surface((title.get_width() + padding * 2, title.get_height() + padding))
        title_bg.fill(self.TITLE_BG_COLOR)
        title_bg_rect = title_bg.get_rect(center=(self.width//2, 60))
        
        # Başlık arka planını çiz
        pygame.draw.rect(self.screen, self.TITLE_BG_COLOR, title_bg_rect, border_radius=15)
        pygame.draw.rect(self.screen, self.BORDER_COLOR, title_bg_rect, 3, border_radius=15)
        
        # Başlığı çiz
        self.screen.blit(title, title_rect)
        
        # Viewport alanını çiz
        pygame.draw.rect(self.screen, self.TITLE_BG_COLOR, self.viewport, border_radius=10)
        pygame.draw.rect(self.screen, self.BORDER_COLOR, self.viewport, 2, border_radius=10)
        
        # Scroll bar arka planını çiz
        pygame.draw.rect(self.screen, self.SCROLL_BG_COLOR, self.scroll_bar_bg, border_radius=5)
        
        # Viewport için surface oluştur
        viewport_surface = pygame.Surface((self.viewport.width, self.viewport.height))
        viewport_surface.fill(self.TITLE_BG_COLOR)
        
        # İçeriği viewport surface'ine çiz
        y_offset = self.scroll_y
        max_y = 0
        
        for section, items in self.controls.items():
            # Alt başlık pozisyonu
            subtitle_pos = y_offset
            
            # Sadece görünür alanda ise çiz
            if subtitle_pos + 30 > 0 and subtitle_pos < self.viewport.height:
                # Alt başlık
                subtitle = self.subtitle_font.render(section, True, self.TEXT_COLOR)
                subtitle_rect = subtitle.get_rect(x=30, y=subtitle_pos)
                viewport_surface.blit(subtitle, subtitle_rect)
            
            y_offset += 60
            
            # Kontrol tuşları ve açıklamaları
            for key, description in items.items():
                # Sadece görünür alanda ise çiz
                if y_offset + 30 > 0 and y_offset < self.viewport.height:
                    # Tuş
                    key_text = self.font.render(key, True, self.BUTTON_COLOR)
                    key_rect = key_text.get_rect(x=60, y=y_offset)
                    viewport_surface.blit(key_text, key_rect)
                    
                    # İki nokta
                    colon_text = self.font.render(':', True, self.TEXT_COLOR)
                    colon_rect = colon_text.get_rect(x=key_rect.right + 10, y=y_offset)
                    viewport_surface.blit(colon_text, colon_rect)
                    
                    # Açıklama
                    desc_text = self.font.render(description, True, self.TEXT_COLOR)
                    desc_rect = desc_text.get_rect(x=colon_rect.right + 10, y=y_offset)
                    viewport_surface.blit(desc_text, desc_rect)
                
                y_offset += 40
                max_y = max(max_y, y_offset)
            
            y_offset += 30
        
        # Maksimum scroll değerini hesapla
        self.max_scroll = max(0, max_y - self.viewport.height)
        
        # Viewport surface'ini ekrana çiz
        self.screen.blit(viewport_surface, self.viewport)
        
        # Scroll bar'ı güncelle ve çiz
        self.update_scroll_bar()
        pygame.draw.rect(self.screen, self.SCROLL_FG_COLOR, self.scroll_bar, border_radius=5)
        
        # Geri dön butonu
        mouse_pos = pygame.mouse.get_pos()
        button_color = self.BUTTON_HOVER_COLOR if self.back_button.collidepoint(mouse_pos) else self.BUTTON_COLOR
        
        # Buton gölgesi
        shadow_rect = self.back_button.copy()
        shadow_rect.y += 3
        pygame.draw.rect(self.screen, (0, 0, 0, 50), shadow_rect, border_radius=10)
        
        # Butonu çiz
        pygame.draw.rect(self.screen, button_color, self.back_button, border_radius=10)
        pygame.draw.rect(self.screen, self.BORDER_COLOR, self.back_button, 2, border_radius=10)
        
        # Buton metni
        text = self.font.render('Geri Dön', True, self.TEXT_COLOR)
        text_rect = text.get_rect(center=self.back_button.center)
        self.screen.blit(text, text_rect)
        
        pygame.display.flip()

    def run(self) -> str:
        """Kontroller menüsünü çalıştırır"""
        while True:
            self.draw()
            action = self.handle_input()
            
            if action:
                return action 