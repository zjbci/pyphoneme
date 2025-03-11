import os
import pygame

# 颜色定义 - 深色背景和浅色文字
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
CYAN = (0, 200, 200)
DARK_CYAN = (0, 150, 150)
LIGHT_CYAN = (100, 255, 255)

# 尝试加载系统中的中文字体
def get_font(size):
    # 尝试常见的中文字体，按优先级排序
    font_names = [
        'simhei.ttf',  # 黑体
        'simsun.ttc',  # 宋体
        'msyh.ttc',    # 微软雅黑
        'simkai.ttf',  # 楷体
        'STKAITI.TTF', # 华文楷体
        'STFANGSO.TTF',# 华文仿宋
        'STXIHEI.TTF'  # 华文细黑
    ]
    
    # 尝试从系统字体目录加载字体
    for font_name in font_names:
        # Windows 字体路径
        windows_font_path = os.path.join('C:\\Windows\\Fonts', font_name)
        # Linux 字体路径
        linux_font_path = os.path.join('/usr/share/fonts/truetype', font_name)
        # macOS 字体路径
        macos_font_path = os.path.join('/Library/Fonts', font_name)
        
        # 尝试加载字体
        if os.path.exists(windows_font_path):
            return pygame.font.Font(windows_font_path, size)
        elif os.path.exists(linux_font_path):
            return pygame.font.Font(linux_font_path, size)
        elif os.path.exists(macos_font_path):
            return pygame.font.Font(macos_font_path, size)
    
    # 如果找不到中文字体，使用默认字体并打印警告
    print("警告：找不到中文字体，文字可能显示为方块")
    return pygame.font.Font(None, size)
