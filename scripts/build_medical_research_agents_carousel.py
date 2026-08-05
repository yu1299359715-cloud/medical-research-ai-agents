from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


W, H = 1600, 2133
DPI = 600
CREAM = "#FBF6ED"
PAPER = "#FFFDF8"
BROWN = "#4B342A"
MUTED = "#806B5E"
TERRACOTTA = "#B85F45"
TERRACOTTA_DARK = "#8F4435"
SAGE = "#7C8B70"
MUSTARD = "#D7A44D"
PEACH = "#F2E4D7"
LINE = "#E6D5C3"
PALE_GREEN = "#E6E9DD"
WHITE = "#FFFFFF"

FONT_REG = r"C:\Windows\Fonts\msyh.ttc"
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
GITHUB_OWNER_REPO = "yu1299359715-cloud/medical-research-ai-agents"


def font(size: int, bold: bool = False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def text_width(draw: ImageDraw.ImageDraw, text: str, fnt) -> float:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0]


def wrap_text(draw: ImageDraw.ImageDraw, text: str, fnt, max_width: int):
    lines = []
    for paragraph in text.split("\n"):
        if not paragraph:
            lines.append("")
            continue
        current = ""
        for ch in paragraph:
            candidate = current + ch
            if current and text_width(draw, candidate, fnt) > max_width:
                lines.append(current)
                current = ch
            else:
                current = candidate
        if current:
            lines.append(current)
    return lines


def draw_wrapped(draw, xy, text, fnt, fill=BROWN, max_width=1300, line_spacing=16):
    x, y = xy
    lines = wrap_text(draw, text, fnt, max_width)
    line_h = fnt.size + line_spacing
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += line_h
    return y


