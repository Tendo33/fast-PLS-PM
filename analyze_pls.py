import sys
from pathlib import Path

import pandas as pd
import plspm.inner_model
import statsmodels.api as sm
import yaml
from plspm.config import MV, Config
from plspm.mode import Mode
from plspm.plspm import Plspm


# 猴子补丁：修复 plspm 与较新版本 pandas 的兼容性问题（zip 错误）
def fixed_inner_model_init(self, path: pd.DataFrame, scores: pd.DataFrame):
    self._InnerModel__summaries = None
    self._InnerModel__r_squared = pd.Series(0.0, index=path.index, name="r_squared")
    self._InnerModel__r_squared_adj = pd.Series(0.0, index=path.index, name="r_squared_adj")
    self._InnerModel__path_coefficients = pd.DataFrame(0.0, columns=path.columns, index=path.index)
    
    endogenous = path.sum(axis=1).astype(bool)
    self._InnerModel__endogenous = list(endogenous[endogenous].index)
    rows = scores.shape[0]
    
    # Access private module functions
    _summary = plspm.inner_model._summary
    _effects = plspm.inner_model._effects
    
    for dv in self._InnerModel__endogenous:
        # 修复：移除 loc[dv,] 中的尾随逗号，该逗号导致了 "zip argument 2 is longer than argument 1" 错误
        # 原始代码: ivs = path.loc[dv,][path.loc[dv,] == 1].index
        ivs = path.loc[dv][path.loc[dv] == 1].index
        
        exogenous = sm.add_constant(scores.loc[:, ivs])
        regression = sm.OLS(scores.loc[:, dv], exogenous).fit()
        
        self._InnerModel__path_coefficients.loc[dv, ivs] = regression.params
        rsquared = regression.rsquared
        self._InnerModel__r_squared.loc[dv] = rsquared
        self._InnerModel__r_squared_adj.loc[dv] = 1 - (1 - rsquared) * (rows - 1) / (rows - path.loc[dv].sum() - 1)
        self._InnerModel__summaries = pd.concat([self._InnerModel__summaries, _summary(dv, regression)]).reset_index(drop=True)
        
    self._InnerModel__effects = _effects(self._InnerModel__path_coefficients)

# 应用补丁
plspm.inner_model.InnerModel.__init__ = fixed_inner_model_init


