# pywordmatch

## 项目构建说明

本项目依据 PEP 518 标准，使用 pyproject.toml 文件进行项目配置。

### 工具安装

推荐使用 uv 或 rye 或 poetry（速度较慢）等工具操作

```shell
# 安装 uv
pip install uv

# 验证 uv
uv --version
```

### 项目运行

在项目根目录下执行

```bash
# 根据 pyproject.toml 文件安装项目依赖
uv sync

# 运行项目
uv run -m pywordmatch

```

### 管理依赖

```bash
# 添加依赖
uv add numpy

# 删除依赖
uv remove numpy

# 更新依赖
uv update

# 查看依赖
uv list
```
