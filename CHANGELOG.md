# Changelog

# [Unreleased]

- 新增功能
    - 修改`ds`命令含义，是从当前目录向上递归寻找`dryadsfile`文件

- Bug修复
    - 对参数检测禁止空格
    - help option显示help option本身

- 改进
    - help option的表现形式

- 移除或者废弃的功能

# [1.2.0] - 2024-1-17

- 新增功能：创建可执行文件`ds`，以用户根目录的`dryadsfile`作为执行脚本

# [1.1.1] - 2024-1-17

第一次提交到PyPI，实验性提交

- 新增功能：
    - 建立基本框架，将命令行项目描述为或者要维护的脚本组织为树形结构

      树中基本元素：
      中间节点类型为`dict`，
      叶子节点类型为`str`或者`list[str | DryadsFlag]`，
      其中中间节点的键的类型为`str`、`DryadsFlag`或者`tuple[str]`，值的类型为中间节点或叶子节点

    - 提供若干枚举标记，即`DryadsFlag`