import pygame
from pywordmatch.utils import get_font, BLACK, LIGHT_CYAN

class Button:
    """
    按钮组件类
    用于创建可交互的按钮，支持悬停和点击效果
    """
    def __init__(self, x, y, width, height, text, color, hover_color, text_color):
        """
        初始化按钮
        
        参数:
            x, y: 按钮左上角的坐标
            width, height: 按钮的宽度和高度
            text: 按钮上显示的文本
            color: 按钮的默认颜色
            hover_color: 鼠标悬停或按下时的颜色
            text_color: 文本的颜色
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.is_pressed = False
        
    def draw(self, surface):
        """
        在指定的surface上绘制按钮
        
        参数:
            surface: 要绘制到的pygame surface
        """
        # 根据状态选择颜色
        current_color = self.hover_color if self.is_pressed else (
                        self.hover_color if self.is_hovered else self.color)
        
        # 绘制按钮
        pygame.draw.rect(surface, current_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, LIGHT_CYAN, self.rect, 2, border_radius=10)  # 边框
        
        # 绘制文字
        font = get_font(36)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        # 如果按下，稍微偏移文字位置以产生按下效果
        if self.is_pressed:
            text_rect.y += 2
            
        surface.blit(text_surface, text_rect)
        
    def check_hover(self, pos):
        """
        检查鼠标是否悬停在按钮上
        
        参数:
            pos: 鼠标位置的(x, y)坐标元组
            
        返回:
            如果鼠标在按钮上，返回True，否则返回False
        """
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
    
    def check_pressed(self, pos, pressed):
        """
        检查按钮是否被按下
        
        参数:
            pos: 鼠标位置的(x, y)坐标元组
            pressed: 如果鼠标按下为True，否则为False
            
        返回:
            如果按钮被按下，返回True，否则返回False
        """
        if self.rect.collidepoint(pos):
            self.is_pressed = pressed
            return self.is_pressed
        return False 
