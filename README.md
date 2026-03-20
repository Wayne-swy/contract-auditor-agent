# Contract Auditor Agent 合同风险自动审计员

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> AI 驱动的智能合同审计工具，自动识别合同中的法律风险和陷阱

---

## 项目简介

**Contract Auditor Agent** 是一个基于 AI 的合同审计技能，专注于自动识别和分析合同文本中的潜在法律风险。它能够帮助法务人员、企业管理者和普通用户快速发现合同中的问题条款，提供修改建议，降低法律风险。

### 核心能力

- **风险识别**：自动检测合同中的不平等条款、模糊表述和潜在陷阱
- **合规检查**：对照法律法规和行业标准进行合规性验证
- **智能报告**：生成结构化的审计报告，包含风险等级和修改建议
- **多场景支持**：适用于劳动合同、商业合同、服务协议等多种场景

---

## 目标用户

| 用户类型 | 使用场景 |
|---------|---------|
| **法务人员** | 快速初审合同，提高工作效率 |
| **中小企业主** | 在签署前自查合同风险 |
| **个人用户** | 理解劳动合同、租房合同等个人协议 |
| **律师助理** | 辅助完成合同审查工作 |

---

## 使用方法

### 前提条件

- 已安装 Claude Code 或支持 Skill 的 Claude 环境
- 本技能需要配置到 Claude Code 的 skill 目录中

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/Wayne-swy/contract-auditor-agent.git

# 将 skill 目录复制到 Claude Code 的 skills 目录
# Windows: %USERPROFILE%\.claude\skills\
# macOS/Linux: ~/.claude/skills/
cp -r contract-auditor-skill ~/.claude/skills/contract-auditor
```

### 使用方式

在 Claude Code 中调用本技能：

```bash
/contract-auditor
```

或直接上传合同文本并请求审计：

```
请帮我审计这份合同，查找潜在风险点...
```

### 输出示例

审计后生成的报告包含：

1. **核心要素摘要** - 合同名称、签署双方等基本信息
2. **风险预警** - 按风险等级列出问题条款
3. **修改建议** - 针对每个风险点提供具体修改方案
4. **审计结论** - 通过/修改后通过/不建议签署

---

## 项目结构

```
contract-auditor-skill/
├── SKILL.md                 # 技能定义和配置
├── README.md                # 项目说明文档
├── assets/
│   └── report-template.md   # 审计报告输出模板
└── references/
    ├── checklist.md         # 审计检查清单
    └── legal-guidelines.md  # 法律法规和合规指南
```

### 文件说明

| 文件 | 用途 |
|-----|------|
| `SKILL.md` | 定义技能的角色、工作流程和约束条件 |
| `checklist.md` | 必查清单，包含主体身份、金额期限、违约责任等检查项 |
| `legal-guidelines.md` | 详细的法律依据，包含 SWC 分类、证券法合规、数据隐私等 |
| `report-template.md` | 审计报告的输出格式模板 |

---

## 审计维度

### 检查清单（checklist.md）

- 主体身份验证
- 金额与期限逻辑
- 违约责任条款
- 争议解决方式

### 法律依据（legal-guidelines.md）

- 安全红线（重入攻击、权限控制、逻辑缺陷等）
- SWC 智能合约弱点分类（125 项）
- 证券法合规（Howey 测试）
- 数据隐私（GDPR）
- 金融监管（DeFi、KYC/AML）

---

## 注意事项

> **免责声明**：本工具生成的审计报告仅供参考，不构成法律建议。重要合同请咨询专业律师。

- 本技能不会修改合同原意，仅标记风险点
- 审计结果不能替代专业法律意见
- 建议对重要合同进行多重审计

---

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 贡献

欢迎提交 Issue 和 Pull Request！

---

## 联系方式

- GitHub: [@Wayne-swy](https://github.com/Wayne-swy)
- 项目仓库: [contract-auditor-agent](https://github.com/Wayne-swy/contract-auditor-agent)

---

*最后更新：2026-03-20*
