import os

# 创建data目录（如果不存在）
if not os.path.exists('data'):
    os.mkdir('data')

# 声母列表
pinyin_initials = ['b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'h', 'j', 
                   'q', 'x', 'zh', 'ch', 'sh', 'r', 'z', 'c', 's', 'y', 'w']

# 创建23个声母子目录
for initial in pinyin_initials:
    dir_path = os.path.join('data', initial)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

print("所有声母目录已创建完成！")
