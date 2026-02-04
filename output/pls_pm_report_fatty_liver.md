# PLS-PM / SEM 分析报告

此报告由生物实验数据分析脚本自动生成。报告详细说明了各项统计指标及其生物学意义。

## Inner Model (Relationships)

| index                                      | from           | to                       |    estimate |   std error |          t |    p>\|t\| |
|--------------------------------------------|----------------|--------------------------|-------------|-------------|------------|------------|
| UroA_Treatment -> LayingPerformance        | UroA_Treatment | LayingPerformance        |  0.269007   |   0.0894251 |  3.00818   | 0.00322378 |
| UroA_Treatment -> LiverFatIndex            | UroA_Treatment | LiverFatIndex            |  0.102972   |   0.0923541 |  1.11497   | 0.267169   |
| UroA_Treatment -> LiverGlutamateMetabolism | UroA_Treatment | LiverGlutamateMetabolism |  0.0937646  |   0.0924386 |  1.01434   | 0.312529   |
| UroA_Treatment -> LiverAntioxidant         | UroA_Treatment | LiverAntioxidant         | -0.0177863  |   0.092833  | -0.191594  | 0.848395   |
| UroA_Treatment -> LiverImmune              | UroA_Treatment | LiverImmune              | -0.00729103 |   0.0928452 | -0.0785289 | 0.937543   |
| UroA_Treatment -> LiverLipidMetabolism     | UroA_Treatment | LiverLipidMetabolism     |  0.215722   |   0.0906616 |  2.37942   | 0.0189715  |
| UroA_Treatment -> LiverInjury              | UroA_Treatment | LiverInjury              |  0.102595   |   0.0923577 |  1.11084   | 0.268933   |
| UroA_Treatment -> FattyLiverSyndrome       | UroA_Treatment | FattyLiverSyndrome       |  0.187313   |   0.0912043 |  2.05378   | 0.0422452  |

### 字段解析与指标说明

| 字段 | 解释 | 生物学/统计学意义 |
| :--- | :--- | :--- |
| **from** | 起始变量 | 路径的自变量，即影响源。 |
| **to** | 目标变量 | 路径的因变量，即受影响的对象。 |
| **estimate** | 估计值 (路径系数) | 衡量自变量对因变量直接影响的大小和方向 (范围通常在 -1 到 1)。 |
| **std error** | 标准误 | 估计量的标准误差，反映估计的精确度。 |
| **t** | t 检验统计量 | 估计值除以标准误的值，绝对值越大越显著。 |
| **p>\|t\|** | p 值 | 判断显著性的核心指标。若 p < 0.05，认为对应的路径关系在统计上是显著的。 |

---

## Path Coefficients

|                          |   UroA_Treatment |   LayingPerformance |   LiverFatIndex |   LiverGlutamateMetabolism |   LiverAntioxidant |   LiverImmune |   LiverLipidMetabolism |   LiverInjury |   FattyLiverSyndrome |
|--------------------------|------------------|---------------------|-----------------|----------------------------|--------------------|---------------|------------------------|---------------|----------------------|
| UroA_Treatment           |       0          |                   0 |               0 |                          0 |                  0 |             0 |                      0 |             0 |                    0 |
| LayingPerformance        |       0.269007   |                   0 |               0 |                          0 |                  0 |             0 |                      0 |             0 |                    0 |
| LiverFatIndex            |       0.102972   |                   0 |               0 |                          0 |                  0 |             0 |                      0 |             0 |                    0 |
| LiverGlutamateMetabolism |       0.0937646  |                   0 |               0 |                          0 |                  0 |             0 |                      0 |             0 |                    0 |
| LiverAntioxidant         |      -0.0177863  |                   0 |               0 |                          0 |                  0 |             0 |                      0 |             0 |                    0 |
| LiverImmune              |      -0.00729103 |                   0 |               0 |                          0 |                  0 |             0 |                      0 |             0 |                    0 |
| LiverLipidMetabolism     |       0.215722   |                   0 |               0 |                          0 |                  0 |             0 |                      0 |             0 |                    0 |
| LiverInjury              |       0.102595   |                   0 |               0 |                          0 |                  0 |             0 |                      0 |             0 |                    0 |
| FattyLiverSyndrome       |       0.187313   |                   0 |               0 |                          0 |                  0 |             0 |                      0 |             0 |                    0 |

