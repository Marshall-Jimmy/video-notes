# 视频笔记 · 游戏开发 & AI 美术

把抖音（以及 B 站、YouTube、小红书等）的视频链接，抓成**结构化摘要 + 带时间点的完整文字稿 + 关键帧截图**，产物统一放在这个仓库里持续更新。

内容以**游戏开发技术**和**AI 辅助美术/立项**为主，都是我自己觉得值得回看的视频。

**在线阅读：[marshall-jimmy.github.io/video-notes](https://marshall-jimmy.github.io/video-notes/)** ← 带图排版的报告页都在这

---

## 怎么读

每期一个目录 `<标题>_<作品ID>/`，里面固定这几个文件：

| 文件 | 用途 |
|---|---|
| `report.html` | **优先看这个**。单文件网页，图片已内联，双击/下载就能看，排版好读 |
| `summary.md` | 纯文本摘要。分「一句话概括 / 30 秒要点 / 分步拆解 / 参数表 / 三条经验」 |
| `transcript.md` | 带时间点的完整口播稿，想核对原话时看 |
| `contact_sheet.jpg` | 关键帧拼图，一眼看完全片 |
| `frames/` | 关键帧原图，文件名带时间点（如 `k04_01m21s.jpg`） |
| `manifest.json` | 元信息索引：作者、时长、点赞收藏、每帧时间点、音频路径 |

> `source.mp4`（原视频）和 `audio/`（音轨）**不入库**——它们占了 145MB，随时能用下面一条命令重新抓。

## 已整理的视频

### 技术实现

| # | 视频 | 作者 | 时长 | 一句话 |
|---|---|---|---|---|
| 01 | [让火焰烧起来 ·《五星地牢》开发日志 04](让火焰烧起来_《五星地牢》开发日志04_分享我正在制作的游戏《五_7689158160245973672/summary.md) | babyunko | 03:17 | 不靠贴图动画：每像素一个数值，两层滚动噪声把轮廓推到 0 附近，正数显示负数透明 |
| 02 | [2D 游戏中的雪天效果 DEV LOG 05](2D游戏中的雪天效果_DEV_LOG.05_本期主要是讨论一下在_7683890555486506255/summary.md) | Mushreb | 04:00 | 粒子归粒子、积雪归 shader：噪波 + Step 阈值当蒙版，阈值就是积雪厚度 |
| 03 | [今天继续驯服 AI（PageKit）](今天继续驯服AI_Godot_游戏开发_五星地牢_uik_7703573494676899008/summary.md) | babyunko | 03:18 | Godot 太自由 → AI 每个页面写一套动画；用 UIKit 式转场协议把动画收进一个类 |

### 方法论与 AI 协作

| # | 视频 | 作者 | 时长 | 一句话 |
|---|---|---|---|---|
| 04 | [AI 游戏美术立项：先有画风还是先有玩法？](AI游戏美术立项：先有画风还是先有玩法？_做游戏美术到底先画什么_7692132863755537718/summary.md) | 野路子游戏车间 | 07:34 | 三个入口（题材/画风/形象）没有高下，金字塔是看别人作品的放大镜 |
| 05 | [AI 做的场景为什么一眼假？](AI_做的场景为什么一眼假？_上期讲了_AI_怎么从零搭出一个游_7710984439119340518/summary.md) | 糯米鱼丸（Ai版） | 06:36 | 「假」是四个问题：东西太少、太新、摆得太整齐、光没来源 |
| 06 | [AI 游戏美术：风格 ≠ 画风](AI游戏美术-风格≠画风：游戏的美术风格怎么确定？_美术风格不等_7695768004130344202/summary.md) | 野路子游戏车间 | 04:48 | 美术风格 = 题材元素 × 感受调性 × 表现技法，「画风」只住在第三层 |
| 07 | [4 招抢救 AI 半成品](4招教你抢救AI半成品！零基础可照抄！_AI_给的半成品总差点意_7709727096804887846/summary.md) | tp 制造好游戏 | 03:51 | 先定位哪块不满意 → 让 AI 反问 → 说清喜恶并沉淀 taste 文档 → 多 AI 交叉验收 |

报告页（**在线看**，图片已内联，手机也能开）：

**<https://marshall-jimmy.github.io/video-notes/>**

- [01 · 火焰特效](https://marshall-jimmy.github.io/video-notes/让火焰烧起来_《五星地牢》开发日志04_分享我正在制作的游戏《五_7689158160245973672/report.html)
- [02 · 雪天效果](https://marshall-jimmy.github.io/video-notes/2D游戏中的雪天效果_DEV_LOG.05_本期主要是讨论一下在_7683890555486506255/report.html)
- [03 · PageKit](https://marshall-jimmy.github.io/video-notes/今天继续驯服AI_Godot_游戏开发_五星地牢_uik_7703573494676899008/report.html)
- [04 · 美术立项](https://marshall-jimmy.github.io/video-notes/AI游戏美术立项：先有画风还是先有玩法？_做游戏美术到底先画什么_7692132863755537718/report.html)
- [05 · AI 场景优化](https://marshall-jimmy.github.io/video-notes/AI_做的场景为什么一眼假？_上期讲了_AI_怎么从零搭出一个游_7710984439119340518/report.html)
- [06 · 风格 ≠ 画风](https://marshall-jimmy.github.io/video-notes/AI游戏美术-风格≠画风：游戏的美术风格怎么确定？_美术风格不等_7695768004130344202/report.html)
- [07 · 4 招抢救半成品](https://marshall-jimmy.github.io/video-notes/4招教你抢救AI半成品！零基础可照抄！_AI_给的半成品总差点意_7709727096804887846/report.html)

> GitHub 的仓库文件页不会渲染 HTML，所以报告走 GitHub Pages 发布；`summary.md` 在仓库里点开就是排好版的。

## 新增一期怎么做

整套流程封装成了一个 skill：`~/.workbuddy/skills/video-summarize/`。

```bash
# 1. 抓视频 + 抽关键帧 + 抽音轨（在本仓库根目录执行）
python ~/.workbuddy/skills/video-summarize/scripts/vidsum.py prepare "<视频链接>" --out . --max-frames 10

# 2. 语音转写：把 <目录>/audio/audio.mp3 交给 AudioTranscribe 工具
# 3. 用 ViewImage 逐张看 <目录>/frames/*.jpg，照着写 <目录>/summary.md
# 4. 渲染单文件网页
python ~/.workbuddy/skills/video-summarize/scripts/vidsum.py render "<目录>"
```

给下一个 AI 助手看的完整交接说明在 **[AGENTS.md](AGENTS.md)**，里面记了目录约定、写作规范，以及踩过的坑（抖音必须开有头浏览器、抽帧不能用 `fps` 滤镜等）。

## 关于本仓库

- 摘要与关键帧由 AI 生成后人工校对，**图注和数字都对着原片核过**；口播稿是语音识别，同音错字已按上下文修正
- 视频版权归原作者所有，这里只保留**摘要、关键帧和引用**，用于个人学习
- 仓库`.gitignore` 排除了 `source.mp4`、`audio/`，所以 clone 下来只有约 20MB
