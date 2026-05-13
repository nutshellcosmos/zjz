# -*- coding: utf-8 -*-
# 主程序｜纯净浅色版 无多余居中代码
import streamlit as st
from game_text import *
from game_style import *

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
    side.divider()
    side.error(SIDEBAR_WARN)
    if side.button("🔄 重开一局"):
        st.session_state.clear()
        st.rerun()

# 开局页
def page_start():
    st.title("📜 万古松风")
    st.subheader("你将扮演：张居正｜大明铁血首辅")
    st.markdown("",unsafe_allow_html=True)
    st.markdown(STORY_BOX.format(START_INTRO),unsafe_allow_html=True)
    st.markdown("<div style='margin-top: 40px'></div>", unsafe_allow_html=True)
    if st.button("✅ 入局大明，化身张居正"):
        st.session_state.page = "play"
        st.rerun()

# 游玩页
def page_play():
    cid = st.session_state.chapter
    data = CHAPTER_LIST[cid]
    st.title(data["title"])
    st.markdown("",unsafe_allow_html=True)
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
                if st.session_state.status[key] > 100:
                    st.session_state.status[key] = 100
                if st.session_state.status[key] < 0:
                    st.session_state.status[key] = 0
            st.session_state.choice_feedback = feedback
            st.session_state.confirm_next = True
            st.rerun()

        if opt1: change_attr(effects[0], feedback_texts[cid][0])
        if opt2: change_attr(effects[1], feedback_texts[cid][1])
        if opt3: change_attr(effects[2], feedback_texts[cid][2])
    else:
        st.markdown(f"""
        <p style="color:#5C3A21;font-size:18px;margin:20px 0;padding:15px;border-left:4px solid #8c6e42;background:#fff9e8;">
        {st.session_state.choice_feedback}
        </p>
        """, unsafe_allow_html=True)
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

# ✅ 新增：张居正生平传记页面
def page_bio():
    st.title("📜 张居正的生平与他的选择")
    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)

    st.subheader("【人物简介】")
    st.markdown(ZHANG_JUZENG_BIO, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:30px'></div>", unsafe_allow_html=True)
    st.subheader("【张居正的选择】")
    st.markdown(JUZENG_SIX_CHOICES, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:50px'></div>", unsafe_allow_html=True)
    if st.button("🔙 返回结局页面"):
        st.session_state.page = "end"
        st.rerun()

# 结局页
def page_end():
    st.title("🏮 终章：一代首辅｜张居正归途")
    st.markdown("",unsafe_allow_html=True)
    s = st.session_state.status
    ml = s["谋略"]
    hq = s["皇权"]
    cc = s["赤诚"]
    sw = s["声望"]

    t, desc, hidden_t, hidden_desc = get_ending(sw, hq, ml, cc)

    if st.session_state.hidden_ending:
        st.success(f"### {hidden_t}")
        bg = ENDING_SUCCESS
        end_box = f"""
<p style="{bg}padding:30px 40px;border-radius:12px;font-size:18px;line-height:2.2;text-indent:2em;text-align:justify;margin-top:15px;margin-bottom:15px;">{hidden_desc}</p>
"""
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
        end_box = f"""
<p style="{bg}padding:30px 40px;border-radius:12px;font-size:18px;line-height:2.2;text-indent:2em;text-align:justify;margin-top:15px;margin-bottom:15px;">{desc}</p>
"""

    st.markdown(end_box,unsafe_allow_html=True)
    st.markdown("",unsafe_allow_html=True)
    st.markdown("**📊 最终属性评定**")
    st.markdown(get_bar_html("🏛️ 朝野声望","#b89768",sw),unsafe_allow_html=True)
    st.markdown(get_bar_html("👑 皇权好感","#a82020",hq),unsafe_allow_html=True)
    st.markdown(get_bar_html("🧠 治世谋略","#3c5480",ml),unsafe_allow_html=True)
    st.markdown(get_bar_html("❤️ 家国赤诚","#c72c41",cc),unsafe_allow_html=True)

    # ✅ 新增：每个结局都显示这个按钮
    st.markdown("<div style='margin-top:30px'></div>", unsafe_allow_html=True)
    if st.button("📜 查看张居正生平与他的选择"):
        st.session_state.page = "bio"
        st.rerun()

    # 悲剧隐藏按钮
    if t == "💀 身死政废｜千古悲风（悲剧结局）" and not st.session_state.hidden_ending:
        st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)
        if st.button("🐢 触发白龟护佑（隐藏结局）"):
            st.session_state.hidden_ending = True
            st.rerun()

    # 重玩
    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)
    if st.button("🔁 重活一世，改写张居正命运"):
        st.session_state.clear()
        st.rerun()

# 主入口
def main():
    st.set_page_config(page_title=PAGE_TITLE, page_icon="🐢", layout=PAGE_LAYOUT)
    st.markdown(CSS_STYLE,unsafe_allow_html=True)
    init_data()
    show_side()

    if st.session_state.page == "start":
        page_start()
    elif st.session_state.page == "play":
        page_play()
    elif st.session_state.page == "end":
        page_end()
    # ✅ 新增：跳转传记页
    elif st.session_state.page == "bio":
        page_bio()

if __name__ == "__main__":
    main()