def load_config(config_path='config.yaml'):
    """
    从 YAML 文件加载配置。
    如果未找到配置文件，程序将退出并提示用户。
    """
    config_file = Path(config_path)
    
    if not config_file.exists():
        print(f"错误：配置文件 '{config_path}' 未找到。")
        print(f"请复制 'config.example.yaml' 为 '{config_path}' 并根据你的数据进行配置。")
        sys.exit(1)
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # 验证必需的配置项
        required_keys = ['data', 'column_mapping', 'latent_variables', 'paths', 'output']
        for key in required_keys:
            if key not in config:
                print(f"错误：配置文件缺少必需的键: '{key}'")
                sys.exit(1)
        
        print(f"成功加载配置文件: {config_path}")
        return config
    
    except yaml.YAMLError as e:
        print(f"错误：配置文件格式错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"错误：无法读取配置文件: {e}")
        sys.exit(1)


def save_results_to_markdown(results_dict, output_file='pls_pm_report.md'):
    """
    将结果保存到带有详细解释的 Markdown 文件中。
    results_dict: {部分名称: 数据框} 的字典
    """
    print(f"\n正在生成 Markdown 报告: {output_file}...")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# PLS-PM / SEM 分析报告\n\n")
            f.write("此报告由生物实验数据分析脚本自动生成。报告详细说明了各项统计指标及其生物学意义。\n\n")
            
            for section, df in results_dict.items():
                f.write(f"## {section}\n\n")
                if df is None or df.empty:
                    f.write("该项暂无数据。\n\n")
                    continue
                
                # 预处理数据框以确保 Markdown 渲染正常
                # 1. 处理列名中的 '|' 字符，防止破坏表格结构
                df_to_save = df.copy()
                df_to_save.columns = [str(c).replace('|', '\\|') for c in df_to_save.columns]
                
                # 2. 如果索引是字符串，也处理其中的 '|'
                if df_to_save.index.dtype == 'object':
                    df_to_save.index = [str(i).replace('|', '\\|') for i in df_to_save.index]
                
                # 3. 处理数据中的 '|' (如果存在)
                for col in df_to_save.columns:
                    if df_to_save[col].dtype == 'object':
                        df_to_save[col] = df_to_save[col].apply(lambda x: str(x).replace('|', '\\|'))

                # 写入表格使用 GitHub 风格，兼容性更好
                f.write(df_to_save.to_markdown(index=True, tablefmt="github"))
                f.write("\n\n")
                
                # 针对不同表格提供更详尽的字段解释
                f.write("### 字段解析与指标说明\n\n")
                
                if "Inner Model" in section:
                    f.write("| 字段 | 解释 | 生物学/统计学意义 |\n")
                    f.write("| :--- | :--- | :--- |\n")
                    f.write("| **from** | 起始变量 | 路径的自变量，即影响源。 |\n")
                    f.write("| **to** | 目标变量 | 路径的因变量，即受影响的对象。 |\n")
                    f.write("| **estimate** | 估计值 (路径系数) | 衡量自变量对因变量直接影响的大小和方向 (范围通常在 -1 到 1)。 |\n")
                    f.write("| **std error** | 标准误 | 估计量的标准误差，反映估计的精确度。 |\n")
                    f.write("| **t** | t 检验统计量 | 估计值除以标准误的值，绝对值越大越显著。 |\n")
                    f.write("| **p>\\|t\\|** | p 值 | 判断显著性的核心指标。若 p < 0.05，认为对应的路径关系在统计上是显著的。 |\n")
                    
                elif "Path Coefficients" in section:
                    f.write("| 维度 | 解释 |\n")
                    f.write("| :--- | :--- |\n")
                    f.write("| **行(Row)** | 被影响的内生变量。 |\n")
                    f.write("| **列(Column)** | 施加影响的自变量。 |\n")
                    f.write("| **数值** | 对应路径的标准化系数。0 表示没有直接连接。 |\n")

                elif "R-Squared" in section:
                    f.write("| 指标 | 解释 | 理想范围 / 参考 |\n")
                    f.write("| :--- | :--- | :--- |\n")
                    f.write("| **type** | 变量类型 | Exogenous(外生，即只有输出路径) 或 Endogenous(内生，包含输入路径)。 |\n")
                    f.write("| **r_squared** | R² (判定系数) | 反映内生变量方差被模型解释的比例。 | > 0.6 表示模型解释力较好。 |\n")
                    f.write("| **r_squared_adj** | 调整后 R² | 考虑了自变量个数后的 R²，用于更公平地评价模型。 | 值越接近 R² 越好。 |\n")
                    f.write("| **block_communality** | 块共同度 | 衡量该潜变量与其测量指标间的平均关联程度。 | 建议 > 0.7 |\n")
                    f.write("| **ave** | 平均方差提取量 | 衡量潜变量对测量指标的平均方差贡献。 | 建议 > 0.5 (表示潜变量能解释过半的指标方差)。 |\n")
                    f.write("| **mean_redundancy** | 平均冗余度 | 反映模型对内生变量测量指标的整体预测能力。 | 值越高表示预测性越强。 |\n")

                elif "Outer Model" in section or "Loadings" in section:
                    f.write("| 指标 | 解释 | 评价指标 |\n")
                    f.write("| :--- | :--- | :--- |\n")
                    f.write("| **weight** | 权重 (Outer Weights) | 各个测量指标对潜变量分数的贡献权重。 | 越大说明指标对潜变量的定义越重要。 |\n")
                    f.write("| **loading** | 因子载荷 (Loadings) | 指标与潜变量的相关性。 | 建议 > 0.7 (表示指标对潜变量有高度代表性)。 |\n")
                    f.write("| **communality** | 共同性 | loading 的平方，衡量潜变量对该指标方差的解释比例。 | 越高越好。 |\n")
                    f.write("| **redundancy** | 冗余度 | 反映该指标通过模型被解释的程度。 | - |\n")
                    
                elif "Effects" in section:
                    f.write("| 字段 | 解释 |\n")
                    f.write("| :--- | :--- |\n")
                    f.write("| **direct** | 直接效应 | 两个变量之间直接连线的路径系数。 |\n")
                    f.write("| **indirect** | 间接效应 | 通过路径中其他中介变量传递的影响。 |\n")
                    f.write("| **total** | 总效应 | 直接效应 + 间接效应。反映一个变量对另一个变量的总影响力强度。 |\n")
                
                f.write("\n---\n\n")
        print("报告生成成功。")
    except Exception as e:
        print(f"生成报告失败: {e}")

def main(config_path='config.yaml'):
    """
    主分析函数，使用配置文件驱动。
    
    Args:
        config_path: YAML 配置文件路径，默认为 'config.yaml'
    """
    # 加载配置
    cfg = load_config(config_path)
    
    # 读取数据
    print("正在加载数据...")
    data_file = cfg['data']['file_path']
    header = cfg['data'].get('header', None)
    data_start_row = cfg['data'].get('data_start_row', 1)
    
    try:
        df = pd.read_excel(data_file, header=header)
    except Exception as e:
        print(f"读取文件错误: {e}")
        print(f"请检查配置文件中的 data.file_path 是否正确: {data_file}")
        return

    # 数据预处理
    print("正在预处理数据...")
    
    # 提取数据部分（从配置的起始行开始）
    data = df.iloc[data_start_row:].copy()
    
    # 从配置获取列映射
    column_mapping = cfg['column_mapping']
    
    # 重命名列
    selected_cols = []
    rename_dict = {}
    for idx, name in column_mapping.items():
        if idx < df.shape[1]:
            rename_dict[idx] = name
            selected_cols.append(idx)
        else:
            print(f"警告：列索引 {idx} 超出范围")

    data = data[selected_cols]
    data.columns = [rename_dict[c] for c in selected_cols]
    
    # 转换为数值型
    data = data.apply(pd.to_numeric, errors='coerce')
    
    # 删除包含缺失值的行
    original_len = len(data)
    data = data.dropna()
    if len(data) < original_len:
        print(f"已删除 {original_len - len(data)} 行包含缺失值的数据。")

    if data.empty:
        print("错误：清洗后没有剩余数据。")
        return

    print(f"数据形状: {data.shape}")
    
    # 从配置构建路径模型
    latent_vars = cfg['latent_variables']
    lvs = [lv['name'] for lv in latent_vars]
    path_matrix = pd.DataFrame(0, index=lvs, columns=lvs)
    
    # 根据配置的路径设置路径矩阵
    for source, target in cfg['paths']:
        if target in lvs and source in lvs:
            path_matrix.loc[target, source] = 1
        else:
            print(f"警告：路径 {source} -> {target} 中的变量不在潜变量列表中")
        
    print("路径矩阵已定义。")

    # 配置 PLS-PM
    plspm_config = Config(path_matrix, scaled=True)
    
    # 添加潜变量和测量指标
    for lv in latent_vars:
        lv_name = lv['name']
        mode = Mode.A if lv['mode'] == 'A' else Mode.B
        indicators = [MV(ind) for ind in lv['indicators']]
        plspm_config.add_lv(lv_name, mode, *indicators)
    
    # 检查方差
    print("正在检查方差...")
    low_var_cols = []
    for col in data.columns:
        if data[col].std() == 0:
            print(f"警告：列 {col} 方差为零。")
            low_var_cols.append(col)
            
    if low_var_cols:
        print("移除零方差列会破坏上面定义的模型结构。")
        # Proceeding hoping for the best or erroring out
    
    # 尝试 PLS-PM
    print("正在运行 PLS-PM（尝试 1）...")
    success = False
    report_file = cfg['output'].get('report_file', 'pls_pm_report.md')
    
    try:
        # 首先尝试不使用 scheme（默认值）
        plspm_calc = Plspm(data, plspm_config)
        print("PLS-PM 计算完成。")
        success = True
        
        print("\n" + "="*30)
        print("PLS-PM 结果")
        print("="*30)
        
        print("\n--- 内部模型路径系数 (关系) ---")
        print(plspm_calc.inner_model())
        
        print("\n--- 路径系数矩阵 ---")
        print(plspm_calc.path_coefficients())
        
        print("\n--- R-Squared (解释方差) ---")
        print(plspm_calc.inner_summary())
        
        print("\n--- 外部模型 (载荷/权重) ---")
        print(plspm_calc.outer_model())

        print("\n--- 效应 (直接, 间接, 总效应) ---")
        try:
            print(plspm_calc.effects())
        except:
            print("效应不可用")

        # 保存结果到 Markdown
        results = {
            'Inner Model (Relationships)': plspm_calc.inner_model(),
            'Path Coefficients': plspm_calc.path_coefficients(),
            'R-Squared': plspm_calc.inner_summary(),
            'Outer Model (Loadings)': plspm_calc.outer_model()
        }
        try:
            results['Effects'] = plspm_calc.effects()
        except:
            pass
            
        save_results_to_markdown(results, report_file)



    except Exception as e:
        print(f"PLS-PM 失败: {e}")
        import traceback
        traceback.print_exc()
        
    if not success:
        print("\n" + "="*30)
        print("备选方案：使用 semopy 进行 SEM（结构方程模型）")
        print("="*30)
        print("使用 semopy 估计关系（解释与 PLS-PM 类似）。")
        
        sem_report_file = cfg['output'].get('sem_report_file', 'sem_report.md')
        
        try:
            from semopy import Model
            
            # 从配置构建测量模型
            desc = []
            for lv in latent_vars:
                lv_name = lv['name']
                indicators = ' + '.join(lv['indicators'])
                desc.append(f"{lv_name} =~ {indicators}")
            
            # 从配置构建结构模型
            for source, target in cfg['paths']:
                desc.append(f"{target} ~ {source}")
                
            model_spec = "\n".join(desc)
            print("模型规范:")
            print(model_spec)
            
            model = Model(model_spec)
            print("正在拟合 SEM 模型...")
            # semopy 使用匹配标题的 DataFrame
            model.fit(data)
            
            print("\n--- SEM 估计值 (路径系数) ---")
            stats = model.inspect()
            # 筛选回归系数 (op='~')
            reg_stats = stats[stats['op'] == '~']
            print(reg_stats[['lval', 'op', 'rval', 'Estimate', 'p-value', 'Std. Err']])
            
            print("\n--- 测量模型 (载荷) ---")
            load_stats = stats[stats['op'] == '=~']
            print(load_stats[['lval', 'op', 'rval', 'Estimate', 'p-value']])
            
            print("\n--- R-Squared (R平方) ---")
            # 手动计算 R2 或在统计数据中查找
            try:
                # semopy 不在 inspect 中直接输出 R2？
                # 它有特定的方法，或者我们解释 'Estimate'
                pass
            except:
                pass

            # 保存 SEM 结果到 Markdown
            results = {
                'Path Coefficients': reg_stats,
                'Measurement Model (Loadings)': load_stats,
                'Full Stats': stats
            }
            save_results_to_markdown(results, sem_report_file)

        except ImportError:
            print("semopy 未安装或导入失败。")
        except Exception as e:
            print(f"SEM 失败: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    # 支持通过命令行参数指定配置文件
    # 用法: python analyze_pls.py [config.yaml]
    config_file = sys.argv[1] if len(sys.argv) > 1 else 'config.yaml'
    main(config_file)
