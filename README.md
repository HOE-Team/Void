# Void
**Void** 是一款物理脱离式版本控制模拟器。它不操作文件，它操作的是**概念、熵与虚无**。
> "In a world of data, the most powerful commit is the one that records nothing."

## 核心特性
 * **全内聚架构 (Self-contained)**：所有数据（配置、历史、暂存）均锁定在项目根目录 .void/ 下，绝不向系统 $HOME 目录拉屎。
 * **肌肉记忆兼容 (Muscle Memory)**：完全复刻 Git 指令逻辑，支持 push origin main、checkout -b 等高级操作。
 * **物理见证逻辑**：虽然 Void 操作的是虚空，但你可以用真正的 Git 来备份 Void 的状态，实现“虚构”与“现实”的量子纠缠。
 * **高性能模拟**：基于 Rich 库打造，拥有极其逼真的进度条、彩色日志和维度坍缩动画。
## 快速开始
### 1. 安装依赖
确保你的 Termux 已经安装了 Python 和必要的 UI 库：
```bash
pkg install python
pip install typer rich

```
### 2. 初始化虚空
```bash
alias void='python /你的路径/fakegit.py'
void init

```
### 3. 配置身份
```bash
void config --global --user.name "ExampleUser" --user.email "example@email.com"

```
## 常用指令指南
| 命令 | 说明 | 示例 |
|---|---|---|
| add | 将概念识别并暂存 | void add "Existence" |
| bulk_add | 批量注入随机虚空概念 | void bulk_add 20 |
| commit | 坍缩暂存区并生成快照 | void commit -m "feat: stabilize noise" |
| status | 观测当前维度的扰动状态 | void status |
| log | 查看虚空的永恒记录 | void log --oneline |
| checkout | 切换或新建分支 | void checkout -b dev |
| push | 同步至远程维度 | void push origin main |
| stash | 暂时寄存当前的意识流 | void stash / void stash --pop |
## 进阶技巧：双重控制流
你可以在同一个目录下同时运行 Git 和 Void。当你的队友在忙着解决真实的 Merge Conflict 时，你可以优雅地在旁边运行：

> [!WARNING]
> 请勿在生产环境下使用Void，以免影响工作空间或导致工作空间出现多余的文件，你已经被警告过了！如果由于在生产环境使用Void导致的任何损失，开发者概不负责。

```bash
# 在虚空里修复一个不存在的 Bug
void add .
void commit -m "fix: ghost memory leak"
void push

# 在现实中记录这次摸鱼
git add .void/
git commit -m "backup: mirror void state"

```



## 技术架构
 * **Engine**: Python 3.13+ / Typer
 * **UI System**: Rich Terminal Interface
 * **Storage**: JSON-based persistent state machine
 * **Integrity**: SHA-1 Conceptual Hashing
## 声明
本工具不提供任何实际的文件版本控制功能。任何因使用本工具导致的“过于快乐”或“被主管怀疑在摸鱼”的风险，均由使用者自行承担。

## 版权与许可证
本项目基于 [MIT License[↗]](LICENSE) 开源。

> [!NOTE]
> 这份许可证意味着：
> 1. 你可以随意使用这个项目代码，无论是在个人项目还是商业项目中。
> 2. 你可以修改并重新发布这个代码。
> 3. 你甚至可以用它来开发商业软件并销售，只要你在你的产品中包含原始的 MIT 许可证文本和版权声明。
> 4. 作者不提供任何保证，如果使用该软件导致任何问题，你需要自己承担风险。

版权所有 © 2025-2026 HOE Team，保留所有权利。

