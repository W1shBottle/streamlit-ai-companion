![CI](https://github.com/W1shBottle/streamlit-ai-companion/actions/workflows/ci.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

# Streamlit AI Companion

一个基于 Streamlit 的 AI 智能伴侣聊天应用（DeepSeek API，使用 OpenAI SDK 兼容接口）。
支持自定义“昵称 / 性格”，并把每次会话保存为本地 JSON（`sessions/` 目录）。

---

## 功能

- Streamlit 聊天界面（`st.chat_input` / `st.chat_message`）
- 自定义伴侣昵称与性格（侧边栏）
- 会话历史：新建 / 加载 / 删除
- 流式输出回复
- 本地会话持久化保存（JSON）

---

## 目录结构

```text
streamlit-ai-companion/
  AI_companion.py
  requirements.txt
  README.md
  .gitignore
  sessions/              # 运行后自动生成（本地会话记录，默认已忽略不上传）
  .venv/                 # 本地虚拟环境（默认已忽略不上传）
  .idea/                 # PyCharm 配置（默认已忽略不上传）
```

---

## 环境要求

- Python 3.10+

---

## 本地运行（Windows / PowerShell）

### 1) 创建虚拟环境并安装依赖

在项目根目录执行：

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -U pip
py -m pip install -r requirements.txt
```

> 如果激活时报 ExecutionPolicy 限制，可临时放开（仅对当前终端生效）：
>
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> .\.venv\Scripts\Activate.ps1
> ```

### 2) 配置 API Key（DeepSeek）

本项目通过环境变量读取 DeepSeek API Key：

```powershell
$env:DEEPSEEK_API_KEY="你的key"
```

> 注意：不要把真实 Key 写进代码或提交到 GitHub。

### 3) 启动 Streamlit

```powershell
streamlit run AI_companion.py
```

---

## 本地运行（macOS / Linux）

### 1) 创建虚拟环境并安装依赖

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
```

### 2) 配置 API Key（DeepSeek）

```bash
export DEEPSEEK_API_KEY="你的key"
```

### 3) 启动 Streamlit

```bash
streamlit run AI_companion.py
```

---

## 常见问题（FAQ）

### Q1：PyCharm 报 “没有名为 streamlit/openai 的模块”

原因：PyCharm 选择的解释器里没装依赖。  
解决：确保项目使用 `.venv` 解释器，并在该环境内执行：

```powershell
py -m pip install -r requirements.txt
```

### Q2：`python` 命令不可用，但 `py` 可以

Windows 上这是正常情况：安装了 Python Launcher（`py`），但没有把 `python` 加到 PATH。
你可以一直用 `py`。

### Q3：为什么仓库里没有 `sessions/`？

`sessions/` 是运行后自动生成的本地会话记录目录，包含聊天内容，默认在 `.gitignore` 里忽略，避免隐私数据上传。

---

## 配置说明（代码内关键参数）

- `API_KEY_ENV = "DEEPSEEK_API_KEY"`：读取 API Key 的环境变量名
- `BASE_URL = "https://api.deepseek.com"`：DeepSeek OpenAI 兼容接口地址
- `MODEL_NAME = "deepseek-chat"`：模型名
- `SESSIONS_DIR = "sessions"`：会话保存目录

---

## License

本项目采用 **MIT License** 开源协议，详见仓库根目录的 `LICENSE` 文件。
