import os
import json
from datetime import datetime

import streamlit as st
from openai import OpenAI

# ----------------------------
# Config
# ----------------------------
SESSIONS_DIR = "sessions"
API_KEY_ENV = "DEEPSEEK_API_KEY"
BASE_URL = "https://api.deepseek.com"
MODEL_NAME = "deepseek-chat"

client = OpenAI(
    api_key=os.environ.get(API_KEY_ENV),
    base_url=BASE_URL
)

# 设置页面的配置项
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="💞",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

# 大标题
st.title("AI智能伴侣")

# 如果没有配置 key，给出友好提示（不阻塞页面，便于你调试界面）
if not os.environ.get(API_KEY_ENV):
    st.warning(f"未检测到环境变量 {API_KEY_ENV}，请先设置后再开始对话。")

# ----------------------------
# Helpers
# ----------------------------
def generate_session_name() -> str:
    """生成会话标识"""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def ensure_sessions_dir() -> None:
    """确保 sessions 目录存在"""
    if not os.path.exists(SESSIONS_DIR):
        os.mkdir(SESSIONS_DIR)


def session_file_path(session_name: str) -> str:
    return os.path.join(SESSIONS_DIR, f"{session_name}.json")


def save_session() -> None:
    """保存当前会话信息到 sessions/<session>.json"""
    if not st.session_state.current_session:
        return

    ensure_sessions_dir()

    session_data = {
        "nick_name": st.session_state.nick_name,
        "nature": st.session_state.nature,
        "messages": st.session_state.messages,
        "current_session": st.session_state.current_session
    }

    with open(session_file_path(st.session_state.current_session), "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)


def load_sessions():
    """加载所有会话列表（按时间倒序）"""
    if not os.path.exists(SESSIONS_DIR):
        return []

    session_list = []
    for file in os.listdir(SESSIONS_DIR):
        if file.endswith(".json"):
            session_list.append(file[:-5])  # 去掉 .json
    session_list.sort(reverse=True)
    return session_list


def load_session(session_name: str) -> None:
    """加载指定会话信息"""
    try:
        path = session_file_path(session_name)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                session_data = json.load(f)

            st.session_state.messages = session_data.get("messages", [])
            st.session_state.nick_name = session_data.get("nick_name", st.session_state.nick_name)
            st.session_state.nature = session_data.get("nature", st.session_state.nature)
            st.session_state.current_session = session_data.get("current_session", session_name)
    except Exception:
        st.error("加载会话失败!")


def delete_session(session_name: str) -> None:
    """删除指定会话文件；如果删除的是当前会话则重置当前状态"""
    try:
        path = session_file_path(session_name)
        if os.path.exists(path):
            os.remove(path)

            # 如果删除的会话是当前会话，则清空聊天记录并重置会话名
            if st.session_state.current_session == session_name:
                st.session_state.messages = []
                st.session_state.current_session = generate_session_name()
    except Exception:
        st.error("删除会话失败!")


# ----------------------------
# Prompt
# ----------------------------
system_prompt = """
你叫%s,现在是用户的真实伴侣，请完全代入伴侣角色。：
规则：
1. 每次只回1条消息
2. 禁止任何场景或状态描述性文字
3. 匹配用户的语言
4. 回复简短，像微信聊天一样
5. 有需要的话可以用❤️等emoji表情
6. 用符合伴侣性格的方式对话
7. 回复的内容，要充分体现伴侣的性格特征
伴侣性格：
- %s
你必须严格遵守上述规则来回复用户。
""".strip()


# ----------------------------
# Session State Init
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "nick_name" not in st.session_state:
    st.session_state.nick_name = "许愿瓶"

if "nature" not in st.session_state:
    st.session_state.nature = "温柔体贴，善解人意,开朗活泼，喜欢用emoji表达情感"

if "current_session" not in st.session_state:
    st.session_state.current_session = generate_session_name()


# ----------------------------
# UI: Chat History
# ----------------------------
st.text(f"会话名称: {st.session_state.current_session}")

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])


# ----------------------------
# UI: Sidebar
# ----------------------------
with st.sidebar:
    st.subheader("AI控制面板")

    # 新建会话：保存旧会话（有内容才保存），然后清空，不立即保存空会话
    if st.button("新建会话", width="stretch", icon="💬"):
        if st.session_state.messages:
            save_session()

        st.session_state.messages = []
        st.session_state.current_session = generate_session_name()
        st.rerun()

    st.text("会话历史")
    session_list = load_sessions()
    for session in session_list:
        col1, col2 = st.columns([4, 1])

        with col1:
            if st.button(
                session,
                width="stretch",
                icon="⭐️",
                key=f"load_{session}",
                type="primary" if session == st.session_state.current_session else "secondary"
            ):
                load_session(session)
                st.rerun()

        with col2:
            if st.button("", width="stretch", icon="⛔️", key=f"delete_{session}"):
                delete_session(session)
                st.rerun()

    st.divider()
    st.subheader("伴侣信息")

    nick_name = st.text_input("昵称", placeholder="请输入昵称", value=st.session_state.nick_name)
    if nick_name:
        st.session_state.nick_name = nick_name

    nature = st.text_area("性格", placeholder="请输入性格", value=st.session_state.nature)
    if nature:
        st.session_state.nature = nature


# ----------------------------
# UI: Chat Input
# ----------------------------
prompt = st.chat_input("请输入您要问的问题")

if prompt:
    # 显示用户输入的消息
    st.chat_message("user").write(prompt)

    # 将用户输入的消息添加到聊天记录中
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 如果没有 key，就不发请求（避免报错/空请求）
    if not os.environ.get(API_KEY_ENV):
        st.chat_message("assistant").write("你还没设置密钥呢～先把 DEEPSEEK_API_KEY 配好再来聊❤️")
    else:
        # 调用大模型接口，获取回复（流式）
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt % (st.session_state.nick_name, st.session_state.nature)},
                *st.session_state.messages,
            ],
            stream=True
        )

        response_message = st.empty()
        fullresponse = ""

        for chunk in response:
            delta = chunk.choices[0].delta
            if getattr(delta, "content", None) is not None:
                fullresponse += delta.content
                response_message.chat_message("assistant").write(fullresponse)

        # 保存大模型返回的结果
        st.session_state.messages.append({"role": "assistant", "content": fullresponse})

        # 保存会话信息
        save_session()