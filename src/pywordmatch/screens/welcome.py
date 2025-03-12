import pygame
import sys
from pywordmatch.screens import intro
from pywordmatch.utils import get_font, BLACK, WHITE, DARK_GREY, CYAN, DARK_CYAN, LIGHT_CYAN
from pywordmatch.components.button import Button

# 初始化pygame
pygame.init()

# 获取屏幕信息并设置全屏
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("汉语发声解码实验")

def welcome_screen():
    # 创建开始按钮
    button_width, button_height = 200, 60
    button_x = (screen_width - button_width) // 2  # 水平居中
    button_y = int(screen_height * 0.75)  # 在屏幕底部1/4的位置
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
                        # 切换到说明界面，而不是直接进入主界面
                        intro.intro_screen(screen, screen_width, screen_height)
                        return
        
        # 清屏 - 使用黑色背景
        screen.fill(BLACK)
        
        # 绘制欢迎文字 - 使用浅青色
        font = get_font(8)  # 原来是72，约为屏幕高度的7%
        welcome_text = font.render("欢迎参与汉语发声解码实验", True, LIGHT_CYAN)
        text_rect = welcome_text.get_rect(center=(screen_width // 2, int(screen_height * 0.375)))
        screen.blit(welcome_text, text_rect)

        # 绘制欢迎文字 - 使用浅青色
        font = get_font(4)  # 原来是72，约为屏幕高度的7%
        welcome_text = font.render("按 Esc 键退出实验", True, DARK_GREY)
        text_rect = welcome_text.get_rect(center=(screen_width // 2, int(screen_height * 0.7)))
        screen.blit(welcome_text, text_rect)

        # 绘制按钮
        start_button.draw(screen)
        
        # 更新屏幕
        pygame.display.flip()
