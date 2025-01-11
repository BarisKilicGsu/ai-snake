import pygame
from classic_mode.menu import Menu
from classic_mode.game import Game
from classic_mode.settings import Settings
from classic_mode.controls import Controls
from ai_mode.game import AIGame

def main():
    pygame.init()
    
    # Pencere boyutları
    width = 800
    height = 600
    
    # Menü ve oyun nesneleri
    menu = Menu(width, height)
    game = Game(width, height)
    ai_game = AIGame(width, height)
    settings = Settings(width, height)
    controls = Controls(width, height)
    
    current_screen = 'MENU'
    
    while True:
        if current_screen == 'MENU':
            current_screen = menu.run()
        elif current_screen == 'Klasik Mod':
            current_screen = game.run()
        elif current_screen == 'AI Mod':
            current_screen = ai_game.run()
        elif current_screen == 'Ayarlar':
            current_screen = settings.run()
            if current_screen == 'MENU':
                # Ayarları yükle
                game_settings = settings.settings
                game.load_settings(game_settings)
                ai_game.load_settings(game_settings)
        elif current_screen == 'Kontroller':
            current_screen = controls.run()
        elif current_screen == 'QUIT':
            break
    
    pygame.quit()

if __name__ == '__main__':
    main() 