### 字段解析与指标说明

| 维度 | 解释 |
| :--- | :--- |
| **行(Row)** | 被影响的内生变量。 |
| **列(Column)** | 施加影响的自变量。 |
| **数值** | 对应路径的标准化系数。0 表示没有直接连接。 |

---

## R-Squared

|                          | type       |   r_squared |   r_squared_adj |   block_communality |   mean_redundancy |      ave |
|--------------------------|------------|-------------|-----------------|---------------------|-------------------|----------|
| FattyLiverSyndrome       | Endogenous | 0.0350862   |     0.026768    |            0.384762 |       0.0134999   | 0.384762 |
| LayingPerformance        | Endogenous | 0.0723647   |     0.0643678   |            0.313073 |       0.0226555   | 0.313073 |
| LiverAntioxidant         | Endogenous | 0.000316351 |    -0.00830161  |            0.823869 |       0.000260632 | 0.823869 |
| LiverFatIndex            | Endogenous | 0.0106032   |     0.0020739   |            0.920293 |       0.00975803  | 0.920293 |
| LiverGlutamateMetabolism | Endogenous | 0.0087918   |     0.000246906 |            0.945793 |       0.00831523  | 0.945793 |
| LiverImmune              | Endogenous | 5.31591e-05 |    -0.00856707  |            0.949972 |       5.04996e-05 | 0.949972 |
| LiverInjury              | Endogenous | 0.0105257   |     0.00199577  |            0.879151 |       0.0092537   | 0.879151 |
| LiverLipidMetabolism     | Endogenous | 0.046536    |     0.0383165   |            0.465299 |       0.0216532   | 0.465299 |
| UroA_Treatment           | Exogenous  | 0           |     0           |            1        |       0           | 1        |

### 字段解析与指标说明

| 指标 | 解释 | 理想范围 / 参考 |
| :--- | :--- | :--- |
| **type** | 变量类型 | Exogenous(外生，即只有输出路径) 或 Endogenous(内生，包含输入路径)。 |
| **r_squared** | R² (判定系数) | 反映内生变量方差被模型解释的比例。 | > 0.6 表示模型解释力较好。 |
| **r_squared_adj** | 调整后 R² | 考虑了自变量个数后的 R²，用于更公平地评价模型。 | 值越接近 R² 越好。 |
| **block_communality** | 块共同度 | 衡量该潜变量与其测量指标间的平均关联程度。 | 建议 > 0.7 |
| **ave** | 平均方差提取量 | 衡量潜变量对测量指标的平均方差贡献。 | 建议 > 0.5 (表示潜变量能解释过半的指标方差)。 |
| **mean_redundancy** | 平均冗余度 | 反映模型对内生变量测量指标的整体预测能力。 | 值越高表示预测性越强。 |

---

## Outer Model (Loadings)

