"""
出题器模块

负责从配置文件中读取诗句并生成问题
"""

import os
import random
import yaml

class QuestionGenerator:
    """
    出题器类
    
    负责从配置文件中读取诗句，并根据实验规则生成问题
    """
    
    def __init__(self):
        """
        初始化出题器
        """
        self.questions = []
        self.used_questions = set()  # 记录已使用的问题ID
        self.load_questions()
    
    def load_questions(self):
        """
        从配置文件加载问题
        """
        try:
            with open('config/config.yaml', 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                if 'questions' in config:
                    self.questions = config['questions']
                    print(f"成功加载 {len(self.questions)} 个问题")
                else:
                    print("配置文件中没有找到问题列表")
        except Exception as e:
            print(f"加载问题时出错: {e}")
    
    def get_question(self):
        """
        获取一个随机问题
        
        如果所有问题都已使用，则重置已使用问题集合
        
        返回:
            包含问题信息的字典，包括id, q, a和声母文件路径列表
        """
        # 如果所有问题都已使用，重置
        if len(self.used_questions) >= len(self.questions):
            self.used_questions.clear()
            print("所有问题已用完，重置问题池")
        
        # 获取未使用的问题
        available_questions = [q for q in self.questions if q['id'] not in self.used_questions]
        
        # 随机选择一个问题
        question = random.choice(available_questions)
        self.used_questions.add(question['id'])
        
        # 为每个声母选择一个随机的.mat文件
        file_paths = []
        for initial in question['a']:
            # 构建声母目录路径
            initial_dir = os.path.join('data', initial)
            
            # 检查目录是否存在
            if not os.path.exists(initial_dir):
                print(f"警告: 声母目录 {initial_dir} 不存在")
                file_paths.append(None)
                continue
            
            # 获取可用的.mat文件
            mat_files = [f for f in os.listdir(initial_dir) if f.endswith('.mat') and f[0].isdigit()]
            
            if not mat_files:
                print(f"警告: 在 {initial_dir} 中没有找到.mat文件")
                file_paths.append(None)
                continue
            
            # 随机选择一个文件
            selected_file = random.choice(mat_files)
            file_path = os.path.join(initial_dir, selected_file)
            file_paths.append(file_path)
        
        # 返回问题信息和文件路径
        result = {
            'id': question['id'],
            'q': question['q'],
            'a': question['a'],
            'file_paths': file_paths
        }
        
        return result 
