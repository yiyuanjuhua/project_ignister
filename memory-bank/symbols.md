# 🔣 Symbol Reference Guide
*v1.0 | Created: 2025-01-17 | Updated: 2025-01-17*

## 📁 File Symbols
- 📂 = `/memory-bank/` - CursorRIPER♦Σ 内存银行目录
- 📦 = `/memory-bank/backups/` - 备份存储目录
- 📄 = 文件引用
- 📁 = 文件夹引用
- 💻 = 代码引用
- 📚 = 文档引用
- 📏 = 规则引用
- 🔄 = Git 引用
- 📝 = 笔记引用
- 📌 = 固定文件引用

## 🔖 Memory Bank Files (𝕄)
- 𝕄[0] = `📂projectbrief.md` - σ₁ 项目简介
- 𝕄[1] = `📂systemPatterns.md` - σ₂ 系统架构
- 𝕄[2] = `📂techContext.md` - σ₃ 技术上下文
- 𝕄[3] = `📂activeContext.md` - σ₄ 活动上下文
- 𝕄[4] = `📂progress.md` - σ₅ 进度跟踪
- 𝕄[5] = `📂protection.md` - σ₆ 保护注册表

## ⚙️ RIPER Modes (Ω)
- Ω₁ = 🔍 RESEARCH - 研究模式 (`/research`, `/r`)
- Ω₂ = 💡 INNOVATE - 创新模式 (`/innovate`, `/i`)
- Ω₃ = 📝 PLAN - 规划模式 (`/plan`, `/p`)
- Ω₄ = ⚙️ EXECUTE - 执行模式 (`/execute`, `/e`)
- Ω₅ = 🔎 REVIEW - 审查模式 (`/review`, `/rev`)

## 🏗️ Project Phases (Π)
- Π₁ = 🌱 UNINITIATED - 未初始化
- Π₂ = 🚧 INITIALIZING - 初始化中
- Π₃ = 🏗️ DEVELOPMENT - 开发阶段
- Π₄ = 🔧 MAINTENANCE - 维护阶段

## 🛡️ Protection Levels (Ψ)
- Ψ₁ = 🔒 PROTECTED - 受保护 (`!cp`)
- Ψ₂ = 🛡️ GUARDED - 守护 (`!cg`) 
- Ψ₃ = ℹ️ INFO - 信息 (`!ci`)
- Ψ₄ = 🐞 DEBUG - 调试 (`!cd`)
- Ψ₅ = 🧪 TEST - 测试 (`!ct`)
- Ψ₆ = ⚠️ CRITICAL - 关键 (`!cc`)

## 🔐 Permission Types (ℙ)
- ✓ = 完全允许
- ~ = 有限制的允许
- ✗ = 禁止
- C = Create (创建)
- R = Read (读取)
- U = Update (更新) 
- D = Delete (删除)

## 📎 Context References (Γ)
- Γ₁ = 📄 @Files - 文件上下文
- Γ₂ = 📁 @Folders - 文件夹上下文
- Γ₃ = 💻 @Code - 代码上下文
- Γ₄ = 📚 @Docs - 文档上下文
- Γ₅ = 📏 @Cursor Rules - 规则上下文
- Γ₆ = 🔄 @Git - Git 上下文
- Γ₇ = 📝 @Notepads - 笔记上下文
- Γ₈ = 📌 #Files - 固定文件上下文

## 🔄 Operations (𝕋)
```
𝕋[0:3]   = 观察操作 (read_files, ask_questions, observe_code, document_findings)
𝕋[4:6]   = 思考操作 (suggest_ideas, explore_options, evaluate_approaches)
𝕋[7:9]   = 规划操作 (create_plan, detail_specifications, sequence_steps)
𝕋[10:12] = 执行操作 (implement_code, follow_plan, test_implementation)
𝕋[13:15] = 验证操作 (validate_output, verify_against_plan, report_deviations)
```

## 🚨 Safety Protocols (Δ)
- Δ₁ = 破坏性操作保护
- Δ₂ = 阶段转换保护
- Δ₃ = 权限违规处理
- Δ₄ = 错误处理
- Δ₅ = 上下文变更保护

## 🔍 Quick Commands

### Context Commands (Φ_context_commands)
- `!af(file)` = 添加文件引用
- `!ad(folder)` = 添加文件夹引用
- `!ac(code)` = 添加代码引用
- `!adoc(doc)` = 添加文档引用
- `!ar(rule)` = 添加规则引用
- `!ag(git)` = 添加 Git 引用
- `!an(notepad)` = 添加笔记引用
- `!pf(file)` = 固定文件到上下文
- `!cs(ref, status)` = 设置上下文状态
- `!cr(ref)` = 移除上下文引用
- `!cc` = 清空所有上下文引用
- `!cm` = 为当前模式设置上下文

### Permission Commands (Φ_permission_commands)
- `!ckp` = 检查当前模式权限
- `!pm(operation)` = 检查操作是否被允许
- `!sp(mode)` = 显示指定模式的权限
- `!vm(operation)` = 验证操作的适当模式

### Protection Commands (Ψ_commands)
- `!cp` = 添加 PROTECTED 保护
- `!cg` = 添加 GUARDED 保护
- `!ci` = 添加 INFO 保护
- `!cd` = 添加 DEBUG 保护
- `!ct` = 添加 TEST 保护
- `!cc` = 添加 CRITICAL 保护

## 🔗 Cross-Reference Formats
- `[↗️σ₁:R₁]` = 标准交叉引用
- `[↗️σ₁:R₁|Γ₃]` = 带上下文的交叉引用
- `[Γ₃:ClassA]` = 上下文引用
- `[Ψ₁+Γ₃:validate()]` = 保护+上下文引用
- `[ℙ(Ω₁):read_only]` = 权限引用

## 📊 Status Indicators
- 🟢 = 活跃状态
- 🟡 = 部分相关
- 🟣 = 必要状态
- 🔴 = 已废弃
- ✅ = 已完成
- 🔄 = 进行中
- ⏳ = 待开始
- ⚠️ = 有风险 