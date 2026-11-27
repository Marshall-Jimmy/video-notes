# AGENTS.md · 交接说明

> 给下一个接手这个仓库的 AI 助手（或未来的我自己）。读完这一页就能继续加第 06 期，不需要重新摸索。
> 最后更新：2026-11-28

## 一句话上手

新视频链接来了 → `vidsum.py prepare` → AudioTranscribe 转写 → ViewImage 看帧 → 写 `summary.md` → `vidsum.py render` → 更新 README 清单 → `python tools/gh_push.py`。

## 这是什么

一个**视频笔记仓库**。把抖音等平台的视频链接，抓成「结构化摘要 + 带时间点口播稿 + 关键帧」，以每期一个目录的形式持续积累。内容主题是**游戏开发技术**和**AI 辅助美术/立项**。

仓库根目录就是产出根目录（`vidsum_out` 本身），所以新一期直接落在 `./<标题>_<作品ID>/`。

## 当前状态

已整理 5 期（清单见 `README.md`）。每期目录里有：

```
<标题>_<作品ID>/
├── report.html       单文件网页（图片 base64 内联）← 主要交付物
├── summary.md        摘要（结构见下方"写作规范"）
├── transcript.md     带时间点的完整口播稿
├── contact_sheet.jpg 关键帧拼图
├── frames/k01_00m01s.jpg …   关键帧，文件名带时间点
├── manifest.json     元信息索引（作者/时长/每帧时间点/音频路径）
├── meta.json         原始元信息
├── source.mp4        原视频 —— 已 gitignore
└── audio/audio.mp3   16k 单声道音轨 —— 已 gitignore
```

## 新增一期的完整流程

工具是一个本地 skill：`~/.workbuddy/skills/video-summarize/`（脚本在 `scripts/`，说明在 `SKILL.md`）。

### 0. 环境自检（换机器时先跑）

```bash
python ~/.workbuddy/skills/video-summarize/scripts/vidsum.py doctor
```

五项全 `OK` 再继续。缺什么它会把补救命令打印出来。

### 1. 抓取 + 抽帧 + 抽音轨

```bash
python ~/.workbuddy/skills/video-summarize/scripts/vidsum.py prepare "<链接>" --out . --max-frames 10
```

- 抖音口令里那堆 `k@C.Hv`、时间戳全部丢掉，**只留 URL**
- `--max-frames`：口播/幻灯片型给 **10~12**，纯演示/操作录像给 **8**
- 跑完会打印目录名和 manifest 路径，**先读 manifest** 再往下走
- ⚠️ 抖音必须**有头浏览器**，脚本会自己起一个移到屏幕外的 Edge 窗口，别加 `--headless`

### 2. 语音转写

把 `<目录>/audio/audio.mp3` 交给 **AudioTranscribe** 工具。它返回**带时间戳的分段文本**：

```
[0:0.000,0:33.500,0]  正文…
```

整理成 `transcript.md`：按语义合并成 10 段左右的自然段，每段前面标 `**mm:ss – mm:ss**`。同音错字要改（例如 Godda→Godot、twin→Tween、isopret→Aseprite、Grace→GRIS、hyper 3D→Hyper3D），**但不要改写原意**。

### 3. 看图

关键帧必须**真的看**，用 `ViewImage` 逐张过，一次并行 2~4 张。重点读：

- 画面大标题（往往就是这一节的结论）
- 图上标注的公式 / 数值 / 分类标签
- 底部字幕
- 很多教学视频每帧底部有章节进度条，照着它分节最准

**图注写错比不写更糟**，宁可少放一张图，也不要凭标题猜内容。

### 4. 写 summary.md

```markdown
# <标题> —— <一句话副标题>

> 作者 **X** ｜ 时长 **03:17** ｜ 平台 ｜ 点赞 · 收藏 · 评论
> 原视频：<URL>

## 一句话概括
## 30 秒版要点        （每条一句话，覆盖方法论的每一层）
## 分步拆解
### 1. <小节名>（00:37）
![<图注：这张图在讲什么>](frames/k02_00m37s.jpg)
## 可抄参数表          （技术类必须有；方法论类可换成对照表）
## 关键帧总览
![关键帧总览](contact_sheet.jpg)
## 可以直接带走的三条经验
---
完整口播文字稿（带时间点）见 `transcript.md`。
```

硬要求：

- **数字必须准确**：`×10`、`×3`、`0.76`、`70%`、`5 厘米间距`、`344 件` 这类，原样落到正文和表格里，这是这类视频最值钱的部分
- **每张图配时间点**，用户要能回看原片
- 图片一律用**相对路径**（`frames/xxx.jpg`），否则第 5 步内联不进去
- 摘要长度控制在原文的 1/5 左右，不要逐句复述

### 5. 渲染 + 交付

```bash
python ~/.workbuddy/skills/video-summarize/scripts/vidsum.py render "<目录>"
```

生成 `report.html`（图片 base64 内联，单文件可分享）。然后：

1. 更新 `README.md` 的清单表格（按"技术实现 / 方法论与 AI 协作"归类，并补上 report.html 的链接）
2. 提交（commit 规范见下）

