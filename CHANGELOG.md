# Changelog

# [2.0.2]

- Bug 修复:

  - 对于空的 internal node 的行为
    - 整个 cmd tree 都是一个空 dict, 可以理解为用户没有设置任何子命令，正常输出
    - internal node 是空 dict，输出{}表示没有内容（之前是对于出现某个中间节点是空，从根节点到这个节点的子命令不显示）

# [2.0.1]

- Bug 修复:

  - 在非终端使用场景，将 dryads 涉及的命令在代码中使用，dryads 的输出以及管理的命令本身的输出可能乱序，因为 dryads 的输出没有刷新缓冲区

- 其他:
  - 项目添加使用 example 作为回归测试的框架

# [2.0.0]

- 改进:
  - 命令行参数修改
    - 去掉 DryadsFlag.AcceptArg, 而是转为自动识别是否有冗余命令行参数
    - 可以接收多个命令行参数, 通过 dryads.argv 获取
  - 调整项目结构, 提高代码可读性

# [1.3.1]

- Bug 修复
  - 对子命令使用 help option bug

# [1.3.0]

- 新增功能

  - 修改`ds`命令含义，是从当前目录向上递归寻找`dryadsfile`文件

- Bug 修复

  - 对参数检测禁止空格
  - help option 显示 help option 本身

- 改进

  - help option 的表现形式

- 移除或者废弃的功能

# [1.2.0] - 2024-1-17

- 新增功能：创建可执行文件`ds`，以用户根目录的`dryadsfile`作为执行脚本

# [1.1.1] - 2024-1-17

第一次提交到 PyPI，实验性提交

- 新增功能：
  - 建立基本框架，将命令行项目描述为或者要维护的脚本组织为树形结构
  - 提供若干枚举标记，即`DryadsFlag`
