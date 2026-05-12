import streamlit as st

# 页面配置
st.set_page_config(
    page_title="张居正 历史小游戏",
    layout="wide"
)

# 全局样式美化
st.markdown("""
<style>
.main {background-color: #f5f1e6;}
h1 {color: #8b2323; text-align: center;}
.stButton>button {
    background-color: #8b2323;
    color: white;
    font-size: 18px;
    padding: 10px 25px;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# 标题
st.title("📜 张居正 历史知识闯关小游戏")
st.divider()

# 题目列表
questions = [
    {
        "q": "张居正属于哪个朝代的名臣？",
        "options": ["唐朝", "宋朝", "明朝", "清朝"],
        "ans": "明朝"
    },
    {
        "q": "张居正推行的重要改革叫什么？",
        "options": ["王安石变法", "一条鞭法", "戊戌变法", "庆历新政"],
        "ans": "一条鞭法"
    },
    {
        "q": "张居正担任过什么核心官职？",
        "options": ["宰相", "内阁首辅", "大将军", "御史大夫"],
        "ans": "内阁首辅"
    },
    {
        "q": "张居正改革主要针对哪方面？",
        "options": ["军事改革", "赋税与土地改革", "科举改革", "服饰改革"],
        "ans": "赋税与土地改革"
    }
]

# 初始化分数和题号
if "score" not in st.session_state:
    st.session_state.score = 0
if "idx" not in st.session_state:
    st.session_state.idx = 0

# 当前题目
if st.session_state.idx < len(questions):
    q = questions[st.session_state.idx]
    st.subheader(f"第{st.session_state.idx+1}题：{q['q']}")
    choice = st.radio("请选择答案：", q["options"], key="radio_choice")

    if st.button("提交答案"):
        if choice == q["ans"]:
            st.success("✅ 回答正确！加1分")
            st.session_state.score += 1
            st.balloons()
        else:
            st.error(f"❌ 答错了，正确答案是：{q['ans']}")
        
        st.session_state.idx += 1
else:
    # 闯关结束
    st.header("🏆 闯关结束！")
    st.info(f"你的最终得分：{st.session_state.score} / {len(questions)}")
    if st.session_state.score == len(questions):
        st.success("满分！你很了解张居正👍")
    elif st.session_state.score >= 2:
        st.warning("还不错，再多了解一下明朝历史~")
    else:
        st.error("可以多读读张居正相关历史哦")

    # 重置游戏
    if st.button("重新开始游戏"):
        st.session_state.score = 0
        st.session_state.idx = 0