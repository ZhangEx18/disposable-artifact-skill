# Disposable Artifact

一个适用于 Codex、Claude Code 和其他 Agent Skills 运行时的技能：把长文本、研究结果、教程、时间线和数据比较整理成单文件、可交互、可追溯的 HTML 产物。

它的默认行为是先在聊天中回答。只有当用户明确要网页，或搜索、筛选、时间线、关系图和交互模拟能明显降低理解成本时，才生成 HTML。用户明确要求 Markdown、逐字引文或归档文本时，遵守该格式。

## 设计目标

- 单文件、自包含、离线可打开。
- 事实、来源、证据状态、统计期和未验证项可追溯。
- 页面版式由内容形态决定，不套用固定 dashboard 模板。
- 搜索、筛选、详情、时间线和模拟等控件都对应真实数据操作。
- 默认本地交付，不自动发布、上传或部署。

## 安装

把 `skill/` 目录复制到个人或项目技能目录：

```bash
cp -R skill ~/.agents/skills/disposable-artifact
```

在 Codex 中重载技能或开始新会话后，使用：

```text
把这份多来源分析做成可搜索、可展开的单文件 HTML，来源和未验证项要保留。
```

## 开发与验证

本项目按 RED → GREEN → REFACTOR 维护：

1. 先用 [`evals/red-baseline.md`](skill/evals/red-baseline.md) 的压力场景记录没有技能时容易出现的行为。
2. 修改 `skill/SKILL.md`，只补上已观察到的漏洞。
3. 用 [`evals/evals.json`](skill/evals/evals.json) 的场景复测，检查格式选择、证据边界、无依据图表和发布边界。
4. 生成真实 HTML 后做静态检查、浏览器检查、键盘检查和手机宽度检查。

快速校验：

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skill
```

本仓库还提供两个不依赖第三方包的检查器：

```bash
python3 scripts/verify.py
python3 scripts/check_html.py path/to/artifact.html
python3 -m unittest discover -s tests -v
```

`verify.py` 只检查 skill 结构、eval 和本地链接；`check_html.py` 只检查单文件、嵌入资源、文档元数据和证据片段链接。两者都不会代替真实浏览器、内容核验或可视化审查。

## 取舍

本技能借鉴了 `display-dev/visualize` 的反模板审查、`claude-chart-dashboard` 的内容驱动版式和 `dataloupe` 的单文件离线交互原则。它不把这些项目作为运行时依赖，也不要求 CDN、npm、外部 API 或后端服务。
