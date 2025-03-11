import os
import shutil
from scipy import io

# 声母列表
pinyin_initials = ['b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'h', 'j', 
                   'q', 'x', 'zh', 'ch', 'sh', 'r', 'z', 'c', 's', 'y', 'w']

# 为每个声母目录复制.mat文件
for initial in pinyin_initials:
    dir_path = os.path.join('data', initial)
    
    # 检查目录是否存在
    if not os.path.exists(dir_path):
        print(f"警告: 目录 {dir_path} 不存在，跳过")
        continue
    
    # 原始.mat文件路径
    original_mat_file = os.path.join(dir_path, f'{initial}_sound.mat')
    
    # 检查原始文件是否存在
    if not os.path.exists(original_mat_file):
        print(f"警告: 文件 {original_mat_file} 不存在，跳过")
        continue
    
    # 加载原始.mat文件数据
    try:
        mat_data = io.loadmat(original_mat_file)
        
        # 创建6个副本，命名为1.mat到6.mat
        for i in range(1, 7):
            new_file_path = os.path.join(dir_path, f'{i}.mat')
            
            # 保存相同的数据到新文件
            io.savemat(new_file_path, mat_data)
            print(f"已创建: {new_file_path}")
            
    except Exception as e:
        print(f"处理文件 {original_mat_file} 时出错: {e}")

print("所有.mat文件复制完成！") 
