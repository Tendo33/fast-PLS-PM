# fast-PLS-PM

> 快速、配置驱动的 PLS-PM/SEM 生物数据分析工具

---

## 🚀 新手快速上手

### 1. 安装环境

```bash
# 安装 uv 包管理工具（如已安装可跳过）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 进入项目目录
cd fast-PLS-PM

# 安装依赖
uv sync
```

### 2. 准备数据和配置

```bash
# 1. 将你的 Excel 数据放到 data/ 文件夹
# 2. 复制配置模板
cp config.example.yaml template/config.yaml

# 3. 修改 config.yaml（参考下方说明）
```

### 3. 运行分析

```bash
uv run python analyze_pls.py
```

运行完成后,会在 `output/` 文件夹生成分析报告。

---

## ⚙️ 配置文件说明

编辑 `config.yaml`,按照你的数据修改以下内容：

### 1️⃣ 数据文件路径

```yaml
data:
  file_path: "data/你的数据.xlsx"  # 改成你的 Excel 文件名
  header: null                     # 如果第1行是表头,改成 0
  data_start_row: 1                # 数据从第几行开始
```

### 2️⃣ 列映射（告诉工具每列是什么）

```yaml
column_mapping:
  0: "剂量"      # 第1列是剂量
  1: "体重"      # 第2列是体重
  2: "产蛋率"    # 第3列是产蛋率
  # ... 依次填写所有列
```

> 💡 列号从 0 开始：第1列=0,第2列=1,第3列=2...

### 3️⃣ 定义潜变量

```yaml
latent_variables:
  - name: "处理剂量"        # 潜变量名称（自己起名）
    mode: "A"              # 固定填 "A"（90% 情况）
    indicators:            # 包含哪些列
      - "剂量"
  
  - name: "生产性能"
    mode: "A"
    indicators:
      - "产蛋率"
      - "蛋重"
```

### 4️⃣ 设置路径（谁影响谁）

```yaml
paths:
  - ["处理剂量", "生产性能"]  # 处理剂量 → 生产性能
  - ["处理剂量", "肝脏健康"]  # 处理剂量 → 肝脏健康
```

> ⚠️ 箭头方向：`["A", "B"]` 表示 A 影响 B

---

## 📊 看懂分析结果

生成的报告中重点看这些：

### 路径系数表格

| 指标         | 含义     | 怎么看                                  |
| ------------ | -------- | --------------------------------------- |
| **estimate** | 影响大小 | 数值越大影响越强（正数=正向,负数=负向） |
| **p值**      | 是否显著 | **p < 0.05** 就是显著 ✅                 |

**例子：**
```
路径: 处理剂量 → 产蛋率
estimate = 0.65, p = 0.001

解读: 剂量对产蛋率有显著的正向影响（p<0.05）
```

### R²（解释力）

| R² 值     | 解释         |
| --------- | ------------ |
| ≥ 0.67    | 🟢 解释力强   |
| 0.33-0.67 | 🟡 解释力中等 |
| < 0.33    | 🔴 解释力弱   |

---

## 🛠️ 常见问题

**Q: 安装依赖失败？**
```bash
# 换成官方源重试
uv sync --index-url https://pypi.org/simple
```

**Q: 运行报错？**
- 检查 `config.yaml` 中的变量名是否一致
- 确保列索引不超过 Excel 实际列数
- 确保 Excel 文件路径正确

**Q: 结果不显著？**
- 可能样本量太少（建议≥30）
- 可能数据质量问题
- 可能模型设置不对

---

## 📁 项目结构

```
fast-PLS-PM/
├── analyze_pls.py       # 分析脚本（不用改）
├── config.yaml          # 你的配置（需要改）
├── config.example.yaml  # 配置模板（参考用）
├── data/                # 放你的 Excel 数据
└── output/              # 自动生成的报告
```

---

## 📚 参考资料

- 更多配置示例: `template/config.yaml`
- 完整配置说明: `config.example.yaml`

**版本:** 1.1  
**License:** MIT
