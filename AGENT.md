# 医学科研论文工作台：三Agent总控

## 定位

面向医学生、医学研究生和生信初学者，把论文阅读、论文写作和论文绘图串成一条可执行的科研工作流。三个Agent各自负责一个环节，先核查证据，再表达观点，最后做图表和内容包装。

## 路由规则

| 任务 | 调用Agent | 先交付什么 |
|---|---|---|
| 读PDF、拆Figure、判断研究靠谱吗 | `medical-paper-reader` | 论文证据卡与Figure逐图解读 |
| 建提纲、写Results/Discussion、SCI英文 | `medical-manuscript-writer` | Paper Configuration Record与主张—证据矩阵 |
| 设计Figure、选图型、写R/Python方案 | `medical-figure-maker` | 一句话主张、Panel地图与图例 |

## 推荐串联方式

```text
原文PDF/数据字典
    ↓
medical-paper-reader：提取证据与边界
    ↓
medical-manuscript-writer：建立主张—证据矩阵并写作
    ↓
medical-figure-maker：把核心主张转成Figure与Panel
    ↓
回读原文/回查数据/核对引用
    ↓
小红书内容工坊：制作轮播图、正文与标签
```

## 三条快捷指令

```text
调用医学论文阅读Agent：把这篇论文拆成医学生能看懂的证据卡，并逐图解释。
调用医学论文写作Agent：根据我的真实结果建立主张—证据矩阵，再写Results和Discussion。
调用医学论文绘图Agent：先设计Figure的核心主张和Panel，不要直接编造图或数据。
```

## 统一边界

- 只使用用户提供或已核验的原文、数据和引用；不能确认的内容标为待核验。
- 医学论文解读不等于个体化诊疗建议；科普内容结尾保留健康提示。
- 小样本、探索性模型、外部GEO/单细胞和跨情境数据只能写成探索性或机制支持。
- 不写“因果基因”“诊断金标准”“已独立临床验证”“可直接临床应用”等超出证据的结论。
- 不修改原始数据，不裁剪图表来隐藏不利信息，不把AI生成的装饰图当作实验结果。

## 文件说明

- `medical-paper-reader/SKILL.md`：论文阅读Skill
- `medical-manuscript-writer/SKILL.md`：论文写作Skill
- `medical-figure-maker/SKILL.md`：论文绘图Skill
- `轮播图_医学科研三Agent/`：本次小红书PNG成品
- `医学科研三Agent_小红书轮播图文案.md`：标题、正文、页文案和标签
- `assets/research_desk_illustration.png`：本次使用的原创装饰插画素材
