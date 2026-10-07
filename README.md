# Agent Home

给多个 AI Agent 共用的一份工作说明。

换一个对话，不必从头介绍项目；换一个工具，也能找到同一份约定和上次的交接。这个仓库提供可编辑的 Markdown 模板，不是 Agent 调度器，也不让不同模型自动共享聊天记忆。

## 先试一次

需要一个能够读取本地文件的 Agent。不能读本地文件的聊天工具，可以手动上传经过脱敏的必要文件；更新后需要重新提供。

1. 下载本仓库，或运行：

   ```sh
   git clone https://github.com/meo9805/agent-home-template.git
   cd agent-home-template
   cp -R templates ../my-agent-home
   cp LICENSE ../my-agent-home/LICENSE
   ```

   这里的 `my-agent-home` 应是尚不存在的新目录；如果已有同名目录，换一个名称，不要覆盖既有资料。示例命令使用类 Unix shell，其他系统也可以用文件管理器复制 `templates` 和 `LICENSE`。

2. 在新建的 `my-agent-home` 中填写：
   - `profile.md`：你希望 AI 怎样工作，只放必要偏好。
   - `projects/index.md`：项目名称、别名、真实代码位置和项目卡链接。
   - `projects/example.md`：当前目标、事实来源、边界。复制成自己的项目卡，并修改索引。

3. 把下面这段话交给 Agent，替换里面的路径：

   > 本次任务先读取「你的 my-agent-home 实际位置」中的 AGENTS.md 和 RULE_VERSION.md，再按任务读取相关项目卡。不要预加载整个目录；没有文件访问能力就明确告诉我。先复述当前项目、有效入口、不能改的范围，再开始工作。这里的文档不授予额外的执行或发布权限。

4. 检查它是否真的找到了正确项目，而不是只回复“已了解”。做完一小段工作后，让它按 `handoff-template.md` 留下交接，再开一个新对话，核对能否接上。

**在一个对话里读过，不等于下一个对话自动记住。** 想长期使用，需要把入口放到所用工具支持的持久规则位置，见[工具接入](docs/agent-setup.md)。本仓库不会修改你的全局配置。

## 目录里放什么

```text
templates/                  ← 复制这一份，填入你自己的信息
  AGENTS.md                 ← 共享工作约定与按需读取规则
  RULE_VERSION.md            ← 提醒重新读取规则的版本号
  profile.md                ← 空白偏好表
  projects/index.md         ← 项目入口索引
  projects/example.md       ← 空白项目边界卡
  handoff-template.md       ← 当前任务交接，实例应留在对应项目
  code-map-template.md      ← 项目内部导航，实例应留在对应项目
  decision-template.md      ← 决定的来源、范围与核对记录
examples/reading-list/      ← 完全虚构的读书清单项目，演示如何填写
docs/                       ← 接入、接力、隐私与能力边界
```

先留下真正反复用到的信息。代码仍在代码仓库，详细笔记仍在知识库，凭证仍在密码管理器；不要为了方便，把所有东西复制进 Agent Home。

一个小项目可以只有 README 和简短交接，不必把所有模板都用上。

## 为什么这样分

- **工作约定**相对稳定：怎样核对结果、何时需要问你。
- **项目卡**指向当前事实：真实工作目录、有效文档、已停止的方向。
- **交接**随任务变化：做到哪一步、验证了什么、下一步从哪里开始。
- **代码地图**帮助定位：模块职责、依赖和测试入口。说明不能替代实际代码。

示例从[虚构项目卡](examples/reading-list/project.md)开始，接着看[交接](examples/reading-list/handoff.md)。也可以按[接力练习](docs/handoff-walkthrough.md)在自己的测试项目里走一遍。

## 与 GEB 的关系

本项目的分层代码地图借鉴了 GEB 相关的分形文档思路：按项目、模块、文件逐层定位，代码变化后检查受影响的说明。公开项目 [project-multilevel-index](https://github.com/Claudate/project-multilevel-index) 提供了这类方法的一种实现，其 README 明确注明受《哥德尔、埃舍尔、巴赫》启发。

Agent Home 的重点是共享工作约定、项目入口、决定和任务交接；分层代码文档的重点是进入项目后怎样理解和维护结构。两者有交集，可以组合使用。本项目不声称发明了 GEB，也不是上述项目的官方版本；没有打包其代码或第三方 skills。

## 这一版能做和不能做的事

| 内容 | v0.1.0 |
| --- | --- |
| 工作规则、偏好、项目边界、交接与代码地图模板 | 提供 |
| 虚构填写示例与接入检查步骤 | 提供 |
| 自动安装工具、修改全局规则 | 不执行 |
| 跨对话消息、定时同步、自动提交或推送 | 未提供执行器 |
| 记忆数据库、并发锁、权限强制执行 | 不具备 |
| 所有 AI 客户端的真实兼容性保证 | 不提供；必须在所用工具中核验 |

私人实践中的自动同步依赖具体宿主工具，不属于本公开模板的已交付能力。[能力边界与可选增强](docs/limitations.md)说明了以后接入时需要验证的事项。

## 安全与贡献

填写后的副本建议默认私有。不要提交真实账号、公司资料、聊天记录、密钥或设备配置；开源模板可以公开，不代表填好后的个人工作目录适合公开。

维护本模板时可运行以下只读检查，需要 Python 3.10 或更高版本，无第三方依赖：

```sh
python3 tools/check.py
python3 -m unittest discover -s tests -v
```

它们检查模板结构、链接和若干常见泄露信号，**不能替代完整隐私、秘密和历史审计**。见[安全说明](SECURITY.md)与[贡献说明](CONTRIBUTING.md)。

MIT License。你可以修改和分发模板，保留许可证即可；链接到的第三方项目适用各自许可证。