|               |        weight |    loading |   communality |   redundancy |
|---------------|---------------|------------|---------------|--------------|
| ALT_1         |   0.20618     |  0.870836  |    0.758355   |  0.00798223  |
| AST_1         |   1.54615     |  0.999974  |    0.999948   |  0.0105252   |
| AST_2         |   1.48608     |  0.988168  |    0.976477   |  0.0342609   |
| AbdFatIndex_1 |  20.4071      |  0.997179  |    0.994366   |  0.0105434   |
| EggWeight_1   |  -1.29141     |  0.904039  |    0.817287   |  0.0591427   |
| FeedToEgg_1   |  -0.0956221   |  0.185567  |    0.0344349  |  0.00249187  |
| GDH_1         |   0.0227005   |  0.964226  |    0.929733   |  0.00817403  |
| GLS2_1        |   0.108889    |  0.972546  |    0.945847   |  0.0083157   |
| GOGAT_1       |   0.408407    |  0.964717  |    0.93068    |  0.00818235  |
| GSHPx_1       |  10.1749      |  0.720396  |    0.51897    |  0.000164177 |
| Gln_1         |   2.83881     |  0.999988  |    0.999976   |  0.0087916   |
| Glu_1         |   0.0104379   |  0.970082  |    0.941059   |  0.00827361  |
| IL6_2         |   0.0515037   |  0.442614  |    0.195908   |  0.00687366  |
| IgA_1         |   0.276093    |  0.999931  |    0.999862   |  5.31518e-05 |
| LayingRate_1  |   3.96285     | -0.295801  |    0.0874985  |  0.0063318   |
| LayingRate_2  |  -1.32311     | -0.0941615 |    0.00886639 |  0.000311088 |
| LiverIndex_1  |   7.13239     |  0.919902  |    0.846219   |  0.00897261  |
| LiverIndex_2  |   0.0339031   |  0.911989  |    0.831724   |  0.029182    |
| OilRedArea_1  |  19.2964      |  0.999911  |    0.999822   |  0.0465277   |
| TAOC_1        |   0.589664    |  0.976601  |    0.953749   |  0.000301719 |
| TC_1          |   0.099309    |  0.571692  |    0.326831   |  0.0152094   |
| TC_2          |   0.00122569  |  0.484212  |    0.234461   |  0.00822637  |
| TG_1          |   0.0550362   |  0.5757    |    0.331431   |  0.0154235   |
| TG_2          |   0.000679266 |  0.487482  |    0.237639   |  0.00833786  |
| TNFa_1        |  -0.22607     |  0.948726  |    0.900081   |  4.78475e-05 |
| TNFa_2        |   0.279245    |  0.456358  |    0.208263   |  0.00730716  |
| TSOD_1        |   8.3099      |  0.999445  |    0.998889   |  0.000315999 |
| UroA          | 460.39        | -1         |    1          |  0           |
| VLDLC_1       |   2.16532     |  0.45068   |    0.203113   |  0.00945206  |
| aKG_1         |   0.0747988   |  0.963048  |    0.927462   |  0.00815406  |

### 字段解析与指标说明

| 指标 | 解释 | 评价指标 |
| :--- | :--- | :--- |
| **weight** | 权重 (Outer Weights) | 各个测量指标对潜变量分数的贡献权重。 | 越大说明指标对潜变量的定义越重要。 |
| **loading** | 因子载荷 (Loadings) | 指标与潜变量的相关性。 | 建议 > 0.7 (表示指标对潜变量有高度代表性)。 |
| **communality** | 共同性 | loading 的平方，衡量潜变量对该指标方差的解释比例。 | 越高越好。 |
| **redundancy** | 冗余度 | 反映该指标通过模型被解释的程度。 | - |

---

## Effects

|                                            | from           | to                       |      direct |   indirect |       total |
|--------------------------------------------|----------------|--------------------------|-------------|------------|-------------|
| UroA_Treatment -> LayingPerformance        | UroA_Treatment | LayingPerformance        |  0.269007   |          0 |  0.269007   |
| UroA_Treatment -> LiverFatIndex            | UroA_Treatment | LiverFatIndex            |  0.102972   |          0 |  0.102972   |
| UroA_Treatment -> LiverGlutamateMetabolism | UroA_Treatment | LiverGlutamateMetabolism |  0.0937646  |          0 |  0.0937646  |
| UroA_Treatment -> LiverAntioxidant         | UroA_Treatment | LiverAntioxidant         | -0.0177863  |          0 | -0.0177863  |
| UroA_Treatment -> LiverImmune              | UroA_Treatment | LiverImmune              | -0.00729103 |          0 | -0.00729103 |
| UroA_Treatment -> LiverLipidMetabolism     | UroA_Treatment | LiverLipidMetabolism     |  0.215722   |          0 |  0.215722   |
| UroA_Treatment -> LiverInjury              | UroA_Treatment | LiverInjury              |  0.102595   |          0 |  0.102595   |
| UroA_Treatment -> FattyLiverSyndrome       | UroA_Treatment | FattyLiverSyndrome       |  0.187313   |          0 |  0.187313   |

### 字段解析与指标说明

| 字段 | 解释 |
| :--- | :--- |
| **direct** | 直接效应 | 两个变量之间直接连线的路径系数。 |
| **indirect** | 间接效应 | 通过路径中其他中介变量传递的影响。 |
| **total** | 总效应 | 直接效应 + 间接效应。反映一个变量对另一个变量的总影响力强度。 |

---

