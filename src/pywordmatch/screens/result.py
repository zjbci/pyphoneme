"""
实验结束模块

显示实验的统计数据
"""

import pygame
import sys
from pywordmatch.utils import get_font, BLACK, WHITE, CYAN, DARK_CYAN, LIGHT_CYAN
from pywordmatch.components.button import Button
from pywordmatch.question_generator import QuestionGenerator
from pywordmatch.decoder import Decoder

def result_screen(screen, screen_width, screen_height, experiment_results):
    """
    显示实验结束界面
    
    参数:
        screen: pygame屏幕对象
        screen_width: 屏幕宽度
        screen_height: 屏幕高度
        experiment_results: 实验结果统计数据
    """
    # 计算正确率
    accuracy = 0
    if experiment_results['total_characters'] > 0:
        accuracy = experiment_results['correct_characters'] / experiment_results['total_characters'] * 100
    
    # 创建"返回主菜单"按钮
    button_width, button_height = 250, 60
    button_x = (screen_width - button_width) // 2
    button_y = int(screen_height * 0.75)  # 放在屏幕底部1/4的位置
    menu_button = Button(button_x, button_y, button_width, button_height, 
                         "退出实验", CYAN, DARK_CYAN, BLACK)
    
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
                menu_button.check_hover(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键
                    if menu_button.check_pressed(event.pos, True):
                        pass  # 按下效果
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # 左键
                    menu_button.is_pressed = False
                    if menu_button.check_hover(event.pos):
                        # 退出实验
                        pygame.quit()
                        sys.exit()
        
        # 清屏 - 使用黑色背景
        screen.fill(BLACK)
        
        # 绘制实验结束文字
        title_font = get_font(7)
        title_text = title_font.render("实验结束", True, LIGHT_CYAN)
        title_rect = title_text.get_rect(center=(screen_width // 2, int(screen_height * 0.15)))
        screen.blit(title_text, title_rect)
        
        # 绘制统计数据
        stats_font = get_font(5)
        line_height = int(screen_height * 0.07)
        
        # 题目数量
        questions_text = stats_font.render(f"题目数量: {experiment_results['total_questions']}", True, WHITE)
        questions_rect = questions_text.get_rect(center=(screen_width // 2, int(screen_height * 0.3)))
        screen.blit(questions_text, questions_rect)
        
        # 解码文字总数
        total_chars_text = stats_font.render(f"解码文字总数: {experiment_results['total_characters']}", True, WHITE)
        total_chars_rect = total_chars_text.get_rect(center=(screen_width // 2, int(screen_height * 0.3) + line_height))
        screen.blit(total_chars_text, total_chars_rect)
        
        # 解码正确总数
        correct_chars_text = stats_font.render(f"解码正确总数: {experiment_results['correct_characters']}", True, WHITE)
        correct_chars_rect = correct_chars_text.get_rect(center=(screen_width // 2, int(screen_height * 0.3) + 2 * line_height))
        screen.blit(correct_chars_text, correct_chars_rect)
        
        # 解码正确率
        accuracy_text = stats_font.render(f"解码正确率: {accuracy:.2f}%", True, WHITE)
        accuracy_rect = accuracy_text.get_rect(center=(screen_width // 2, int(screen_height * 0.3) + 3 * line_height))
        screen.blit(accuracy_text, accuracy_rect)
        
        # 绘制按钮
        menu_button.draw(screen)
        
        # 更新屏幕
        pygame.display.flip()
