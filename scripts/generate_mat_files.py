import os
import numpy as np
from scipy import io, signal
import matplotlib.pyplot as plt

# 确保data目录存在
if not os.path.exists('data'):
    os.mkdir('data')

# 声母列表
pinyin_initials = ['b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'h', 'j', 
                   'q', 'x', 'zh', 'ch', 'sh', 'r', 'z', 'c', 's', 'y', 'w']

# 采样率
sample_rate = 16000  # Hz

# 为每个声母生成模拟声音数据并保存为.mat文件
for initial in pinyin_initials:
    # 创建目录（如果不存在）
    dir_path = os.path.join('data', initial)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    
    # 生成模拟声音数据
    # 这里我们使用不同的频率和持续时间来模拟不同声母的特性
    duration = 0.5  # 秒
    
    # 根据声母特性设置不同的频率
    if initial in ['b', 'p', 'm']:
        # 唇音
        base_freq = 120
    elif initial in ['f']:
        # 唇齿音
        base_freq = 200
    elif initial in ['d', 't', 'n', 'l']:
        # 舌尖音
        base_freq = 150
    elif initial in ['g', 'k', 'h']:
        # 舌根音
        base_freq = 180
    elif initial in ['j', 'q', 'x']:
        # 舌面音
        base_freq = 220
    elif initial in ['zh', 'ch', 'sh', 'r']:
        # 舌尖后音
        base_freq = 160
    elif initial in ['z', 'c', 's']:
        # 舌尖前音
        base_freq = 190
    else:  # 'y', 'w'
        # 介音
        base_freq = 240
    
    # 生成时间序列
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    # 生成基本波形
    base_signal = np.sin(2 * np.pi * base_freq * t)
    
    # 添加谐波以模拟声母特性
    harmonic1 = 0.5 * np.sin(2 * np.pi * base_freq * 2 * t)
    harmonic2 = 0.3 * np.sin(2 * np.pi * base_freq * 3 * t)
    
    # 添加噪声以模拟摩擦音特性（对于某些声母）
    if initial in ['f', 'h', 'sh', 's', 'x', 'c', 'ch', 'z', 'zh']:
        noise = 0.2 * np.random.normal(0, 1, len(t))
    else:
        noise = 0.05 * np.random.normal(0, 1, len(t))
    
    # 组合信号
    signal = base_signal + harmonic1 + harmonic2 + noise
    
    # 应用包络以模拟声母的起始和结束特性
    envelope = np.ones_like(t)
    attack = int(0.1 * sample_rate)  # 起音时间
    decay = int(0.3 * sample_rate)   # 衰减时间
    
    # 应用起音斜坡
    envelope[:attack] = np.linspace(0, 1, attack)
    # 应用衰减斜坡
    envelope[-decay:] = np.linspace(1, 0, decay)
    
    # 应用包络
    final_signal = signal * envelope
    
    # 归一化信号
    final_signal = final_signal / np.max(np.abs(final_signal))
    
    # 创建数据字典
    data = {
        'signal': final_signal,
        'sample_rate': sample_rate,
        'initial': initial,
        'duration': duration,
        'base_frequency': base_freq
    }
    
    # 保存为.mat文件
    mat_file_path = os.path.join(dir_path, f'{initial}_sound.mat')
    io.savemat(mat_file_path, data)
    
    # 可选：生成并保存波形图
    plt.figure(figsize=(10, 4))
    plt.plot(t, final_signal)
    plt.title(f'声母 "{initial}" 的波形')
    plt.xlabel('时间 (秒)')
    plt.ylabel('振幅')
    plt.grid(True)
    plt.tight_layout()
    
    # 保存图像
    plt.savefig(os.path.join(dir_path, f'{initial}_waveform.png'))
    plt.close()
    
    print(f'已生成声母 "{initial}" 的.mat文件和波形图')

print("所有声母的.mat文件和波形图已生成完成！") 
