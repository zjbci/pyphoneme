import sys
import pygame
from pywordmatch.utils import get_font, BLACK, WHITE, LIGHT_GRAY, CYAN, LIGHT_CYAN

def main_screen():
    # 初始化pygame（如果尚未初始化）
    if not pygame.get_init():
        pygame.init()
    
    # 获取屏幕信息并设置全屏
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("主页面")
    
    # 主循环
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # 清屏 - 使用黑色背景
        screen.fill(BLACK)
        
        # 这里可以添加主页面的内容 - 使用浅青色文字
        font = get_font(36)
        text = font.render("这是主页面", True, LIGHT_CYAN)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)
        
        # 更新屏幕
        pygame.display.flip()
    
    return
