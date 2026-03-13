# Subtitle Extractor & Translator (MVP)

一个可运行的 Python MVP，用于**音视频字幕提取（ASR）+ 翻译 + SRT 导出**。

## 功能
- 上传音视频文件（`mp4/mp3/wav/mkv/m4a`）
- ffmpeg 抽取单声道 16k wav
- 语音识别生成 `original.srt`
- 翻译生成 `translated.srt`
- 双语合并生成 `bilingual.srt`
- 查询任务状态、下载字幕

## 技术栈
- FastAPI
- Uvicorn
- ffmpeg（系统依赖）
- faster-whisper（可选）
- deep-translator（可选，默认有离线回退）

## 快速开始
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

打开：`http://127.0.0.1:8000/docs`

## API
### 1) 创建任务
`POST /jobs`

Form Data:
- `file`: 音视频文件
- `target_lang`: 目标语言代码，默认 `zh-CN`
- `source_lang`: 源语言代码，默认 `auto`

返回：
```json
{
  "id": "uuid",
  "status": "queued"
}
```

### 2) 查询任务
`GET /jobs/{job_id}`

### 3) 下载字幕
`GET /jobs/{job_id}/artifacts/{name}`

`name` 可选：`original.srt`, `translated.srt`, `bilingual.srt`

## 环境变量
- `ASR_MODEL_SIZE`：`tiny/base/small/medium/large-v3`（默认 `base`）
- `USE_WHISPER`：`1` 时优先使用 faster-whisper，默认 `0`

## 目录结构
```text
app/
  main.py
  models.py
  pipeline.py
  srt.py
  storage.py
  translation.py
  asr.py
  media.py
  worker.py
data/
  jobs/
```

## 说明
- 未安装 `faster-whisper` 或 `ffmpeg` 时，会在任务日志中给出错误信息。
- 翻译层做了可插拔：如果 online translator 不可用，会回退到本地占位翻译，确保流程可跑通。


## 真机测试建议
- 如果环境没有 ffmpeg，可直接上传 **16k 单声道 wav**，系统会跳过 ffmpeg 转码。
- 在本仓库可执行：`PYTHONPATH=. pytest -q tests/test_pipeline_e2e.py` 验证端到端产出。


## Web 界面
- 启动后访问 `http://127.0.0.1:8000/`，可通过页面上传文件、查看状态并下载字幕。
- API 文档仍可用：`http://127.0.0.1:8000/docs`。


## 打包成 EXE（Windows）
1. 在 Windows 上打开终端，进入项目根目录。
2. 执行：`scripts\build_exe.bat`
3. 产物位于：`dist\subtitle-tool.exe`
4. 双击或命令行启动后，默认访问：`http://127.0.0.1:8000/`

你也可以手动执行（Windows）：
```bash
py -3 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt pyinstaller==6.10.0
pyinstaller --onefile --name subtitle-tool --add-data "app\static;app\static" scripts\run_app.py
```

> 说明：打包后界面静态文件会一起被带入 EXE，代码里已兼容 PyInstaller 的 `_MEIPASS` 资源路径。
