"""
解码器模块

负责处理用户输入的声母，并验证是否与目标诗句匹配
"""

import threading
import time
import random
from scipy import io
import numpy as np
import os

class Decoder:
    """
    解码器类
    
    负责解析和验证用户输入的声母序列，判断是否与目标诗句匹配
    """
    
    def __init__(self):
        """
        初始化解码器
        """
        self.current_thread = None
        self.decode_results = []  # 存储解码结果
        # 汉语拼音声母列表
        self.all_initials = [
            'b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'h', 
            'j', 'q', 'x', 'zh', 'ch', 'sh', 'r', 'z', 'c', 's', 'y', 'w'
        ]
    
    def decode(self, file_paths):
        """
        解码声母文件
        
        参数:
            file_paths: 声母文件路径列表
            
        返回:
            生成器，逐个返回解码结果
        """
        # 重置解码结果
        self.decode_results = []
        
        # 创建一个新线程来处理解码
        self.current_thread = threading.Thread(target=self._decode_thread, args=(file_paths,))
        self.current_thread.daemon = True
        self.current_thread.start()
        
        # 等待线程完成
        while self.current_thread.is_alive():
            time.sleep(0.1)
            yield None  # 让主线程继续运行
        
        # 返回解码结果
        for result in self.decode_results:
            yield result
    
    def _decode_thread(self, file_paths):
        """
        在单独的线程中处理解码
        
        参数:
            file_paths: 声母文件路径列表
        """
        # 处理每个文件
        for file_path in file_paths:
            # 模拟解码耗时
            time.sleep(0.5)
            
            # 15% 的概率随机返回一个声母
            if random.random() < 0.15:
                random_initial = random.choice(self.all_initials)
                self.decode_results.append(random_initial)
                continue
            
            # 正常解码逻辑
            if file_path is None:
                self.decode_results.append("?")
                continue
                
            try:
                # 加载.mat文件
                mat_data = io.loadmat(file_path)
                
                # 获取声母信息
                if 'initial' in mat_data:
                    initial = str(mat_data['initial'][0])
                    self.decode_results.append(initial)
                else:
                    # 从文件路径中提取声母
                    parts = file_path.split(os.sep)
                    if len(parts) >= 2:
                        self.decode_results.append(parts[-2])  # 返回目录名作为声母
                    else:
                        self.decode_results.append("?")
            except Exception as e:
                print(f"解码文件 {file_path} 时出错: {e}")
                self.decode_results.append("?")
