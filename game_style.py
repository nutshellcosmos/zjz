# -*- coding: utf-8 -*-
# UI美化文件｜【纯浅色模式、删除全部深色冗余代码】
import streamlit as st

# 页面基础配置
PAGE_TITLE = "万古松风｜张居正"
PAGE_LAYOUT = "wide"

# 全局古风CSS（✅修复所有语法错误，标题大小强制生效）
CSS_STYLE = """
<style>
/* 全局背景 */
.main {
    background-color: #f8f2e4;
}

/* 全局字体：修复语法错误 */
html, body, .stMarkdown p {
    font-family: 楷体 !important;
    font-size: 18px !important;
}

/* 👇 这里就是你要改的标题大小！！！ */
h1, h2, h3 {
    color: #5c1010 !important;
    font-family: 楷体 !important;
    font-weight: bold !important;
    font-size: 24px !important;  /* 想变小就改这个数字：24 → 22 → 20 → 18 */
}

/* 自定义分割线 */
hr {
    border: none;
    height: 2px;
    background: linear-gradient(to right, transparent, #8c6e42, transparent);
    margin: 10px 0;
    border-radius: 2px;
}

/* 选项按钮 */
.stButton>button {
    background: linear-gradient(145deg, #8c6e42, #6b5232);
    color: #fff9e8;
    border-radius: 8px;
    padding: 10px 26px;
    font-size: 16px;
    border: none;
    box-shadow: 0 2px 6px #c9b99e;
    transition: 0.2s;
}
.stButton>button:hover {
    background: #9c7c52;
    transform: scale(1.02);
    box-shadow: 0 3px 10px #b8a488;
}

/* 侧边栏 */
[data-testid="stSidebar"] {
    background-color: #ebe3d5;
}
[data-testid="stSidebar"] hr {
    display: none;
}
</style>
"""

# 通用黄框（纯浅色原版样式）
STORY_BOX = """
<p style="background:#fff6e8;padding:30px 40px;border-radius:12px;font-size:18px;line-height:2.2;text-indent:2em;text-align:justify;margin-top:15px;margin-bottom:15px;border:1px solid #e9dfcd;box-shadow:0 2px 8px #e2d6c0;color:#120b04;">{}</p>
"""

# 侧边栏文字
SIDEBAR_TITLE = "📜 张居正极简面板"
SIDEBAR_WARN = "🐢 愿以深心奉尘刹，不予自身求利益。"

# 进度条（满分100、修复负数BUG：负数强制归0）
def get_bar_html(name,color,num,max_num=100):
    if num < 0:
        num = 0
    percent = min(num/max_num*100,100)
    html = f"""
<p style="margin:4px 0px;font-size:15px;color:#4b2b1b;">{name}：{num}/{max_num}</p>
<div style="width:100%;height:14px;background:#d9cdbc;border-radius:7px;overflow:hidden;margin-bottom:12px;">
<div style="width:{percent}%;height:100%;background:{color};border-radius:7px;transition:0.4s;"></div>
</div>
"""
    return html

# 结局专属背景色
ENDING_SUCCESS = "background:#f9f1d9;border:1px solid #e2c894;"
ENDING_FAIL = "background:#4b1c1c;border:1px solid #7a2e2e;color:#f8e8e8;"
ENDING_NORMAL = "background:#f0ebe1;border:1px solid #d3c7b4;"