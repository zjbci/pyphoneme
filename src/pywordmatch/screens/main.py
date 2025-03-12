"""
主界面模块

实验的主要界面，显示问题和接收用户输入
"""

import pygame
import sys
from pywordmatch.screens.result import result_screen
from pywordmatch.utils import get_font, BLACK, WHITE, LIGHT_GRAY, CYAN, DARK_CYAN, LIGHT_CYAN, GREEN, PINK
from pywordmatch.components.button import Button
from pywordmatch.question_generator import QuestionGenerator
from pywordmatch.decoder import Decoder

def main_screen():
    """
    显示实验主界面
    """
    # 初始化pygame
    pygame.init()
    
    # 获取屏幕信息并设置全屏
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("声母匹配实验")
    
    # 创建出题器和解码器
    question_generator = QuestionGenerator()
    decoder = Decoder()
    
    # 实验状态变量
    current_question = None
    decoded_results = []
    decoding_complete = False
    current_round = 0  # 从0开始计数
    max_rounds = 20
    
    # 实验结果统计
    experiment_results = {
        'total_questions': 0,
        'total_characters': 0,
        'correct_characters': 0,
        'questions': []  # 存储每个问题的详细信息
    }
    
    # 创建"下一题"按钮和"完成实验"按钮
    button_width, button_height = 200, 60
    button_x = (screen_width - button_width) // 2
    button_y = int(screen_height * 0.75)  # 放在屏幕底部1/4的位置
    next_button = Button(button_x, button_y, button_width, button_height, 
                         "下一题", CYAN, DARK_CYAN, BLACK)
    finish_button = Button(button_x, button_y, button_width, button_height, 
                          "完成", CYAN, DARK_CYAN, BLACK)
    
    # 解码生成器
    decode_generator = None
    
    # 主循环
    running = True
    next_question_clicked = False
    
    while running:
        # 如果没有当前问题或解码已完成且点击了下一题，获取新问题
        if current_question is None or (decoding_complete and next_question_clicked):
            # 如果有当前问题，保存结果
            if current_question is not None:
                # 计算正确字符数
                correct_count = 0
                for i, result in enumerate(decoded_results):
                    if i < len(current_question['a']) and result != "_":
                        if result == current_question['a'][i]:
                            correct_count += 1
                
                # 保存问题结果
                question_result = {
                    'id': current_question['id'],
                    'question': current_question['q'],
                    'expected': current_question['a'],
                    'actual': decoded_results,
                    'correct_count': correct_count
                }
                experiment_results['questions'].append(question_result)
                experiment_results['total_characters'] += len(current_question['a'])
                experiment_results['correct_characters'] += correct_count
            
            # 增加轮次计数
            current_round += 1
            
            # 检查是否达到最大轮次
            if current_round > max_rounds:
                break
            
            # 更新实验统计
            experiment_results['total_questions'] += 1
            
            # 获取新问题
            current_question = question_generator.get_question()
            decoded_results = ["_"] * len(current_question['a'])  # 初始化为下划线
            decoding_complete = False
            next_question_clicked = False
            
            # 开始解码
            decode_generator = decoder.decode(current_question['file_paths'])
        
        # 处理事件
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
                if decoding_complete:
                    if current_round == max_rounds:
                        finish_button.check_hover(event.pos)
                    else:
                        next_button.check_hover(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and decoding_complete:  # 左键
                    if current_round == max_rounds:
                        if finish_button.check_pressed(event.pos, True):
                            pass  # 按下效果
                    else:
                        if next_button.check_pressed(event.pos, True):
                            pass  # 按下效果
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and decoding_complete:  # 左键
                    if current_round == max_rounds:
                        finish_button.is_pressed = False
                        if finish_button.check_hover(event.pos):
                            # 保存最后一题的结果
                            save_current_question_result(current_question, decoded_results, experiment_results)
                            # 直接跳出循环，进入结算界面
                            running = False
                    else:
                        next_button.is_pressed = False
                        if next_button.check_hover(event.pos):
                            next_question_clicked = True
        
        # 如果有解码生成器，获取下一个解码结果
        if decode_generator is not None and not decoding_complete:
            try:
                result = next(decode_generator)
                if result is not None:
                    # 找到第一个未解码的位置
                    for i in range(len(decoded_results)):
                        if decoded_results[i] == "_":
                            decoded_results[i] = result
                            break
                    
                    # 检查是否所有位置都已解码
                    if "_" not in decoded_results:
                        decoding_complete = True
            except StopIteration:
                decoding_complete = True
                decode_generator = None
        
        # 清屏 - 使用黑色背景
        screen.fill(BLACK)
        
        # 绘制轮次信息
        round_font = get_font(2.5)
        round_text = round_font.render(f"第 {current_round}/{max_rounds} 题", True, LIGHT_GRAY)
        round_rect = round_text.get_rect(topleft=(20, 20))
        screen.blit(round_text, round_rect)
        
        # 绘制问题
        if current_question:
            # 绘制诗句
            question_font = get_font(9)
            question_text = question_font.render(current_question['q'], True, LIGHT_CYAN)
            question_rect = question_text.get_rect(center=(screen_width // 2, screen_height // 3))
            screen.blit(question_text, question_rect)
            
            # 绘制解码结果
            result_font = get_font(7)
            result_spacing = 100  # 字符间距
            total_width = result_spacing * len(decoded_results)
            start_x = (screen_width - total_width) // 2 + result_spacing // 2
            
            for i, result in enumerate(decoded_results):
                # 确定文字颜色：如果已解码（不是下划线），则根据是否正确选择颜色
                if result != "_":
                    # 检查解码结果是否正确
                    is_correct = (i < len(current_question['a']) and result == current_question['a'][i])
                    text_color = GREEN if is_correct else PINK
                else:
                    text_color = WHITE  # 未解码的位置使用白色
                
                result_text = result_font.render(result, True, text_color)
                result_rect = result_text.get_rect(center=(start_x + i * result_spacing, screen_height * 0.6))
                screen.blit(result_text, result_rect)
                
                # 绘制下划线
                line_y = result_rect.bottom + 5
                line_color = text_color if result != "_" else WHITE
                pygame.draw.line(screen, line_color, 
                                (start_x + i * result_spacing - 20, line_y),
                                (start_x + i * result_spacing + 20, line_y), 2)
        
        # 如果解码完成，显示按钮
        if decoding_complete:
            if current_round == max_rounds:
                finish_button.draw(screen)
            else:
                next_button.draw(screen)
        
        # 更新屏幕
        pygame.display.flip()
        
        # 控制帧率
        pygame.time.Clock().tick(60)
    
    # 实验结束，显示结束界面
    result_screen(screen, screen_width, screen_height, experiment_results)

def save_current_question_result(current_question, decoded_results, experiment_results):
    """
    保存当前问题的结果
    
    参数:
        current_question: 当前问题
        decoded_results: 解码结果
        experiment_results: 实验结果统计
    """
    # 计算正确字符数
    correct_count = 0
    for i, result in enumerate(decoded_results):
        if i < len(current_question['a']) and result != "_":
            if result == current_question['a'][i]:
                correct_count += 1
    
    # 保存问题结果
    question_result = {
        'id': current_question['id'],
        'question': current_question['q'],
        'expected': current_question['a'],
        'actual': decoded_results,
        'correct_count': correct_count
    }
    experiment_results['questions'].append(question_result)
    experiment_results['total_characters'] += len(current_question['a'])
    experiment_results['correct_characters'] += correct_count
