"""
出题器单元测试
"""

import unittest
import os
import yaml
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from src.pywordmatch.question_generator import QuestionGenerator

class TestQuestionGenerator(unittest.TestCase):
    """测试出题器类"""
    
    def setUp(self):
        """测试前准备工作"""
        # 创建临时目录和文件
        self.temp_dir = tempfile.mkdtemp()
        
        # 创建临时配置文件
        self.config_dir = os.path.join(self.temp_dir, 'config')
        os.makedirs(self.config_dir, exist_ok=True)
        
        self.config_file = os.path.join(self.config_dir, 'config.yaml')
        self.test_questions = {
            'questions': [
                {
                    'id': 1,
                    'q': '测试诗句一',
                    'a': ['t', 'sh', 'sh', 'j', 'y']
                },
                {
                    'id': 2,
                    'q': '测试诗句二',
                    'a': ['c', 'sh', 'sh', 'j', 'er']
                }
            ]
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.test_questions, f, allow_unicode=True)
        
        # 创建临时声母目录和.mat文件
        self.data_dir = os.path.join(self.temp_dir, 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 为每个声母创建目录和测试文件
        for initial in ['t', 'sh', 'j', 'y', 'c', 'er']:
            initial_dir = os.path.join(self.data_dir, initial)
            os.makedirs(initial_dir, exist_ok=True)
            
            # 创建几个测试.mat文件
            for i in range(1, 4):
                with open(os.path.join(initial_dir, f'{i}.mat'), 'w') as f:
                    f.write(f'Test file for {initial}')
    
    def tearDown(self):
        """测试后清理工作"""
        # 删除临时目录
        shutil.rmtree(self.temp_dir)
    
    @patch('src.pywordmatch.question_generator.os.path.exists')
    @patch('src.pywordmatch.question_generator.os.path.join')
    @patch('src.pywordmatch.question_generator.os.listdir')
    def test_get_question(self, mock_listdir, mock_join, mock_exists):
        """测试获取问题功能"""
        # 配置模拟对象
        mock_exists.return_value = True
        mock_join.side_effect = lambda *args: '/'.join(args)
        mock_listdir.return_value = ['1.mat', '2.mat', '3.mat']
        
        # 创建出题器实例，但不调用load_questions
        generator = QuestionGenerator.__new__(QuestionGenerator)
        generator.questions = self.test_questions['questions']
        generator.used_questions = set()
        
        # 测试获取问题
        question = generator.get_question()
        
        # 验证结果
        self.assertIn('id', question)
        self.assertIn('q', question)
        self.assertIn('a', question)
        self.assertIn('file_paths', question)
        
        # 验证ID是否在预期范围内
        self.assertIn(question['id'], [1, 2])
        
        # 验证文件路径列表长度是否与声母列表长度相同
        self.assertEqual(len(question['file_paths']), len(question['a']))
    
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='questions: []')
    @patch('yaml.safe_load')
    def test_load_questions(self, mock_yaml_load, mock_open):
        """测试加载问题功能"""
        # 配置模拟对象
        mock_yaml_load.return_value = self.test_questions
        
        # 创建出题器实例，但不调用__init__方法
        generator = QuestionGenerator.__new__(QuestionGenerator)
        generator.questions = []
        
        # 手动调用加载问题方法
        generator.load_questions()
        
        # 验证结果
        self.assertEqual(len(generator.questions), 2)
        self.assertEqual(generator.questions[0]['id'], 1)
        self.assertEqual(generator.questions[1]['id'], 2)
        
        # 验证是否调用了正确的方法
        mock_open.assert_called_once()
        mock_yaml_load.assert_called_once()
    
    def test_used_questions_reset(self):
        """测试已使用问题重置功能"""
        # 创建出题器实例，但不调用load_questions
        generator = QuestionGenerator.__new__(QuestionGenerator)
        
        # 手动设置问题列表和已使用问题集合
        generator.questions = self.test_questions['questions']
        generator.used_questions = {1, 2}  # 所有问题都已使用
        
        # 获取问题，应该会重置已使用问题集合
        question = generator.get_question()
        
        # 验证已使用问题集合是否被重置
        self.assertEqual(len(generator.used_questions), 1)
        self.assertIn(question['id'], generator.used_questions)

if __name__ == '__main__':
    unittest.main() 
