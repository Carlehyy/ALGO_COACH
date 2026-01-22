# Everything Claude Code - 项目架构与学习指南

> 本文档详细介绍了 **Everything Claude Code** 项目的完整架构、功能模块以及每个目录的学习指南。

---

## 目录

1. [项目概述](#项目概述)
2. [项目架构](#项目架构)
3. [功能模块图](#功能模块图)
4. [目录学习指南](#目录学习指南)
5. [核心概念](#核心概念)
6. [快速开始](#快速开始)

---

## 项目概述

**Everything Claude Code** 是一个 Anthropic 黑客松获奖作品的配置集合，提供了生产就绪的代理（agents）、技能（skills）、钩子（hooks）、命令（commands）、规则（rules）和 MCP 配置。这些配置经过 10+ 个月的密集日常使用和真实产品开发打磨而成。

### 项目目标

- 提供 Claude Code 的完整配置模板
- 建立可重用的开发模式和最佳实践
- 实现跨会话的上下文持久化
- 提供自动化的工作流程和代码质量保证

### 技术栈

- **Claude Code**: Anthropic 的官方 CLI 工具
- **MCP (Model Context Protocol)**: 用于外部服务集成
- **Shell 脚本**: 钩子自动化
- **Markdown**: 配置文件格式
- **JSON**: 配置文件格式

---

## 项目架构

```
everything-claude-code/
|
├── agents/           # 专业化的子代理系统
├── commands/         # 斜杠命令快捷执行
├── contexts/         # 动态上下文注入
├── examples/         # 示例配置和会话
├── hooks/            # 事件驱动的自动化
├── mcp-configs/      # MCP 服务器配置
├── plugins/          # 插件生态文档
├── rules/            # 强制性编码规范
├── skills/           # 工作流定义和领域知识
|
├── docs/             # 项目文档 (本文档所在位置)
├── .gitignore        # Git 忽略配置
├── CONTRIBUTING.md   # 贡献指南
└── README.md         # 项目说明
```

### 架构设计原则

1. **模块化**: 每个目录独立负责特定功能
2. **可组合性**: 不同组件可以灵活组合使用
3. **可扩展性**: 易于添加新的 agents、skills、commands 等
4. **上下文感知**: 根据不同场景动态调整行为

---

## 功能模块图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Everything Claude Code                             │
│                         完整配置生态系统                                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        ▼                             ▼                             ▼
┌───────────────┐           ┌───────────────┐           ┌───────────────┐
│    AGENTS     │           │   COMMANDS    │           │    SKILLS     │
│   代理系统     │           │   命令系统     │           │   技能系统     │
├───────────────┤           ├───────────────┤           ├───────────────┤
│ • planner     │           │ • /plan       │           │ • TDD 工作流  │
│ • architect   │           │ • /tdd        │           │ • 编码规范     │
│ • code-review │           │ • /code-review│           │ • 前端模式     │
│ • security    │           │ • /e2e        │           │ • 后端模式     │
│ • tdd-guide   │           │ • /build-fix  │           │ • 安全审查     │
│ • e2e-runner  │           │ • /refactor   │           │ • 持续学习     │
│ • refactor    │           │ • /learn      │           │ • 战略压缩     │
│ • doc-updater │           │ • /update-*   │           │               │
└───────────────┘           └───────────────┘           └───────────────┘
        │                             │                             │
        └─────────────────────────────┼─────────────────────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        ▼                             ▼                             ▼
┌───────────────┐           ┌───────────────┐           ┌───────────────┐
│    RULES      │           │    HOOKS      │           │    CONTEXTS   │
│   规则系统     │           │   钩子系统     │           │   上下文系统   │
├───────────────┤           ├───────────────┤           ├───────────────┤
│ • security    │           │ • PreToolUse  │           │ • dev.md      │
│ • coding-style│           │ • PostToolUse │           │ • review.md   │
│ • testing     │           │ • PreCompact  │           │ • research.md │
│ • git-workflow│           │ • SessionStart│           │               │
│ • performance │           │ • SessionEnd  │           │               │
│ • agents      │           │ • Stop        │           │               │
│ • patterns    │           │ • 记忆持久化   │           │               │
│ • hooks       │           │ • 战略压缩     │           │               │
└───────────────┘           └───────────────┘           └───────────────┘
                                      │
                                      ▼
                            ┌───────────────┐
                            │   MCP CONFIGS │
                            │  MCP 配置系统  │
                            ├───────────────┤
                            │ • GitHub      │
                            │ • Supabase    │
                            │ • Vercel      │
                            │ • Railway     │
                            │ • Firecrawl   │
                            │ • Memory      │
                            │ • ClickHouse  │
                            │ • Cloudflare  │
                            │ • Context7    │
                            └───────────────┘
```

### 核心交互流程

```
用户请求
    │
    ▼
┌─────────────────┐
│  上下文选择      │ ← contexts/ (dev/review/research)
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│  命令执行        │ ──→ │  代理委托        │
│  commands/      │     │  agents/        │
└────────┬────────┘     └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     ▼
         ┌───────────────────────┐
         │   技能应用              │
         │   skills/              │
         └───────────┬───────────┘
                     ▼
         ┌───────────────────────┐
         │   规则检查              │
         │   rules/               │
         └───────────┬───────────┘
                     ▼
         ┌───────────────────────┐
         │   钩子触发              │
         │   hooks/               │
         └───────────┬───────────┘
                     ▼
              ┌─────────────┐
              │   MCP 集成   │
              │   mcp-.../   │
              └─────────────┘
```

---

## 目录学习指南

### 1. agents/ - 专业代理系统

**作用**: 定义专业化的子代理，用于委托特定任务。

#### 文件清单

| 文件 | 功能 | 使用场景 |
|------|------|----------|
| `planner.md` | 功能实现规划专家 | 新功能开发、架构变更、复杂重构 |
| `architect.md` | 系统设计决策专家 | 架构设计、技术选型、系统设计 |
| `tdd-guide.md` | 测试驱动开发向导 | TDD 实践、测试编写 |
| `code-reviewer.md` | 代码质量审查专家 | 代码审查、质量检查 |
| `security-reviewer.md` | 安全漏洞分析专家 | 安全审计、漏洞扫描 |
| `build-error-resolver.md` | 构建错误解决专家 | 修复构建失败、编译错误 |
| `e2e-runner.md` | E2E 测试专家 | Playwright E2E 测试生成和运行 |
| `refactor-cleaner.md` | 死代码清理专家 | 重构、清理未使用代码 |
| `doc-updater.md` | 文档同步专家 | 保持文档与代码同步 |

#### 学习要点

1. **代理结构**: 每个 agent 包含 name、description、tools、model 等元数据
2. **委托时机**: 何时应该委托给子代理而非直接处理
3. **工具选择**: 不同代理使用的工具集差异
4. **模型选择**: opus vs haiku 的使用场景

#### 示例代理结构

```markdown
---
name: planner
description: 功能实现规划专家
tools: Read, Grep, Glob
model: opus
---

You are an expert planning specialist...
```

---

### 2. commands/ - 斜杠命令系统

**作用**: 提供快速执行的斜杠命令，简化常见工作流程。

#### 文件清单

| 文件 | 命令 | 功能 |
|------|------|------|
| `plan.md` | `/plan` | 创建实现计划，等待确认后再编写代码 |
| `tdd.md` | `/tdd` | 使用测试驱动开发实现功能 |
| `code-review.md` | `/code-review` | 执行代码质量审查 |
| `e2e.md` | `/e2e` | 生成和运行 E2E 测试 |
| `build-fix.md` | `/build-fix` | 修复构建错误 |
| `refactor-clean.md` | `/refactor-clean` | 清理死代码和重构 |
| `learn.md` | `/learn` | 会话中提取模式到可重用技能 |
| `test-coverage.md` | `/test-coverage` | 检查测试覆盖率 |
| `update-codemaps.md` | `/update-codemaps` | 更新代码地图 |
| `update-docs.md` | `/update-docs` | 更新文档 |

#### 学习要点

1. **命令设计**: 如何设计高效的命令流程
2. **代理集成**: 命令如何调用对应的 agents
3. **用户交互**: 命令执行过程中的用户确认机制
4. **工作流编排**: 多个命令的组合使用

---

### 3. contexts/ - 上下文系统

**作用**: 根据不同模式动态注入系统提示词上下文。

#### 文件清单

| 文件 | 模式 | 行为特点 |
|------|------|----------|
| `dev.md` | 开发模式 | 先写代码后解释，优先工作解决方案 |
| `review.md` | 审查模式 | 专注代码审查，发现问题 |
| `research.md` | 研究模式 | 探索和分析代码库 |

#### 学习要点

1. **上下文切换**: 不同模式的行为差异
2. **优先级管理**: 模式如何影响任务优先级
3. **工具选择**: 不同模式下偏好的工具

---

### 4. hooks/ - 钩子系统

**作用**: 基于事件的自动化触发器，在特定工具操作时自动执行。

#### 目录结构

```
hooks/
├── hooks.json              # 所有钩子配置
├── memory-persistence/     # 会话生命周期钩子
│   ├── pre-compact.sh
│   ├── session-start.sh
│   └── session-end.sh
└── strategic-compact/      # 压缩建议钩子
    └── suggest-compact.sh
```

#### 钩子类型

| 钩子类型 | 触发时机 | 用途 |
|----------|----------|------|
| `PreToolUse` | 工具使用前 | 验证、阻止、修改操作 |
| `PostToolUse` | 工具使用后 | 格式化、检查、通知 |
| `PreCompact` | 上下文压缩前 | 保存状态 |
| `SessionStart` | 会话开始时 | 加载上下文 |
| `SessionEnd` | 会话结束时 | 持久化学习 |
| `Stop` | 会话停止时 | 最终检查 |

#### 示例钩子功能

- **开发服务器保护**: 阻止在 tmux 外运行开发服务器
- **Git push 确认**: 推送前打开编辑器审查
- **console.log 警告**: 自动检测并警告调试语句
- **TypeScript 检查**: 编辑 TS 文件后自动类型检查
- **自动格式化**: 编辑后自动运行 Prettier

---

### 5. rules/ - 规则系统

**作用**: 定义必须遵守的编码规范和最佳实践。

#### 文件清单

| 文件 | 规范领域 | 核心内容 |
|------|----------|----------|
| `security.md` | 安全 | 密钥管理、输入验证、漏洞防护 |
| `coding-style.md` | 编码风格 | 不可变性、文件组织、代码格式 |
| `testing.md` | 测试 | TDD、80% 覆盖率要求 |
| `git-workflow.md` | Git 工作流 | 提交格式、PR 流程 |
| `agents.md` | 代理使用 | 何时委托给子代理 |
| `performance.md` | 性能 | 模型选择、上下文管理 |
| `patterns.md` | 设计模式 | 常用模式和反模式 |
| `hooks.md` | 钩子规范 | 钩子编写指南 |

#### 学习要点

1. **模块化**: 规则按功能分离到不同文件
2. **强制性**: Rules vs 其他配置的区别
3. **检查清单**: 提交前的安全检查
4. **最佳实践**: 编码规范的具体示例

---

### 6. skills/ - 技能系统

**作用**: 工作流定义和领域知识，可由 commands 或 agents 调用。

#### 目录结构

```
skills/
├── coding-standards.md         # 通用编码规范
├── backend-patterns.md         # 后端模式 (API、数据库、缓存)
├── frontend-patterns.md        # 前端模式 (React、Next.js)
├── clickhouse-io.md            # ClickHouse 数据库操作
├── project-guidelines-example.md
├── continuous-learning/        # 持续学习技能
│   └── config.json
├── strategic-compact/          # 战略压缩技能
├── tdd-workflow/               # TDD 工作流
│   └── SKILL.md
└── security-review/            # 安全审查技能
    └── SKILL.md
```

#### 学习要点

1. **技能定义**: 如何编写可重用的工作流
2. **领域知识**: 特定技术栈的模式和最佳实践
3. **技能组合**: 多个技能的协同使用
4. **持续学习**: 从会话中自动提取模式

---

### 7. mcp-configs/ - MCP 配置系统

**作用**: 配置 Model Context Protocol 服务器，扩展 Claude Code 的外部服务集成能力。

#### 文件清单

`mcp-servers.json` - 包含所有 MCP 服务器配置

#### 已配置的 MCP 服务器

| 服务器 | 功能 | 用途 |
|--------|------|------|
| `github` | GitHub 操作 | PR、Issues、仓库管理 |
| `firecrawl` | 网页抓取 | Web 抓取和爬取 |
| `supabase` | 数据库操作 | Supabase 数据库 |
| `memory` | 持久化记忆 | 跨会话记忆 |
| `sequential-thinking` | 思维链推理 | 复杂推理 |
| `vercel` | Vercel 部署 | 部署和项目管理 |
| `railway` | Railway 部署 | Railway 部署 |
| `cloudflare-*` | Cloudflare 服务 | 文档、构建、绑定、监控 |
| `clickhouse` | ClickHouse 查询 | 分析查询 |
| `context7` | 文档查找 | 实时文档查找 |
| `magic` | UI 组件 | Magic UI 组件 |
| `filesystem` | 文件系统操作 | 文件系统访问 |

#### 学习要点

1. **上下文警告**: 不要同时启用过多 MCP（保持在 10 个以下）
2. **配置方式**: 环境变量和命令参数
3. **禁用策略**: 使用 `disabledMcpServers` 按项目禁用

---

### 8. examples/ - 示例配置

**作用**: 提供项目级和用户级的配置示例。

#### 文件清单

| 文件 | 用途 |
|------|------|
| `CLAUDE.md` | 项目级配置示例 |
| `user-CLAUDE.md` | 用户级配置示例 |
| `statusline.json` | 状态栏配置示例 |
| `sessions/` | 示例会话日志文件 |

---

### 9. plugins/ - 插件生态

**作用**: 插件系统文档和市场指南。

#### 推荐插件

**开发类:**
- `typescript-lsp` - TypeScript 智能提示
- `pyright-lsp` - Python 类型检查
- `hookify` - 对话式创建钩子

**代码质量:**
- `code-review` - 代码审查
- `pr-review-toolkit` - PR 自动化
- `security-guidance` - 安全检查

**搜索类:**
- `mgrep` - 增强搜索（优于 ripgrep）
- `context7` - 实时文档查找

---

## 核心概念

### Agents vs Commands vs Skills

| 类型 | 作用 | 触发方式 | 示例 |
|------|------|----------|------|
| **Agents** | 专业子代理，处理委托任务 | 自动或手动调用 | `planner` 代理创建实现计划 |
| **Commands** | 斜杠命令，快速执行工作流 | 用户输入 `/command` | `/plan` 调用 planner 代理 |
| **Skills** | 可重用的工作流和领域知识 | 被 agents/commands 调用 | `coding-standards` 技能提供编码规范 |

### Context Window 管理

**重要原则**: 上下文窗口是有限资源（200k tokens），需要谨慎管理。

**最佳实践**:
- 配置 20-30 个 MCP，但每个项目保持 10 个以下启用
- 活跃工具数量控制在 80 个以内
- 使用钩子进行战略性压缩
- 使用记忆持久化跨会话保存重要信息

### Hooks 工作流程

```
会话开始
    │
    ▼ SessionStart Hook
加载之前的上下文
    │
    ▼ (用户操作)
    ├─ PreToolUse Hook (验证/阻止)
    ├─ 工具执行
    ├─ PostToolUse Hook (格式化/检查)
    │
    ▼ (上下文压缩触发)
    ├─ PreCompact Hook (保存状态)
    ├─ 压缩执行
    │
    ▼ Stop Hook
最终检查 + 持久化学习
```

---

## 快速开始

### 1. 复制配置

```bash
# 克隆仓库
git clone https://github.com/affaan-m/everything-claude-code.git

# 复制 agents
cp everything-claude-code/agents/*.md ~/.claude/agents/

# 复制 rules
cp everything-claude-code/rules/*.md ~/.claude/rules/

# 复制 commands
cp everything-claude-code/commands/*.md ~/.claude/commands/

# 复制 skills
cp -r everything-claude-code/skills/* ~/.claude/skills/
```

### 2. 配置 Hooks

将 `hooks/hooks.json` 中的内容复制到 `~/.claude/settings.json`。

### 3. 配置 MCP

从 `mcp-configs/mcp-servers.json` 复制需要的 MCP 服务器到 `~/.claude.json`。

**重要**: 将 `YOUR_*_HERE` 占位符替换为实际的 API 密钥。

### 4. 学习路径建议

1. **初学者**: 阅读 [Shorthand Guide](https://x.com/affaanmustafa/status/2012378465664745795)
2. **进阶用户**: 阅读 [Longform Guide](https://x.com/affaanmustafa/status/2014040193557471352)
3. **实践应用**: 从 `commands/` 开始尝试常用命令
4. **深入学习**: 探索 `agents/` 和 `skills/` 了解高级功能

---

## 贡献指南

欢迎贡献！如果您有：
- 有用的 agents 或 skills
- 巧妙的 hooks
- 更好的 MCP 配置
- 改进的 rules

请查看 [CONTRIBUTING.md](../CONTRIBUTING.md) 了解贡献指南。

---

## 许可证

MIT - 可自由使用和修改，如能贡献回来则更好。

---

**相关资源**:
- **Shorthand Guide**: [The Shorthand Guide to Everything Claude Code](https://x.com/affaanmustafa/status/2012378465664745795)
- **Longform Guide**: [The Longform Guide to Everything Claude Code](https://x.com/affaanmustafa/status/2014040193557471352)
- **作者**: [@affaanmustafa](https://x.com/affaanmustafa)
- **获奖作品**: [zenith.chat](https://zenith.chat)
