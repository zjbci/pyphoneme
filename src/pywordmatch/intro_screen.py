"""
说明界面模块

显示实验规则和操作说明
"""

import pygame
import sys
from pywordmatch import main_screen
from pywordmatch.utils import get_font, BLACK, WHITE, LIGHT_GRAY, CYAN, DARK_CYAN, LIGHT_CYAN
from pywordmatch.components.button import Button

def intro_screen(screen, screen_width, screen_height):
    """
    显示实验说明界面
    
    参数:
        screen: pygame屏幕对象
        screen_width: 屏幕宽度
        screen_height: 屏幕高度
    """
    # 创建"我已理解，开始"按钮
    button_width, button_height = 250, 60
    button_x = (screen_width - button_width) // 2
    button_y = (screen_height + 200) // 2  # 在屏幕中心下方
    start_button = Button(button_x, button_y, button_width, button_height, 
                         "我已理解，开始", CYAN, DARK_CYAN, BLACK)
    
    # 说明文字 - 分三行显示，总共不超过50字
    intro_text = [
        "这是一个声母匹配实验，你需要根据给出的诗句，",
        "找出每个汉字对应的声母，并按顺序输入。",
        "答对得分，答错扣分，看看你能得多少分！"
    ]
    
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
        
        # 绘制说明文字标题
        title_font = get_font(48)
        title_text = title_font.render("实验说明", True, LIGHT_CYAN)
        title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 2 - 200))
        screen.blit(title_text, title_rect)
        
        # 绘制说明文字内容
        content_font = get_font(28)
        line_height = 40
        for i, line in enumerate(intro_text):
            text = content_font.render(line, True, WHITE)
            text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 80 + i * line_height))
            screen.blit(text, text_rect)
        
        # 绘制按钮
        start_button.draw(screen)
        
        # 更新屏幕
        pygame.display.flip() 