### 6. 重抽关键帧（不重新下载）

```bash
python ~/.workbuddy/skills/video-summarize/scripts/vidsum.py frames "<目录>" --max-frames 12
```

会重写 `frames/` 和 `contact_sheet.jpg` 并更新 manifest。**改完要重跑 render。**

## 踩过的坑（别重复踩）

| 坑 | 结论 |
|---|---|
| 抖音网页明文地址 | 早就没有了。`_ROUTER_DATA` 只剩 query；curl 首页只发 `__ac_nonce`。**必须**用有头浏览器拦 `aweme/detail` 接口 |
| yt-dlp 抓抖音 | 直接报 `Fresh cookies ... are needed`，导出浏览器 Cookie 喂它也没用。抖音一律走浏览器，别浪费时间 |
| headless 浏览器 | 抖音会甩到"验证码中间页"。**永远用有头**（脚本已把窗口移到屏幕外） |
| 抽帧时间戳 | 不能用 `fps` 滤镜——它会**把输出时间戳重排成从 0 开始**，片头有淡入时导出的"第 0 帧"是纯黑。必须 `select='not(mod(n,step))'` + `-vsync 0` 保留原始 PTS |
| 关键帧数量 | 口播/PPT 型给 8 帧会漏掉关键图表（07:34 那条丢了金字塔页，改 12 帧才补回） |
| 装依赖 | 这台机器 pypi 直连超时、清华镜像 403。用**阿里云镜像** `-i https://mirrors.aliyun.com/pypi/simple`；ffmpeg 从 **npmmirror** 拉（`@ffmpeg-installer/win32-x64`，22MB/4s） |
| 文件名 | 目录名里的 `？`、`《》` 是**全角/合法字符**，不要"修正"成半角，改了链接就断。但 `#` 和 `%` 必须去掉——`#` 在 URL 里是片段分隔符、`%` 是转义起始，带它们的目录点不开（脚本的 `slugify` 已经会剥掉） |

## 环境依赖

- Python 3.13 · Pillow
- `yt-dlp`（B站/YouTube/小红书等非抖音站点）
- Playwright 1.65，用 `channel="msedge"`（机器上只有 Edge，没有 Chrome）
- ffmpeg / ffprobe 在 `~/.workbuddy/binaries/ffmpeg/`（脚本会依次找 `VIDSUM_FFMPEG` → 该目录 → PATH → 剪映自带 → imageio-ffmpeg）

## 提交约定

- `.gitignore` 排除 `source.mp4`、`audio/`、`.cand/`、`*.part`。**这个仓库要保持 20MB 量级**，别把原视频提交进去
- commit message 用 `feat: 新增《标题》摘要` / `fix: 修正 xx 图注` / `docs: 更新 README 清单`
- 一期的素材和文档**一次提交**，方便回溯

## 推送到 GitHub（重要）

仓库：<https://github.com/Marshall-Jimmy/video-notes>（private）

**本机 `git push` 用不了**：HTTP 代理只放通了 `api.github.com`，`github.com:443` 连不上，
git 会报 `Failed to connect to github.com:443 over proxy`。gh 的 API 是通的，所以推送走 API：

```bash
git add -A && git commit -m "feat: 新增《xxx》摘要"
python tools/gh_push.py            # 本地 HEAD 的 tree -> 远端 main
python tools/gh_push.py --dry-run  # 只看差异不动手
```

`tools/gh_push.py` 的做法：把本地 HEAD 的每个文件按 git 对象库里的内容（LF 归一化后）
做成 blob → 建 tree → 以**远端当前 main 为父**建 commit → 移动分支指针。
远端 tree 与本地一致时会直接跳过，不会产生空提交。

⚠️ 由此带来的**历史分歧**：远端有两个提交（`chore: 初始化仓库` 引导提交 + 内容提交），
本地只有一个。内容（tree）完全一致，但祖先不同。所以**在能正常访问 github.com 的机器上
第一次操作前**，先跑一次：

```bash
git fetch origin && git reset --hard origin/main
```

之后 `git pull / git push` 就是正常的了。

## 待办 / 想法

- [x] GitHub Pages 已启用，`index.html` 发成了在线页面：<https://marshall-jimmy.github.io/video-notes/>
      （仓库已设为 public；Pages 源 = `main` 分支根目录，每次推送后自动重建，约 40 秒）
- [ ] 抖音图文作品（`kind=images`）还没实际跑过，脚本里有分支，遇到时验证一下
- [ ] 可以考虑给每期加"标签"（Godot / Shader / AI 美术 / 立项），README 里按标签检索

## Pages 的注意点

- **目录名不能含 `#` 和 `%`**：`#` 在 URL 里是片段分隔符，带它的目录在网页上点不开
  （03 期原来叫 `今天继续驯服AI_#Godot_...`，已经改名；skill 的 `slugify` 现在会自动剥掉这两个字符）
- 全角 `？`、`《》`、`：` 是安全的，会被自动 URL 编码
- Pages 不渲染 `.md`，所以对外看排版走 `report.html` / `index.html`
