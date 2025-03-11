import pygame
import sys
from pywordmatch import main_screen
from pywordmatch.utils import get_font, BLACK, WHITE, LIGHT_GRAY, CYAN, DARK_CYAN, LIGHT_CYAN
from pywordmatch.components.button import Button

# 初始化pygame
pygame.init()

# 获取屏幕信息并设置全屏
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("欢迎界面")

def welcome_screen():
    # 创建开始按钮
    button_width, button_height = 200, 60
    button_x = (screen_width - button_width) // 2
    button_y = (screen_height + 100) // 2  # 在屏幕中心下方一点
    start_button = Button(button_x, button_y, button_width, button_height, 
                         "开始", CYAN, DARK_CYAN, BLACK)
    
    # 主循环
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            
            # 鼠标事件处理
            elif event.type == pygame.MOUSEMOTION:
                start_button.check_hover(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键
                    if start_button.check_pressed(event.pos, True):
                        pass  # 按下效果
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # 左键
                    start_button.is_pressed = False
                    if start_button.check_hover(event.pos):
                        # 切换到主页面
                        main_screen.main_screen()
                        return
        
        # 清屏 - 使用黑色背景
        screen.fill(BLACK)
        
        # 绘制欢迎文字 - 使用浅青色
        font = get_font(72)
        welcome_text = font.render("欢迎使用", True, LIGHT_CYAN)
        text_rect = welcome_text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
        screen.blit(welcome_text, text_rect)
        
        # 绘制按钮
        start_button.draw(screen)
        
        # 更新屏幕
        pygame.display.flip()
