"""
解码器单元测试
"""

import unittest
import os
import tempfile
import shutil
import numpy as np
from scipy import io
from unittest.mock import patch, MagicMock
from src.pywordmatch.decoder import Decoder

class TestDecoder(unittest.TestCase):
    """测试解码器类"""
    
    def setUp(self):
        """测试前准备工作"""
        # 创建临时目录
        self.temp_dir = tempfile.mkdtemp()
        
        # 创建测试.mat文件
        self.test_files = []
        self.test_initials = ['b', 'c', 'd']
        
        for i, initial in enumerate(self.test_initials):
            file_path = os.path.join(self.temp_dir, f'test_{i}.mat')
            
            # 创建包含声母信息的.mat文件
            data = {
                'signal': np.random.rand(1000),
                'sample_rate': 16000,
                'initial': np.array([initial], dtype='<U1'),  # 使用正确的格式
                'duration': 0.5
            }
            io.savemat(file_path, data)
            self.test_files.append(file_path)
    
    def tearDown(self):
        """测试后清理工作"""
        # 删除临时目录
        shutil.rmtree(self.temp_dir)
    
    def test_decode_thread(self):
        """测试解码线程方法"""
        # 创建解码器实例
        decoder = Decoder()
        
        # 直接调用解码线程方法
        decoder._decode_thread(self.test_files)
        
        # 验证结果
        self.assertEqual(len(decoder.decode_results), len(self.test_initials))
        for i, initial in enumerate(self.test_initials):
            self.assertEqual(decoder.decode_results[i], initial)
    
    def test_decode_thread_with_invalid_files(self):
        """测试使用无效文件进行解码线程"""
        # 创建包含无效文件路径的列表
        invalid_files = [None, os.path.join(self.temp_dir, 'non_existent.mat'), self.test_files[0]]
        
        # 创建解码器实例
        decoder = Decoder()
        
        # 直接调用解码线程方法
        decoder._decode_thread(invalid_files)
        
        # 验证结果
        self.assertEqual(len(decoder.decode_results), 3)
        self.assertEqual(decoder.decode_results[0], '?')  # None 应该返回 ?
        self.assertEqual(decoder.decode_results[1], '?')  # 不存在的文件应该返回 ?
        self.assertEqual(decoder.decode_results[2], self.test_initials[0])  # 有效文件应该返回正确的声母
    
    def test_decode_thread_with_directory_extraction(self):
        """测试从目录名提取声母的解码线程"""
        # 创建特殊的测试文件，不包含initial字段
        special_dir = os.path.join(self.temp_dir, 'data', 'zh')
        os.makedirs(special_dir, exist_ok=True)
        special_file = os.path.join(special_dir, 'test.mat')
        
        # 创建不包含initial字段的.mat文件
        data = {
            'signal': np.random.rand(1000),
            'sample_rate': 16000,
            'duration': 0.5
        }
        io.savemat(special_file, data)
        
        # 创建解码器实例
        decoder = Decoder()
        
        # 直接调用解码线程方法
        decoder._decode_thread([special_file])
        
        # 验证结果
        self.assertEqual(len(decoder.decode_results), 1)
        self.assertEqual(decoder.decode_results[0], 'zh')  # 应该从目录名提取声母
    
    def test_decode_generator(self):
        """测试解码生成器的集成功能"""
        # 创建解码器实例
        decoder = Decoder()
        
        # 获取解码生成器
        decode_gen = decoder.decode(self.test_files)
        
        # 跳过None值（线程运行中）
        result = next(decode_gen)
        while result is None:
            result = next(decode_gen)
        
        # 收集所有结果
        results = [result]  # 包含第一个非None结果
        for r in decode_gen:
            results.append(r)
        
        # 验证结果
        self.assertEqual(len(results), len(self.test_initials))
        for i, initial in enumerate(self.test_initials):
            self.assertEqual(results[i], initial)

if __name__ == '__main__':
    unittest.main() 
