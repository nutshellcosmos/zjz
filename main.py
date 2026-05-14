# -*- coding: utf-8 -*-
# 主程序｜纯净浅色版 无多余居中代码
import streamlit as st
import base64
import os

from game_text import *
from game_style import *

#自定义的标题样式
def custom_title(text, top_margin="-60px", bottom_margin="0px"):
    # top_margin 可以根据需要调整，负值越大越靠上
    st.markdown(f'''
        <h1 style="margin-top: {top_margin}; bottom_margin: {bottom_margin}; color: #5c1010; font-family: 楷体;">
            {text}
        </h1>
    ''', unsafe_allow_html=True)
    
    
# 存档初始化
def init_data():
    if "chapter" not in st.session_state:
        st.session_state.chapter = 0
    if "status" not in st.session_state:
        st.session_state.status = {"声望":35,"皇权":15,"谋略":75,"赤诚":85}
    if "page" not in st.session_state:
        st.session_state.page = "start"
    if "choice_feedback" not in st.session_state:
        st.session_state.choice_feedback = ""
    if "confirm_next" not in st.session_state:
        st.session_state.confirm_next = False
    if "hidden_ending" not in st.session_state:
        st.session_state.hidden_ending = False
# 侧边栏
def show_side():
    side = st.sidebar
    side.title(SIDEBAR_TITLE)
    side.markdown(get_bar_html("🏛️ 朝野声望","#b89768",st.session_state.status["声望"]),unsafe_allow_html=True)
    side.markdown(get_bar_html("👑 皇权好感","#a82020",st.session_state.status["皇权"]),unsafe_allow_html=True)
    side.markdown(get_bar_html("🧠 治世谋略","#3c5480",st.session_state.status["谋略"]),unsafe_allow_html=True)
    side.markdown(get_bar_html("❤️ 家国赤诚","#c72c41",st.session_state.status["赤诚"]),unsafe_allow_html=True)
    #side.divider()
    side.error(SIDEBAR_WARN)
    if side.button("🔄 重开一局"):
        st.session_state.clear()
        st.rerun()
# 开局页
def page_start():
    custom_title("📜 万古松风 | 角色扮演")
    st.subheader("你将扮演：铁腕首辅｜张居正")
    st.markdown("",unsafe_allow_html=True)
    st.markdown(STORY_BOX.format(START_INTRO),unsafe_allow_html=True)
    st.markdown("<div style='margin-top: 20px'></div>", unsafe_allow_html=True)
    if st.button("✅ 入局大明，化身张居正"):
        st.session_state.page = "play"
        st.rerun()
# 游玩页
def page_play():
    cid = st.session_state.chapter
    data = CHAPTER_LIST[cid]
    # 在 main.py 的 page_play 函数中
    st.markdown(f"<h1 style='margin-top: -60px;'>{data['title']}</h1>", unsafe_allow_html=True)
    st.markdown(STORY_BOX.format(data["story"]),unsafe_allow_html=True)
    feedback_texts = CHOICE_FEEDBACK_TEXTS
    if not st.session_state.confirm_next:
        opt1 = st.button(data["opts"][0])
        opt2 = st.button(data["opts"][1])
        opt3 = st.button(data["opts"][2])
        effects = data["effect"]
        def change_attr(e, feedback):
            st.session_state.status["声望"] += e["声望"]
            st.session_state.status["皇权"] += e["皇权"]
            st.session_state.status["谋略"] += e["谋略"]
            st.session_state.status["赤诚"] += e["赤诚"]
            for key in st.session_state.status:
                if st.session_state.status[key] > 100: st.session_state.status[key] = 100
                if st.session_state.status[key] < 0: st.session_state.status[key] = 0
            st.session_state.choice_feedback = feedback
            st.session_state.confirm_next = True
            st.rerun()
        if opt1: change_attr(effects[0], feedback_texts[cid][0])
        if opt2: change_attr(effects[1], feedback_texts[cid][1])
        if opt3: change_attr(effects[2], feedback_texts[cid][2])
    else:
        st.markdown(f"""<p style="color:#5C3A21;font-size:18px;margin:20px 0;padding:15px;border-left:4px solid #8c6e42;background:#fff9e8;">{st.session_state.choice_feedback}</p>""", unsafe_allow_html=True)
        if st.button("📜 确认抉择，进入下一章"):
            st.session_state.confirm_next = False
            st.session_state.choice_feedback = ""
            next_chapter()
def next_chapter():
    if st.session_state.chapter < 5:
        st.session_state.chapter += 1
        st.rerun()
    else:
        st.session_state.page = "end"
        st.rerun()
