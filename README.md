# fast-PLS-PM - PLS-PM/SEM 生物数据分析工具

本项目是一个**配置驱动的统计分析工具**，专门用于分析生物实验数据中的因果关系，特别适合研究处理剂量与多个生理指标之间的关系。

## 📋 目录

- [项目简介](#项目简介)
- [快速开始](#快速开始)
- [配置文件详解](#配置文件详解)
- [如何更换数据集](#如何更换数据集)
- [运行分析](#运行分析)
- [理解分析结果](#理解分析结果)
- [常见问题](#常见问题)
- [技术支持](#技术支持)

---

## 项目简介

### 功能特性

- **PLS-PM / SEM 分析**：使用偏最小二乘路径建模（PLS-PM）和结构方程模型（SEM）分析变量间的因果关系
- **配置驱动**：通过简单的 YAML 配置文件即可适配不同的数据集，无需修改代码
- **自动报告生成**：分析完成后自动生成详细的 Markdown 格式报告
- **新手友好**：详细的配置说明和错误提示，即使不懂编程也能使用

### 适用场景

✅ 研究药物/营养素剂量与生理指标的关系  
✅ 分析多个指标之间的因果路径  
✅ 验证理论假设模型  
✅ 探索潜变量（不可直接观测的概念）与观测指标的关系  

### 示例研究问题

- "尿石素 A（UroA）剂量如何影响产蛋性能、肝脏健康和脂质代谢？"
- "不同处理浓度对多个生理指标的综合影响是什么？"

---

## 快速开始

### 前置要求

在开始之前，请确保你的电脑上已安装：

- **Python 3.13 或更高版本**
  - 检查方法：打开终端，输入 `python3 --version`
  - 如果未安装，访问：https://www.python.org/downloads/

- **uv 包管理工具**
  - 安装方法：`curl -LsSf https://astral.sh/uv/install.sh | sh`
  - 或访问：https://github.com/astral-sh/uv

### 安装步骤

#### 第一步：克隆或下载项目

```bash
# 如果你有 git
git clone <你的仓库地址>
cd bio_test

# 或者直接下载 ZIP 文件并解压
```

#### 第二步：安装依赖

```bash
# 进入项目目录
cd fast-PLS-PM

# 安装所有依赖包
uv sync

# 安装 PyYAML（如果上一步失败，单独安装）
uv pip install pyyaml --index-url https://pypi.org/simple
```

> **💡 提示**：如果遇到网络问题，可能需要开启代理或使用其他镜像源。

#### 第三步：准备配置文件

```bash
# 复制示例配置文件
cp config.example.yaml config.yaml
```

现在你已经成功安装！接下来需要根据你的数据配置 `config.yaml` 文件。

---

## 配置文件详解

配置文件 `config.yaml` 是整个分析的核心，它告诉程序如何读取和分析你的数据。

### 配置文件结构概览

```yaml
data:              # 数据文件配置
column_mapping:    # Excel 列到变量名的映射
latent_variables:  # 潜变量定义
paths:             # 因果关系路径
output:            # 输出文件设置
```

### 详细字段说明

#### 1️⃣ `data` - 数据文件配置

这部分告诉程序你的数据文件在哪里，格式是什么。

```yaml
data:
  file_path: "PLS-剂量实验.xlsx"
  header: null
  data_start_row: 1
```

**字段详解：**

| 字段 | 说明 | 示例值 | 如何设置 |
|------|------|--------|----------|
| `file_path` | Excel 文件的路径 | `"my_data.xlsx"` | 可以是相对路径或绝对路径，相对于项目根目录 |
| `header` | 表头所在行 | `null` 或 `0` | 打开 Excel，如果第一行是数据→`null`；如果第一行是列名→`0` |
| `data_start_row` | 数据起始行（0开始计数） | `1` | 打开 Excel，数据从第几行开始（第1行=索引0，第2行=索引1...） |

**示例场景：**

```
场景A：你的Excel文件是这样的
  第0行：[分类说明] UroA处理组 | 产蛋性能 | ...
  第1行：0.5 | 85.2 | ...
  → 设置：header: null, data_start_row: 1

场景B：你的Excel文件是这样的  
  第0行：[列名] 剂量 | 产蛋率 | 蛋重 | ...
  第1行：0.5 | 85.2 | 62.3 | ...
  → 设置：header: 0, data_start_row: 1
```

#### 2️⃣ `column_mapping` - 列映射配置

这部分将 Excel 的列（按位置）映射为有意义的变量名。

```yaml
column_mapping:
  0: "dose"           # 第1列(A列)
  1: "egg_rate"       # 第2列(B列)
  2: "egg_weight"     # 第3列(C列)
```

**重要概念：列索引（从0开始）**

| Excel列 | 列标识 | 列索引 | 配置示例 |
|---------|--------|--------|----------|
| 第1列 | A列 | 0 | `0: "var_name"` |
| 第2列 | B列 | 1 | `1: "var_name"` |
| 第3列 | C列 | 2 | `2: "var_name"` |
| 第10列 | J列 | 9 | `9: "var_name"` |

**如何确定列索引：**

1. 打开你的 Excel 文件
2. 找到你要分析的列
3. 从左边数，第1列是索引0，第2列是索引1，以此类推
4. **公式：列索引 = Excel列序号 - 1**

**变量命名规则：**

✅ **推荐**：`dose`, `egg_rate_1`, `liver_weight`, `SerumLip_TC`  
❌ **不推荐**：`1st_var`（数字开头）, `肝脏-重量`（中文或特殊符号）, `my var`（空格）

#### 3️⃣ `latent_variables` - 潜变量定义

这是最核心的部分！定义你研究模型中的"概念"。

```yaml
latent_variables:
  - name: "Treatment"      # 潜变量名
    mode: "A"              # 测量模式
    indicators:            # 观测指标
      - "dose_measured"
```

**什么是潜变量？**

潜变量是**无法直接测量**的抽象概念，需要通过多个**可观测指标**来反映。

| 潜变量（概念） | 观测指标（实际测量值） | 为什么需要多个指标？ |
|----------------|------------------------|----------------------|
| 产蛋性能 | 产蛋率、平均蛋重、蛋壳厚度 | 单一指标不能完全代表"性能" |
| 肝脏健康 | 肝重指数、ALT、AST | 多指标综合评估更准确 |
| 血脂水平 | 总胆固醇、甘油三酯、LDL | 血脂是多维度的 |

**字段详解：**

| 字段 | 说明 | 如何填写 |
|------|------|----------|
| `name` | 潜变量名称 | 简洁、有意义的英文名，如 `EggPerformance`、`LiverHealth` |
| `mode` | 测量模式 | `"A"` = 反映性（最常用）<br>`"B"` = 形成性（较少用） |
| `indicators` | 观测指标列表 | 列出所有用来测量这个潜变量的变量名（必须在 column_mapping 中定义过） |

**测量模式（Mode）选择指南：**

```
选择 Mode A（反映性）的情况：
  ✓ 指标是潜变量的"反映"或"表现"
  ✓ 潜变量变化会导致所有指标同时变化
  ✓ 指标之间应该高度相关
  ✓ 例如："智力"影响各科成绩

选择 Mode B（形成性）的情况：
  ✓ 指标"构成"或"形成"潜变量
  ✓ 指标变化导致潜变量变化
  ✓ 指标之间不一定相关
  ✓ 例如："收入"+"资产"+"教育"形成"社会经济地位"

🎯 不确定？90% 的情况选 "A"
```

**完整示例：**

```yaml
latent_variables:
  # 示例1：单指标潜变量（最简单）
  - name: "Dose"
    mode: "A"
    indicators:
      - "treatment_dose"

  # 示例2：双指标潜变量
  - name: "EggPerformance"
    mode: "A"
    indicators:
      - "laying_rate"      # 产蛋率
      - "average_weight"   # 平均蛋重

  # 示例3：多指标潜变量
  - name: "BloodLipid"
    mode: "A"
    indicators:
      - "total_cholesterol"  # 总胆固醇
      - "triglyceride"       # 甘油三酯
      - "ldl"                # 低密度脂蛋白
      - "hdl"                # 高密度脂蛋白
```

#### 4️⃣ `paths` - 路径模型定义

定义潜变量之间的因果关系（你的研究假设）。

```yaml
paths:
  - ["Treatment", "Outcome"]     # Treatment 影响 Outcome
  - ["Treatment", "Mediator"]    # Treatment 影响 Mediator
  - ["Mediator", "Outcome"]      # Mediator 影响 Outcome
```

**关键概念：路径的方向性**

> **路径格式**：`["源变量", "目标变量"]` = "源变量 → 目标变量"

```
["A", "B"]  ≠  ["B", "A"]  ← 这两个完全不同！

["Dose", "Health"]  表示：剂量影响健康（剂量是自变量）
["Health", "Dose"]  表示：健康影响剂量（健康是自变量）← 通常不合理
```

**路径模型示例：**

**示例1：简单模型（一个自变量影响多个因变量）**

```yaml
paths:
  - ["Dose", "LiverWeight"]
  - ["Dose", "BloodLipid"]
  - ["Dose", "Performance"]
```

可视化：
```
        ┌──→ LiverWeight
Dose ───┼──→ BloodLipid
        └──→ Performance
```

**示例2：中介模型（间接效应）**

```yaml
paths:
  - ["Dose", "BloodLipid"]        # 直接路径
  - ["BloodLipid", "LiverWeight"] # 中介路径
```

可视化：
```
Dose ──→ BloodLipid ──→ LiverWeight
```

含义：剂量先影响血脂，血脂再影响肝重（血脂是中介变量）

**示例3：复杂模型**

```yaml
paths:
  - ["Dose", "BloodLipid"]
  - ["Dose", "LiverWeight"]        # 直接效应
  - ["BloodLipid", "LiverWeight"]  # 间接效应
```

可视化：
```
Dose ──┬──→ BloodLipid ──┐
       │                  ↓
       └─────────────→ LiverWeight
```

含义：剂量既直接影响肝重，也通过血脂间接影响肝重

**注意事项：**

- ⚠️ 路径中的变量名必须在 `latent_variables` 中定义过
- ⚠️ 路径是有方向的，不能随意颠倒
- ✅ 可以有循环路径（如 A→B, B→C, C→A），但要谨慎使用
- ✅ 路径数量没有限制

#### 5️⃣ `output` - 输出配置

设置分析结果保存的文件名。

```yaml
output:
  report_file: "pls_pm_report.md"      # PLS-PM 结果
  sem_report_file: "sem_report.md"     # SEM 备选结果
```

**字段说明：**

| 字段 | 用途 | 建议命名 |
|------|------|----------|
| `report_file` | PLS-PM 分析报告 | 包含日期或实验名，如 `2024_dose_analysis.md` |
| `sem_report_file` | SEM 分析报告（备用） | 通常保持默认 `sem_report.md` |

**何时会生成 SEM 报告？**

- 当 PLS-PM 分析失败时，程序会自动尝试 SEM 方法
- 两种方法本质相似，结果可比较

---

## 如何更换数据集

### 完整操作流程（新手版）

假设你有一个新的实验数据文件 `my_experiment.xlsx`，需要分析"饲料添加剂"对"生长性能"和"免疫指标"的影响。

#### 步骤 1：准备数据文件

1. 确保数据是 `.xlsx` 或 `.xls` 格式
2. 数据按列组织（每列一个变量）
3. 将文件放在项目目录下（或记录完整路径）

**示例 Excel 文件结构：**

| A列 | B列 | C列 | D列 | E列 |
|-----|-----|-----|-----|-----|
| 添加量 | 体重1 | 体重2 | IgG | IgA |
| 0 | 1250 | 1280 | 15.2 | 8.3 |
| 10 | 1320 | 1350 | 18.5 | 9.7 |
| 20 | 1380 | 1420 | 21.3 | 11.2 |

#### 步骤 2：创建配置文件

```bash
# 复制示例配置
cp config.example.yaml my_experiment_config.yaml
```

#### 步骤 3：编辑配置文件

用文本编辑器打开 `my_experiment_config.yaml`，按以下小步骤修改：

**3.1 设置数据文件路径**

```yaml
data:
  file_path: "my_experiment.xlsx"  # ← 改成你的文件名
  header: 0                         # ← 如果第一行是列名，改成 0
  data_start_row: 1                 # ← 数据从第2行开始
```

**3.2 映射Excel列**

根据上面的示例 Excel：

```yaml
column_mapping:
  0: "additive_dose"    # A列：添加剂剂量
  1: "bodyweight_1"     # B列：体重测量1
  2: "bodyweight_2"     # C列：体重测量2
  3: "igg_level"        # D列：免疫球蛋白G
  4: "iga_level"        # E列：免疫球蛋白A
```

> **💡 记住**：列索引从0开始！第1列=0，第2列=1...

**3.3 定义潜变量**

```yaml
latent_variables:
  # 潜变量1：饲料添加剂剂量
  - name: "Additive"
    mode: "A"
    indicators:
      - "additive_dose"
  
  # 潜变量2：生长性能（用2个体重指标衡量）
  - name: "Growth"
    mode: "A"
    indicators:
      - "bodyweight_1"
      - "bodyweight_2"
  
  # 潜变量3：免疫指标
  - name: "Immunity"
    mode: "A"
    indicators:
      - "igg_level"
      - "iga_level"
```

**3.4 定义研究假设**

研究假设：添加剂影响生长和免疫

```yaml
paths:
  - ["Additive", "Growth"]      # 添加剂 → 生长性能
  - ["Additive", "Immunity"]    # 添加剂 → 免疫指标
```

**3.5 设置输出文件**

```yaml
output:
  report_file: "my_experiment_report.md"
  sem_report_file: "my_experiment_sem.md"
```

#### 步骤 4：检查配置

在运行前，再检查一下：

- [ ] `file_path` 文件确实存在
- [ ] `column_mapping` 的索引与 Excel 列对应
- [ ] `indicators` 中的名称都在 `column_mapping` 中定义过
- [ ] `paths` 中的变量名都在 `latent_variables` 中定义过
- [ ] 路径方向符合你的研究假设

#### 步骤 5：运行分析

```bash
# 使用自定义配置文件运行
uv run python analyze_pls.py my_experiment_config.yaml
```

#### 步骤 6：查看结果

```bash
# Mac 用户
open my_experiment_report.md

# Windows 用户（在 WSL 中）
explorer.exe my_experiment_report.md

# 或用任何文本编辑器打开
```

---

## 运行分析

### 基本用法

```bash
# 方法1：使用默认配置文件 config.yaml
uv run python analyze_pls.py

# 方法2：指定配置文件
uv run python analyze_pls.py my_config.yaml

# 方法3：在虚拟环境中运行（如果已激活）
python analyze_pls.py
```

### 运行过程说明

程序运行时会显示：

```
成功加载配置文件: config.yaml
正在加载数据...
正在预处理数据...
已删除 2 行包含缺失值的数据。
数据形状: (45, 14)
路径矩阵已定义。
正在检查方差...
正在运行 PLS-PM（尝试 1）...
PLS-PM 计算完成。

==============================
PLS-PM 结果
==============================
...
报告生成成功。
```

**各阶段说明：**

1. **加载配置**：读取 YAML 文件，验证格式
2. **加载数据**：读取 Excel 文件
3. **预处理数据**：
   - 删除缺失值
   - 转换数据类型
   - 检查方差（方差为0的列无法分析）
4. **构建模型**：根据配置创建路径模型
5. **运行分析**：PLS-PM 或 SEM
6. **生成报告**：保存 Markdown 文件

### 预期运行时间

- 小数据集（< 100 行，< 20 列）：5-10 秒
- 中等数据集（100-1000 行）：10-30 秒
- 大数据集（> 1000 行）：30-60 秒

---

## 理解分析结果

生成的报告文件（如 `pls_pm_report.md`）包含以下部分：

### 1. Inner Model（内部模型 - 路径关系）

显示潜变量之间的因果关系：

| from | to | estimate | std error | t | p>|t| |
|------|-----|----------|-----------|---|------|
| UroA | Egg | 0.523 | 0.089 | 5.88 | 0.001 |

**如何解读：**

- **from → to**：路径方向
- **estimate（路径系数）**：影响强度，范围 -1 到 1
  - 正值 = 正向影响（UroA越大，Egg越大）
  - 负值 = 负向影响
  - 绝对值越大，影响越强
- **p>|t|（p值）**：显著性
  - **p < 0.05** ✅ 关系显著（结果可靠）
  - **p ≥ 0.05** ⚠️ 关系不显著（可能是偶然）

**示例解读：**

```
UroA → Egg: estimate=0.523, p=0.001
解读：UroA对产蛋性能有显著的正向影响（p<0.05），
      路径系数0.523表示影响较强。
```

### 2. R-Squared（R²，解释方差）

衡量模型对每个内生变量的解释能力：

| 变量 | r_squared | 解释 |
|------|-----------|------|
| Egg | 0.658 | 模型解释了65.8%的产蛋性能变异 |

**评价标准：**

- **R² ≥ 0.67**：🟢 强解释力
- **0.33 ≤ R² < 0.67**：🟡 中等解释力
- **R² < 0.33**：🔴 弱解释力

### 3. Outer Model（外部模型 - 载荷）

显示观测指标与潜变量的关系：

| MV | LV | weight | loading |
|----|----|--------|---------|
| Egg_1 | Egg | 0.547 | 0.912 |

**如何解读：**

- **loading（因子载荷）**：指标对潜变量的代表性
  - **≥ 0.7** ✅ 指标很好
  - **0.4-0.7** ⚠️ 可接受
  - **< 0.4** ❌ 指标较差，考虑移除

---

## 常见问题

### Q1: 找不到配置文件

**错误信息：**
```
错误：配置文件 'config.yaml' 未找到。
```

**解决方法：**
```bash
cp config.example.yaml config.yaml
```

---

### Q2: 列索引超出范围

**错误信息：**
```
警告：列索引 15 超出范围
```

**原因：** Excel 文件实际只有 12 列，但配置中写了索引 15

**解决方法：**
1. 打开 Excel 文件，数一下实际有多少列
2. 修改 `column_mapping`，确保索引不超过实际列数

---

### Q3: 变量未定义

**错误信息：**
```
警告：路径 UroA -> EggPerformance 中的变量不在潜变量列表中
```

**原因：** `paths` 中使用的变量名在 `latent_variables` 中没有定义

**解决方法：**
检查拼写，确保 `paths` 中的名称与 `latent_variables` 中的 `name` 完全一致（区分大小写）

---

### Q4: 分析结果不显著

**现象：** 报告中所有 p 值都 > 0.05

**可能原因：**
1. 样本量太小（< 30）
2. 数据质量差（噪音大）
3. 假设模型不正确
4. 变量间确实没有关系

**建议：**
- 检查数据质量
- 增加样本量
- 重新审视研究假设

---

### Q5: PyYAML 安装失败

**错误信息：**
```
ModuleNotFoundError: No module named 'yaml'
```

**解决方法：**
```bash
# 方法1
uv pip install pyyaml --index-url https://pypi.org/simple

# 方法2（如果方法1失败）
python3 -m pip install --user pyyaml

# 方法3（使用代理，如果网络问题）
proxy_on  # 开启代理（需要提前配置）
uv pip install pyyaml
```

---

### Q6: Excel 文件读取失败

**错误信息：**
```
读取文件错误: No such file or directory
```

**解决方法：**
1. 检查文件路径是否正确
2. 如果使用相对路径，确保文件在项目目录下
3. 尝试使用绝对路径：`/Users/username/Desktop/data.xlsx`

---

### Q7: 如何知道我的模型是否合理？

**检查清单：**

- [ ] 所有路径系数的符号（正/负）符合预期
- [ ] 关键路径显著（p < 0.05）
- [ ] R² 值合理（≥ 0.3）
- [ ] 载荷值 > 0.7
- [ ] 没有明显的逻辑错误

**如果不确定：**
- 咨询统计专家
- 参考类似研究的模型
- 尝试不同的模型配置比较

---

## 技术支持

### 配置文件语法检查

在线 YAML 验证工具：https://www.yamllint.com/

### 获取帮助

遇到问题时，请提供：
1. 完整的错误信息
2. 你的配置文件（隐去敏感信息）
3. 数据文件的结构（列数、行数）
4. Python 和 uv 版本

### 进阶学习资源

- PLS-PM 原理：https://en.wikipedia.org/wiki/Partial_least_squares_path_modeling
- SEM 入门：结构方程模型相关教材
- YAML 语法：https://yaml.org/

---

## 附录

### 配置文件完整示例

参考 [`config.example.yaml`](config.example.yaml)，其中包含：
- 每个字段的详细注释
- 多种使用场景的示例
- 常见错误的说明

### 项目文件说明

```
fast-PLS-PM/
├── analyze_pls.py          # 主分析脚本
├── config.yaml             # 你的配置文件（需自己创建）
├── config.example.yaml     # 配置模板（有详细注释）
├── README.md               # 本文档
├── data/                   # 数据文件目录
│   └── PLS-剂量实验.xlsx   # 示例数据文件
├── output/                 # 输出目录
│   └── pls_pm_report.md    # 分析结果报告（运行后生成）
├── template/               # 配置模板目录
│   └── config.yaml         # 配置文件示例
└── .venv/                  # Python 虚拟环境（自动创建）
```

---

**最后更新：** 2026-02-04  
**版本：** 1.1  
**项目：** fast-PLS-PM
