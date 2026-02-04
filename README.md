# fast-PLS-PM

> 快速、配置驱动的 PLS-PM/SEM 生物数据分析工具

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## ✨ 特性

- 🔧 **配置驱动** - 无需修改代码，通过 YAML 配置文件适配不同数据集
- 📊 **双重分析** - 支持 PLS-PM 和 SEM 两种结构方程建模方法
- 📝 **自动报告** - 生成详细的 Markdown 分析报告，含统计指标解释
- 🎯 **新手友好** - 清晰的进度提示和错误信息，易于上手

---

## 🚀 快速开始

### 环境要求

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) 包管理工具

### 安装

```bash
# 1. 克隆项目
git clone <your-repo-url>
cd fast-PLS-PM

# 2. 安装依赖（如遇到镜像源问题，见下方故障排除）
uv sync

# 3. 准备配置文件
cp config.example.yaml config.yaml
```

### 运行分析

```bash
# 使用默认配置
uv run python analyze_pls.py

# 或指定配置文件
uv run python analyze_pls.py my_config.yaml
```

---

## 📁 项目结构

```
fast-PLS-PM/
├── analyze_pls.py          # 主分析脚本
├── config.yaml             # 你的配置（需创建）
├ ├── config.example.yaml     # 配置模板
├── data/
│   └── *.xlsx              # 数据文件
├── output/
│   └── *.md                # 生成的报告
└── template/
    └── config.yaml         # 配置示例
```

---

## ⚙️ 配置文件

配置文件 `config.yaml` 包含以下部分：

### 1. 数据配置

```yaml
data:
  file_path: "data/your_data.xlsx"  # Excel 文件路径
  header: null                       # 表头行（null 或 0）
  data_start_row: 1                  # 数据起始行
```

### 2. 列映射

```yaml
column_mapping:
  0: "variable_1"  # 第1列 → 变量名
  1: "variable_2"  # 第2列 → 变量名
  # ... 依此类推
```

> 💡 **注意**：列索引从 0 开始（第1列 = 0，第2列 = 1...）

### 3. 潜变量定义

```yaml
latent_variables:
  - name: "Treatment"       # 潜变量名
    mode: "A"              # 测量模式（A=反映性, B=形成性）
    indicators:            # 观测指标
      - "dose_measured"
  
  - name: "Outcome"
    mode: "A"
    indicators:
      - "indicator_1"
      - "indicator_2"
```

**测量模式选择：**
- **Mode A（反映性）**：潜变量导致指标变化，指标高度相关 → 90% 情况选这个
- **Mode B（形成性）**：指标构成潜变量，指标可不相关

### 4. 路径模型

```yaml
paths:
  - ["Treatment", "Outcome"]  # Treatment → Outcome
  - ["Mediator", "Outcome"]   # Mediator → Outcome
```

> ⚠️ **路径方向很重要**：`[A, B]` 表示 A → B，不可颠倒

### 5. 输出配置

```yaml
output:
  report_file: "output/my_report.md"
  sem_report_file: "output/my_sem_report.md"
```

**完整配置示例**请参考 [`config.example.yaml`](config.example.yaml)

---

## 📊 理解分析结果

分析完成后会生成 Markdown 报告，包含以下部分：

### 内部模型（路径系数）

| 指标                | 含义     | 判断标准              |
| ------------------- | -------- | --------------------- |
| **estimate**        | 路径系数 | 绝对值越大影响越强    |
| **p>&#124;t&#124;** | 显著性   | **p < 0.05** = 显著 ✅ |

### R² (解释方差)

| R² 值       | 解释力 |
| ----------- | ------ |
| ≥ 0.67      | 🟢 强   |
| 0.33 - 0.67 | 🟡 中等 |
| < 0.33      | 🔴 弱   |

### 外部模型（载荷）

| 指标 | 含义 | 判断标准 |
|------|------|----------|
| **loading** | 因子载荷 | **≥ 0.7** = 良好 ✅ |

---

## 🛠️ 故障排除

### 依赖安装失败（403 Forbidden）

如果使用清华镜像源时遇到 403 错误：

```bash
# 方法 1：使用官方 PyPI 源
uv pip install pandas openpyxl scikit-learn plspm semopy tabulate pyyaml \
  --index-url https://pypi.org/simple

# 方法 2：清理缓存后重试
uv cache clean
uv sync --index-url https://pypi.org/simple
```

### 配置文件错误

- ✅ 确保所有 `indicators` 在 `column_mapping` 中定义
- ✅ 确保所有 `paths` 中的变量在 `latent_variables` 中定义
- ✅ 列索引不要超出 Excel 实际列数

### 分析结果不显著

可能原因：
- 样本量太小（< 30）
- 数据质量差
- 模型假设不正确

---

## 💡 使用场景

**适合：**
- ✅ 研究药物/营养素剂量效应
- ✅ 分析多指标因果关系
- ✅ 验证理论模型
- ✅ 探索潜在变量

**示例研究问题：**
- "尿石素 A 剂量如何影响产蛋性能、肝脏健康和脂质代谢？"
- "不同处理浓度对生理指标的综合影响？"

---

## 📚 高级主题

<details>
<summary><b>如何更换数据集？</b></summary>

1. 准备 `.xlsx` 格式数据文件
2. 复制配置模板：`cp config.example.yaml my_config.yaml`
3. 根据你的数据修改配置：
   - 更新 `data.file_path`
   - 映射列索引到变量名
   - 定义潜变量和指标
   - 设置路径模型
4. 运行：`uv run python analyze_pls.py my_config.yaml`

</details>

<details>
<summary><b>模型设计建议</b></summary>

**路径模型类型：**

```yaml
# 简单模型（一因多果）
paths:
  - ["X", "Y1"]
  - ["X", "Y2"]

# 中介模型
paths:
  - ["X", "M"]    # X → 中介变量
  - ["M", "Y"]    # 中介变量 → Y

# 复杂模型（直接+间接效应）
paths:
  - ["X", "M"]
  - ["X", "Y"]    # 直接效应
  - ["M", "Y"]    # 间接效应
```

</details>

<details>
<summary><b>结果解读示例</b></summary>

```
路径: Treatment → Outcome
estimate = 0.65, p = 0.001

解读：
✓ p < 0.05，关系显著
✓ 正系数表示正向影响
✓ 0.65 表示影响较强
结论：Treatment 对 Outcome 有显著的正向影响
```

</details>

---

## 🤝 贡献

欢迎提交 Issues 和 Pull Requests！

---

## 📄 许可证

MIT License

---

## 🔗 资源

- [PLS-PM 原理](https://en.wikipedia.org/wiki/Partial_least_squares_path_modeling)
- [YAML 语法](https://yaml.org/)
- [uv 文档](https://github.com/astral-sh/uv)

---

**版本：** 1.1  
**最后更新：** 2026-02-04