def get_image_base64(path):
    with open(path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return f"data:image/jpeg;base64,{encoded}"
# 获取当前脚本所在文件夹的路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 传入新的路径
teacher_img = get_image_base64(os.path.join(current_dir, "teacher.jpg"))
student_img = get_image_base64(os.path.join(current_dir, "student.jpg"))


# 张居正生平传记页面
def page_bio():
    custom_title("📜 张居正生平与他的选择")
    st.subheader("【人物简介】")
    st.markdown(ZHANG_JUZENG_BIO, unsafe_allow_html=True)
    st.subheader("【张居正的选择】")
    st.markdown(JUZENG_SIX_CHOICES, unsafe_allow_html=True)
    st.markdown(f"""
    <div style="display:flex; align-items:flex-start; margin-top:30px; margin-bottom:30px;">
        <img src="{teacher_img}" style="width:80px; height:80px; flex-shrink:0; border-radius:50%; object-fit:cover;">
        <div style="margin-left:20px; background:#fff6e8; padding:15px 22px; border-radius:12px; border:1px solid #e9dfcd; font-size:17px; color:#5c1010;">
            少年，愿你能懂我这一生的坚守与无奈……
        </div>
    </div>
    <div style="display:flex; align-items:flex-start; margin-bottom:30px; justify-content:flex-end;">
        <div style="margin-right:20px; background:#f0ebe1; padding:15px 22px; border-radius:12px; border:1px solid #d3c7b4; font-size:17px; color:#5c1010;">
            先生，我是从郦波老师的讲座《风雨张居正》中认识您的，那时我方认识四百多年前的一个孤独灵魂，我忍不住哭泣、忍不住泪流满面。为您“知我罪我，其惟春秋”的凛然，为您倾注一切心血给万历和新政却终究付诸东流而愤恨，为您孤身一人踽踽独行而心痛而心酸。先生，您万古松风，我辈谨记！
        </div>
        <img src="{student_img}" style="width:70px; height:70px; flex-shrink:0; border-radius:50%; object-fit:cover;">
    </div>""", unsafe_allow_html=True)
    st.markdown("<div style='margin-top:30px'></div>", unsafe_allow_html=True)
    if st.button("🔙 返回结局页面"):
        st.session_state.page = "end"
        st.rerun()
# 结局页
def page_end():
    custom_title("🏮 终章：张居正｜归途")
    st.markdown("",unsafe_allow_html=True)
    s = st.session_state.status
    ml, hq, cc, sw = s["谋略"], s["皇权"], s["赤诚"], s["声望"]
    t, desc, hidden_t, hidden_desc = get_ending(sw, hq, ml, cc)
    if st.session_state.hidden_ending:
        st.success(f"### {hidden_t}")
        bg = ENDING_SUCCESS
        end_box = f'<p style="{bg}padding:30px 40px;border-radius:12px;font-size:18px;line-height:2.2;text-indent:2em;text-align:justify;margin-top:15px;margin-bottom:15px;">{hidden_desc}</p>'
    else:
        if "完美" in t:
            st.success(f"### {t}")
            bg = ENDING_SUCCESS
        elif "悲剧" in t:
            st.error(f"### {t}")
            bg = ENDING_FAIL
        else:
            st.info(f"### {t}")
            bg = ENDING_NORMAL
        end_box = f'<p style="{bg}padding:30px 40px;border-radius:12px;font-size:18px;line-height:2.2;text-indent:2em;text-align:justify;margin-top:15px;margin-bottom:15px;">{desc}</p>'
    st.markdown(end_box,unsafe_allow_html=True)
    st.markdown("**📊 最终属性评定**")
    st.markdown(get_bar_html("🏛️ 朝野声望","#b89768",sw),unsafe_allow_html=True)
    st.markdown(get_bar_html("👑 皇权好感","#a82020",hq),unsafe_allow_html=True)
    st.markdown(get_bar_html("🧠 治世谋略","#3c5480",ml),unsafe_allow_html=True)
    st.markdown(get_bar_html("❤️ 家国赤诚","#c72c41",cc),unsafe_allow_html=True)

    # 【优化方案】用容器包裹按钮，应用紧凑样式
    # 最终属性评定后...
    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)
    
    # 将按钮放入一个垂直的容器中，取消多余的 HTML 标记
    # 使用简单的空列来避免间距过大
    if st.button("📜 查看张居正生平与他的选择"):
        st.session_state.page = "bio"
        st.rerun()

    # 如果需要触发隐藏结局
    if t == "💀 身死政废｜千古悲风（悲剧结局）" and not st.session_state.hidden_ending:
        if st.button("🐢 触发白龟护佑（隐藏结局）"):
            st.session_state.hidden_ending = True
            st.rerun()

    # 重开按钮
    if st.button("🔁 重活一世，改写张居正命运"):
        st.session_state.clear()
        st.rerun()

# 主入口
def main():
    st.set_page_config(page_title=PAGE_TITLE, page_icon="🐢", layout=PAGE_LAYOUT)
    st.markdown(CSS_STYLE,unsafe_allow_html=True)
    init_data()
    show_side()
    if st.session_state.page == "start": page_start()
    elif st.session_state.page == "play": page_play()
    elif st.session_state.page == "end": page_end()
    elif st.session_state.page == "bio": page_bio()
if __name__ == "__main__":
    main()