def rounded(draw, box, radius=28, fill=PAPER, outline=None, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def pill(draw, x, y, label, fill=PEACH, text_fill=TERRACOTTA_DARK, pad_x=24, h=54, size=30):
    fnt = font(size, True)
    tw = text_width(draw, label, fnt)
    rounded(draw, (x, y, x + tw + pad_x * 2, y + h), radius=h // 2, fill=fill)
    draw.text((x + pad_x, y + (h - size) // 2 - 3), label, font=fnt, fill=text_fill)
    return x + tw + pad_x * 2


def header(draw, page_no, section="医学科研工作台"):
    draw.text((100, 84), section, font=font(30, True), fill=TERRACOTTA)
    draw.text((W - 210, 84), f"{page_no:02d} / 12", font=font(30, True), fill=MUTED)
    draw.line((100, 148, W - 100, 148), fill=LINE, width=3)


def footer(draw, label="科研党今天少走一个弯路"):
    draw.line((100, H - 118, W - 100, H - 118), fill=LINE, width=2)
    draw.text((100, H - 86), label, font=font(26), fill=MUTED)
    draw.text((W - 420, H - 86), "收藏后按步骤练习", font=font(26, True), fill=TERRACOTTA)


def number_badge(draw, x, y, number, color=TERRACOTTA):
    draw.ellipse((x, y, x + 70, y + 70), fill=color)
    fnt = font(34, True)
    label = str(number)
    tw = text_width(draw, label, fnt)
    draw.text((x + (70 - tw) / 2, y + 13), label, font=fnt, fill=WHITE)


def bullet(draw, x, y, text, max_width=1180, color=BROWN, accent=TERRACOTTA, size=38):
    draw.ellipse((x, y + 15, x + 18, y + 33), fill=accent)
    return draw_wrapped(draw, (x + 40, y), text, font(size), color, max_width, 12)


def label_value(draw, x, y, label, value, width=620):
    draw.text((x, y), label, font=font(30, True), fill=TERRACOTTA)
    draw_wrapped(draw, (x, y + 52), value, font(36), BROWN, width, 10)


def paste_illustration(canvas, asset_path, box, alpha=255):
    if not asset_path.exists():
        return
    img = Image.open(asset_path).convert("RGBA")
    contained = ImageOps.contain(img, (box[2] - box[0], box[3] - box[1]))
    if alpha != 255:
        contained.putalpha(contained.getchannel("A").point(lambda p: int(p * alpha / 255)))
    x = box[0] + (box[2] - box[0] - contained.width) // 2
    y = box[1] + (box[3] - box[1] - contained.height) // 2
    canvas.alpha_composite(contained, (x, y))


def base():
    return Image.new("RGBA", (W, H), CREAM)


def save_page(img, out_dir: Path, page_no: int):
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{page_no:02d}_医学生科研三Agent.png"
    img.convert("RGB").save(out, format="PNG", dpi=(DPI, DPI), optimize=True)
    return out


def page_cover(asset):
    img = base()
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, W, 22), fill=TERRACOTTA)
    pill(draw, 100, 96, "医学生科研工作流·01", fill=PEACH)
    draw_wrapped(draw, (100, 260), "医学生科研\n别从空白开始", font(102, True), BROWN, 980, 14)
    draw_wrapped(draw, (106, 580), "3个AI Agent，把读论文、写论文、画论文图串起来", font(48), TERRACOTTA_DARK, 840, 14)
    rounded(draw, (100, 790, 940, 985), radius=34, fill=WHITE, outline=LINE, width=3)
    draw_wrapped(draw, (148, 838), "适合：临床科研｜基础实验｜生物信息学入门\n重点：先核查证据，再让AI帮你表达", font(37), BROWN, 740, 14)
    draw_wrapped(draw, (100, 1090), "三个Agent｜名称 + GitHub地址", font(42, True), TERRACOTTA)
    agents = [
        ("01", "医学论文阅读 Agent", "medical-paper-reader", TERRACOTTA),
        ("02", "医学论文写作 Agent", "medical-manuscript-writer", SAGE),
        ("03", "医学论文绘图 Agent", "medical-figure-maker", MUSTARD),
    ]
    y = 1180
    for no, title, slug, color in agents:
        rounded(draw, (100, y, 1500, y + 205), radius=30, fill=WHITE, outline=LINE, width=3)
        draw.rectangle((100, y, 126, y + 205), fill=color)
        draw.ellipse((155, y + 56, 235, y + 136), fill=color)
        draw.text((177, y + 73), no, font=font(28, True), fill=WHITE)
        draw.text((285, y + 28), title, font=font(40, True), fill=BROWN)
        draw.text((285, y + 91), slug, font=font(30), fill=MUTED)
        draw.text((1000, y + 24), "GitHub仓库", font=font(21, True), fill=TERRACOTTA_DARK)
        draw.text((1000, y + 58), "yu1299359715-cloud/", font=font(21), fill=MUTED)
        draw.text((1000, y + 88), "medical-research-ai-agents", font=font(21), fill=MUTED)
        draw.text((1000, y + 118), f"skills/{slug}", font=font(21, True), fill=TERRACOTTA_DARK)
        y += 235
    footer(draw)
    return img


def page_overview():
    img = base(); draw = ImageDraw.Draw(img); header(draw, 2)
    draw_wrapped(draw, (100, 220), "别把AI当答案机\n把它用成科研工作台", font(80, True), BROWN, 1260, 14)
    draw_wrapped(draw, (104, 430), "一篇论文真正的工作，不只是“看懂”，还要能形成证据、写成段落、画成图。", font(40), MUTED, 1250, 12)
    cards = [
        ("01", "论文阅读 Agent", "把PDF拆成\n研究问题、设计、结果和局限性", TERRACOTTA),
        ("02", "论文写作 Agent", "把真实数据组织成\n提纲、主张—证据矩阵和段落", SAGE),
        ("03", "论文绘图 Agent", "把核心结论转成\nFigure、Panel、图例和导出方案", MUSTARD),
    ]
    y = 650
    for no, title, body, color in cards:
        rounded(draw, (100, y, 1500, y + 280), radius=36, fill=WHITE, outline=LINE, width=3)
        number_badge(draw, 140, y + 46, no, color)
        draw.text((250, y + 42), title, font=font(48, True), fill=BROWN)
        draw_wrapped(draw, (250, y + 116), body, font(36), MUTED, 1050, 8)
        y += 340
    rounded(draw, (100, 1700, 1500, 1900), radius=34, fill=PEACH)
    draw_wrapped(draw, (145, 1750), "核心原则：AI负责整理和表达，作者负责核对原文、数据和结论。", font(40, True), TERRACOTTA_DARK, 1240, 12)
    footer(draw)
    return img


def page_prepare():
    img = base(); draw = ImageDraw.Draw(img); header(draw, 3)
    draw_wrapped(draw, (100, 220), "开始之前，先准备4样东西", font(78, True), BROWN, 1280, 14)
    draw_wrapped(draw, (104, 415), "材料越具体，AI越不容易“看起来会写、实际上不可靠”。", font(40), MUTED, 1250, 12)
    items = [
        ("原文", "PDF、DOI或期刊页面；不要只给标题。"),
        ("研究问题", "你想回答什么，目标读者是谁？"),
        ("真实结果", "表格、统计输出、Figure和数据字典。"),
        ("证据边界", "哪些是探索性结果，哪些还需要验证？"),
    ]
    y = 650
    for i, (title, body) in enumerate(items, 1):
        rounded(draw, (130, y, 1470, y + 220), radius=30, fill=WHITE, outline=LINE, width=3)
        number_badge(draw, 176, y + 68, i, TERRACOTTA if i % 2 else SAGE)
        draw.text((290, y + 48), title, font=font(44, True), fill=BROWN)
        draw_wrapped(draw, (290, y + 112), body, font(34), MUTED, 1080, 8)
        y += 275
    rounded(draw, (130, 1785, 1470, 1940), radius=26, fill=PALE_GREEN)
    draw_wrapped(draw, (175, 1828), "建议：先让Agent列“待确认项”，再开始写作。", font(36, True), BROWN, 1200, 10)
    footer(draw)
    return img


def page_reader():
    img = base(); draw = ImageDraw.Draw(img); header(draw, 4, "01 · 论文阅读 Agent")
    draw_wrapped(draw, (100, 220), "Agent 01｜先把论文读对", font(78, True), BROWN, 1300, 14)
    draw_wrapped(draw, (104, 420), "它不是替你“总结摘要”，而是帮你建立一张可核查的证据卡。", font(40), MUTED, 1250, 12)
    rounded(draw, (100, 620, 1500, 1065), radius=36, fill=WHITE, outline=LINE, width=3)
    pill(draw, 150, 675, "输入", fill=PEACH)
    draw_wrapped(draw, (150, 755), "PDF / DOI / 论文截图 / 你的疑问", font(44, True), BROWN, 1240, 10)
    draw.line((800, 735, 800, 1000), fill=LINE, width=3)
    pill(draw, 880, 675, "输出", fill=PALE_GREEN, text_fill=SAGE)
    draw_wrapped(draw, (880, 755), "研究问题\n研究设计\nFigure逐图解读\n证据强度与局限性", font(40), BROWN, 520, 11)
    draw_wrapped(draw, (100, 1175), "可复制提示词", font(42, True), TERRACOTTA)
    rounded(draw, (100, 1255, 1500, 1660), radius=30, fill=PEACH)
    draw_wrapped(draw, (150, 1310), "请阅读这篇医学论文：先判断研究类型，再提取研究问题、样本量、分组、主要结局和统计方法；逐图说明每个Figure回答什么、关键结果是什么，以及不能过度推出什么。", font(35), BROWN, 1300, 13)
    rounded(draw, (100, 1740, 1500, 1910), radius=28, fill=PALE_GREEN)
    draw_wrapped(draw, (145, 1783), "重点：原文没有报告的数字，统一写“未报告”，不要猜。", font(36, True), BROWN, 1280, 10)
    footer(draw)
    return img


def page_reader_flow():
    img = base(); draw = ImageDraw.Draw(img); header(draw, 5, "01 · 论文阅读 Agent")
    draw_wrapped(draw, (100, 220), "读论文的10分钟流程", font(78, True), BROWN, 1300, 14)
    draw_wrapped(draw, (104, 410), "先抓研究骨架，再回到Figure看证据，最后检查它没有说什么。", font(40), MUTED, 1250, 12)
    steps = [
        ("1", "研究了谁", "人群 / 样本 / 数据集"),
        ("2", "怎么分组", "暴露、干预、对照或标签"),
        ("3", "测了什么", "主要结局、指标与时间点"),
        ("4", "怎么分析", "统计方法、模型和验证"),
        ("5", "图里发现", "先看比较，再看效应量"),
        ("6", "边界在哪", "相关≠因果，探索≠验证"),
    ]
    y = 650
    for i, (no, title, body) in enumerate(steps):
        x = 120 if i % 2 == 0 else 830
        yy = y + (i // 2) * 245
        rounded(draw, (x, yy, x + 630, yy + 185), radius=28, fill=WHITE, outline=LINE, width=3)
        number_badge(draw, x + 34, yy + 52, no, TERRACOTTA if i % 2 == 0 else SAGE)
        draw.text((x + 140, yy + 38), title, font=font(38, True), fill=BROWN)
        draw_wrapped(draw, (x + 140, yy + 96), body, font(31), MUTED, 435, 8)
    rounded(draw, (100, 1500, 1500, 1830), radius=32, fill=PEACH)
    draw_wrapped(draw, (150, 1555), "读图提问句：\n“这张图首先比较了什么？差异有多大？误差和样本量在哪里？这个结果只支持到哪一步？”", font(38, True), TERRACOTTA_DARK, 1290, 12)
    footer(draw)
    return img


def page_writer():
    img = base(); draw = ImageDraw.Draw(img); header(draw, 6, "02 · 论文写作 Agent")
    draw_wrapped(draw, (100, 220), "Agent 02｜先搭证据链，再写句子", font(76, True), BROWN, 1300, 14)
    draw_wrapped(draw, (104, 420), "不要一上来就说“帮我写全文”。论文写作更适合分层推进。", font(40), MUTED, 1250, 12)
    stages = [
        ("A", "研究问题", "这篇研究到底要回答什么？"),
        ("B", "主张", "每一段想让读者相信什么？"),
        ("C", "证据", "哪张图、哪张表、哪个统计结果支持它？"),
        ("D", "边界", "哪些结论还不能写得更强？"),
    ]
    y = 650
    for no, title, body in stages:
        rounded(draw, (120, y, 1480, y + 190), radius=28, fill=WHITE, outline=LINE, width=3)
        draw.ellipse((160, y + 55, 250, y + 145), fill=SAGE if no in ("B", "D") else TERRACOTTA)
        draw.text((190, y + 73), no, font=font(36, True), fill=WHITE)
        draw.text((310, y + 42), title, font=font(42, True), fill=BROWN)
        draw_wrapped(draw, (310, y + 105), body, font(34), MUTED, 1040, 8)
        y += 235
    rounded(draw, (120, 1640, 1480, 1880), radius=30, fill=PALE_GREEN)
    draw_wrapped(draw, (170, 1695), "写作提示：先生成提纲和主张—证据矩阵，再让AI写段落。这样你能逐句核对，而不是被一篇“看起来很SCI”的文字带着走。", font(36, True), BROWN, 1240, 11)
    footer(draw)
    return img


def page_matrix():
    img = base(); draw = ImageDraw.Draw(img); header(draw, 7, "02 · 论文写作 Agent")
    draw_wrapped(draw, (100, 220), "最值得收藏的：主张—证据矩阵", font(74, True), BROWN, 1320, 14)
    draw_wrapped(draw, (104, 410), "它能防止Results写成“把图表从头念一遍”，也能提醒你哪些话没有数据支持。", font(40), MUTED, 1250, 12)
    x0, y0 = 120, 670
    col_widths = [250, 480, 300, 370]
    headers = ["段落主张", "证据/数据", "对应图表", "表述边界"]
    rows = [
        ["研究发现", "真实效应量、CI、P值、n", "Figure 2", "只写相关或组间差异"],
        ["机制线索", "通路、细胞定位、外部支持", "Figure 4", "写成支持，不写因果"],
        ["模型表现", "训练/验证、AUC、校准", "Figure 5", "写候选，不写诊断金标准"],
    ]
    x = x0
    for w, htext in zip(col_widths, headers):
        draw.rectangle((x, y0, x + w, y0 + 105), fill=TERRACOTTA)
        draw_wrapped(draw, (x + 20, y0 + 28), htext, font(30, True), WHITE, w - 40, 6)
        x += w
    y = y0 + 105
    for ridx, row in enumerate(rows):
        x = x0
        fill = WHITE if ridx % 2 == 0 else PEACH
        for w, val in zip(col_widths, row):
            draw.rectangle((x, y, x + w, y + 185), fill=fill, outline=LINE, width=2)
            draw_wrapped(draw, (x + 20, y + 28), val, font(30, ridx == 0), BROWN, w - 40, 8)
            x += w
        y += 185
    rounded(draw, (120, 1480, 1480, 1835), radius=30, fill=PEACH)
    draw_wrapped(draw, (170, 1535), "一句结果段骨架：\n“在【研究对象】中，【指标】在【分组】之间出现【方向/效应量】差异（【统计量】），提示【谨慎解释】。”", font(37, True), TERRACOTTA_DARK, 1240, 12)
    footer(draw)
    return img


def page_figure():
    img = base(); draw = ImageDraw.Draw(img); header(draw, 8, "03 · 论文绘图 Agent")
    draw_wrapped(draw, (100, 220), "Agent 03｜先决定一张图要说什么", font(76, True), BROWN, 1300, 14)
    draw_wrapped(draw, (104, 420), "好Figure不是信息越多越好，而是读者能快速找到一个核心结论。", font(40), MUTED, 1250, 12)
    rounded(draw, (100, 650, 1500, 1000), radius=34, fill=WHITE, outline=LINE, width=3)
    pill(draw, 150, 705, "第一步", fill=PEACH)
    draw_wrapped(draw, (150, 790), "写出一句话核心主张：\n“这张图想让读者相信什么？”", font(48, True), TERRACOTTA_DARK, 1200, 12)
    draw_wrapped(draw, (100, 1130), "第二步：给每个Panel安排任务", font(42, True), TERRACOTTA)
    roles = [
        ("A", "定义", "研究对象 / 流程 / 分组"),
        ("B", "主要证据", "最关键的比较和效应量"),
        ("C", "验证", "独立队列、外部数据或新情境"),
        ("D", "机制/转化", "通路、细胞定位或实际意义"),
    ]
    y = 1230
    for i, (letter, title, body) in enumerate(roles):
        x = 120 + (i % 2) * 720
        yy = y + (i // 2) * 230
        rounded(draw, (x, yy, x + 620, yy + 175), radius=26, fill=PALE_GREEN if i % 2 else PEACH, outline=LINE, width=2)
        draw.ellipse((x + 30, yy + 48, x + 105, yy + 123), fill=SAGE if i % 2 else TERRACOTTA)
        draw.text((x + 56, yy + 65), letter, font=font(30, True), fill=WHITE)
        draw.text((x + 145, yy + 28), title, font=font(36, True), fill=BROWN)
        draw_wrapped(draw, (x + 145, yy + 88), body, font(30), MUTED, 430, 7)
    footer(draw)
    return img


def page_figure_check():
    img = base(); draw = ImageDraw.Draw(img); header(draw, 9, "03 · 论文绘图 Agent")
    draw_wrapped(draw, (100, 220), "论文图的发表级检查清单", font(76, True), BROWN, 1300, 14)
    checks = [
        ("内容", "每张主图只有一个主张；Panel字母和图例对应。"),
        ("统计", "写清n、误差线定义、检验方法、效应量和P值。"),
        ("可读", "轴标题含单位；最终尺寸下文字仍能放大看清。"),
        ("配色", "色盲友好；不要用彩虹色和红绿色组合。"),
        ("格式", "优先PDF/SVG；栅格图PNG/TIFF，300–600 DPI。"),
        ("边界", "相关不写因果；候选标志物不写诊断金标准。"),
    ]
    y = 610
    for i, (title, body) in enumerate(checks, 1):
        rounded(draw, (125, y, 1475, y + 195), radius=26, fill=WHITE, outline=LINE, width=3)
        draw.rounded_rectangle((160, y + 58, 225, y + 123), radius=14, fill=SAGE if i % 2 else TERRACOTTA)
        draw.text((177, y + 70), "✓", font=font(32, True), fill=WHITE)
        draw.text((280, y + 36), title, font=font(38, True), fill=BROWN)
        draw_wrapped(draw, (280, y + 102), body, font(32), MUTED, 1080, 8)
        y += 225
    rounded(draw, (125, 1900, 1475, 2010), radius=22, fill=PEACH)
    draw.text((170, 1932), "记住：图表是证据，不是装饰。", font=font(34, True), fill=TERRACOTTA_DARK)
    footer(draw)
    return img


def page_scenarios():
    img = base(); draw = ImageDraw.Draw(img); header(draw, 10)
    draw_wrapped(draw, (100, 220), "临床、基础、生信都能这样用", font(76, True), BROWN, 1320, 14)
    draw_wrapped(draw, (104, 420), "换的是研究材料，不换的是“问题—证据—边界”的顺序。", font(40), MUTED, 1250, 12)
    scenarios = [
        ("临床队列", "先看人群、暴露、结局和混杂；\nResults保留效应量与置信区间；\n报告规范优先看STROBE。", TERRACOTTA),
        ("基础/细胞", "先确认模型、对照、干预和终点；\n动物/细胞结果不能直接写成人体疗效；\n图里标清重复和误差线。", SAGE),
        ("生物信息学", "先核对数据集、基因ID和分析流程；\n模型写清训练/验证和外部支持；\n小样本结果默认探索性。", MUSTARD),
    ]
    y = 650
    for title, body, color in scenarios:
        rounded(draw, (120, y, 1480, y + 300), radius=32, fill=WHITE, outline=LINE, width=3)
        draw.rectangle((120, y, 1480, y + 18), fill=color)
        draw.text((170, y + 58), title, font=font(46, True), fill=BROWN)
        draw_wrapped(draw, (170, y + 140), body, font(35), MUTED, 1240, 10)
        y += 350
    rounded(draw, (120, 1740, 1480, 1930), radius=30, fill=PALE_GREEN)
    draw_wrapped(draw, (170, 1790), "同一条底线：先回到原文和真实数据，再让AI帮你翻译、组织和表达。", font(38, True), BROWN, 1240, 10)
    footer(draw)
    return img


def page_pipeline():
    img = base(); draw = ImageDraw.Draw(img); header(draw, 11)
    draw_wrapped(draw, (100, 220), "从PDF到论文图：完整工作流", font(76, True), BROWN, 1300, 14)
    draw_wrapped(draw, (104, 415), "把一次科研任务拆成几个可检查的小节点，效率和可靠性都会更高。", font(40), MUTED, 1250, 12)
    flow = ["原文/数据", "读论文", "证据矩阵", "写作", "Figure", "最终核查"]
    y = 690
    for i, node in enumerate(flow):
        x = 120 + i * 242
        rounded(draw, (x, y, x + 190, y + 135), radius=24, fill=PEACH if i % 2 == 0 else PALE_GREEN, outline=LINE, width=2)
        draw_wrapped(draw, (x + 18, y + 45), node, font(30, True), BROWN, 155, 6)
        if i < len(flow) - 1:
            draw.line((x + 195, y + 67, x + 232, y + 67), fill=TERRACOTTA, width=5)
            draw.polygon([(x + 232, y + 67), (x + 216, y + 57), (x + 216, y + 77)], fill=TERRACOTTA)
    commands = [
        ("读论文", "把这篇论文拆成研究设计、Figure逐图和证据边界。"),
        ("写论文", "先建立主张—证据矩阵，再写Results段。"),
        ("画论文图", "先给出核心主张、Panel地图和图例，再选择图型。"),
    ]
    y = 1050
    for title, body in commands:
        rounded(draw, (120, y, 1480, y + 210), radius=26, fill=WHITE, outline=LINE, width=3)
        pill(draw, 165, y + 32, title, fill=PEACH if title != "画论文图" else PALE_GREEN, text_fill=TERRACOTTA_DARK if title != "画论文图" else SAGE, h=58, size=30)
        draw_wrapped(draw, (165, y + 112), body, font(34), BROWN, 1250, 8)
        y += 250
    rounded(draw, (120, 1860, 1480, 1980), radius=24, fill=PEACH)
    draw.text((170, 1897), "不要追求一次生成全文，追求每一步都能核对。", font=font(34, True), fill=TERRACOTTA_DARK)
    footer(draw)
    return img


def page_checklist(asset):
    img = base(); draw = ImageDraw.Draw(img); header(draw, 12)
    draw_wrapped(draw, (100, 220), "保存这张清单", font(86, True), BROWN, 1000, 14)
    draw_wrapped(draw, (104, 440), "AI辅助科研的正确打开方式：\n让它帮你少走弯路，不替你制造证据。", font(44), TERRACOTTA_DARK, 980, 12)
    checklist = [
        "我读过原文，而不是只看AI摘要",
        "我核对了样本量、数字、图例和统计方法",
        "我把相关、预测、机制线索和因果分开了",
        "我没有把探索性结果包装成临床结论",
        "我保留了引用、数据和Figure的来源",
    ]
    y = 780
    for item in checklist:
        draw.ellipse((130, y + 8, 190, y + 68), fill=SAGE)
        draw.text((145, y + 12), "✓", font=font(32, True), fill=WHITE)
        draw_wrapped(draw, (230, y), item, font(36, True), BROWN, 1180, 7)
        y += 125
    rounded(draw, (100, 1490, 1500, 1815), radius=32, fill=WHITE, outline=LINE, width=3)
    draw_wrapped(draw, (150, 1540), "给医学生的建议：\n先用一篇论文练习“读—写—画”闭环，再把自己的课题接进来。", font(42, True), BROWN, 1280, 12)
    pill(draw, 150, 1880, "收藏后按这12页练习", fill=PEACH, text_fill=TERRACOTTA_DARK, h=66, size=34)
    paste_illustration(img, asset, (1030, 205, 1510, 680), alpha=90)
    footer(draw)
    return img


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", default="小红书AI医学生信工作台/07_医学科研论文工作台/轮播图_医学科研三Agent")
    parser.add_argument("--asset", default="小红书AI医学生信工作台/07_医学科研论文工作台/assets/research_desk_illustration.png")
    args = parser.parse_args()
    out_dir = Path(args.out_dir)
    asset = Path(args.asset)
    pages = [
        page_cover(asset), page_overview(), page_prepare(), page_reader(),
        page_reader_flow(), page_writer(), page_matrix(), page_figure(),
        page_figure_check(), page_scenarios(), page_pipeline(), page_checklist(asset)
    ]
    outputs = [save_page(page, out_dir, i) for i, page in enumerate(pages, 1)]
    print(f"generated={len(outputs)}")
    for out in outputs:
        print(out)


if __name__ == "__main__":
    main()
