# Streamlit AI Companion

一个基于 Streamlit 的 AI 智能伴侣聊天应用（DeepSeek API，使用 OpenAI SDK 兼容接口）。
支持自定义“昵称 / 性格”，并把每次会话保存为本地 JSON（sessions 目录）。

## 功能

- Streamlit 聊天界面
- 自定义伴侣昵称与性格（侧边栏）
- 会话历史：新建 / 加载 / 删除
- 流式输出回复

## 环境要求

- Python 3.10+

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置 API Key（Windows PowerShell）

本项目通过环境变量读取 DeepSeek API Key：

```powershell
$env:DEEPSEEK_API_KEY="你的key"
```

## 启动

```bash
streamlit run AI_companion.py
```

## 数据说明

- `sessions/`：运行时自动生成的会话记录（包含聊天内容），默认已在 .gitignore 中忽略，不会上传到 GitHub。
