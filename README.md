# Dryads

非侵入式命令行构建工具以及脚本管理工具

+ 类似工具: [Just](https://github.com/casey/just)
+ 如果构建工业级命令行项目，推荐其他框架，比如argparse，click，typer，不过理论上本框架也行
+ 推荐阅读：[Line Interface Guidelines](https://clig.dev/)

+ 使用该框架的实例：
  + [BusTub lab test script](https://github.com/zweix123/bustub_2023spring_backup/blob/master/script.py#L146): [介绍](https://github.com/zweix123/CS-notes/blob/master/README.md#CMU15445)
  + [Note Analysis Tool](https://github.com/zweix123/CS-notes/blob/master/script.py#L205)

+ 发心：

  命令行软件也是软件，那么人类是怎么将需求传达给机器的呢？即参数和选项，形象的说，如果把命令行软件当作人类与机器交通的工具的话，参数和选项就是修饰词。而围绕某一个事物的各种修饰词，将其相同的部分汇总并依次连接，很容易形成树形结构。即很多命令行软件的选项设计可以总结为树形结构。

  拿我在CMU15445 Lab的过程遇到的需求来说，这个过程，测试、格式化、打包等等每个动作都对应一系列命令，而每个动作还能细分，比如Lab分成多个Project，每个Project分成多个Task，于是就可能出现“测试Project1 Task1相关代码”，同理，格式化和打包操作也类似，所以形成了如下树形结构（以Json表示）：
  ```json
  {
    "Test": {
      "Project1": {
        "Task1": ...,
        "Task2": ..., 
        ..., 
      },
      "Project2": ..., 
      ...
    },
    "Format": ...,
    "Submit": ..., 
  }
  ```
  而这里的每个指令，都是由一系列Shell命令实现的；几乎不可能记忆所有的命令，而将对应的命令放在对应的指令下，则可以自由使用

  如果把Shell脚本换成一个个Python函数，则这就形成了一个命令行程序

  即使不考虑命令行程序，即使同是脚本语言，Python的表意能力要比Bash强得多，如果运维相关的操作有点复杂，使用Python实现可能要比Bash实现容易的多。

  这个工具极大的提高了我的工作效率。

## Install

+ 通过PyPI：
    ```bash
    pip install dryads
    ```

    同时会下载可执行文件`ds`/`ds.exe`，它会执行路径为`~/dryadsfile`的使用该框架的正常脚本

+ 通过源代码下载：

    ```bash
    pip install git+https://github.com/zweix123/dryads.git@master
    ```

## Use

如果是在Linux系统，通过在脚本前添加shebang
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
```
则可以通过`./script.py`这种很接近命令的形式使用

我们只需要描述好树形结构即可，即通过`dict`类型的变量，参数解析和执行交给框架，下面是一个简单的例子
```python
# test/example.py
from dryads import Dryads, DryadsContainer, DryadsFlag, run_shell_cmd

def create_python():
    run_shell_cmd(f"poetry new {DryadsContainer.DryadsArg}")

def create_rust():
    run_shell_cmd(f"cargo new {DryadsContainer.DryadsArg}")

CMDS = {
    "echo": {
        "English": "echo Hello World",
        "Chinese": "echo 我可以吞下玻璃而不受到伤害",
        "Math": ["echo 42", "echo 3.14"],
    },
    "work": {
        DryadsFlag.PrefixCmd: ["cd Project"],
        "build": "cd build && make -j`nproc`",
        "run": "./build/bin/work",
    },
    "create": {
        "python": [
            DryadsFlag.Anchoring,
            DryadsFlag.AcceptArg,
            create_python,
        ],
        "rust": [
            DryadsFlag.Anchoring,
            DryadsFlag.AcceptArg,
            create_rust,
        ],
    },
    ("-d", "--dryads"): "echo Hello Dryads",
}

Dryads(CMDS)
```

+ 基本元素：
  + 以嵌套的`dict`来描述树形结构
  + `dict`的键只能是`str`或者`tuple[str]`来描述选项
    + `tuple`即多选项
  + 叶子节点为`str`/`Callable`/`list[str | Callable]`类型表示具体的命令执行内容
    + 每个str作为一个shell脚本一起交给shellypx
      + 如果命令中包含`cd`，需要放在一个`str`字面量中

+ `--help`: help option必不可少
  + 根help option：`python3 script.py`/`python3 script.py -h`/`python3 script.py --help`
    ```bash
    该脚本命令可分为两大类
      Shell Commands, help会输出命令本身
      Python Function, help会输出函数的__doc__
    echo English: echo Hello World
    echo Chinese: echo 我可以吞下玻璃而不受到伤害
    echo Math: echo 42
              echo 3.14
    work DryadsFlag.PrefixCmd: cd Project
    work build: cd build && make -j`nproc`
    work run: ./build/bin/work
    create python: DryadsFlag.Anchoring
                  DryadsFlag.AcceptArg
                  Create Python
    create rust: DryadsFlag.Anchoring
                DryadsFlag.AcceptArg
                Create Rust
    -d/--dryads: echo Hello Dryads
    env: Print Dryads environment variable.
    ```

  + 各选项help option：在任意选项后，都可以添加help option查看之后的命令
    ```bash
    > python example.py echo --help
    该脚本命令可分为两大类
      Shell Commands, help会输出命令本身
      Python Function, help会输出函数的__doc__
    echo English: echo Hello World
    echo Chinese: echo 我可以吞下玻璃而不收到伤害
    echo Math: echo 42
               echo 3.14
    ```

+ 执行：一个命令相当于从根到叶子的路径
  + 叶子节点：
    ```bash
    > python example.py echo Chinese
    echo 我可以吞下玻璃而不收到伤害
    我可以吞下玻璃而不收到伤害
    ```

  + 中间节点：执行该节点子树中的所有叶子节点
    ```bash
    > python example.py echo 
    echo Hello World
    Hello
    World
    echo 我可以吞下玻璃而不收到伤害
    我可以吞下玻璃而不收到伤害
    echo 42
    42
    echo 3.14
    3.14
    ```

+ 标记
  + `DryadsFlag.Anchoring`: 作为叶子的值, 表示该叶子中的命令都是以执行脚本的路径开始, 默认从脚本所在的路径开始, 例子在[Anchoring](./test/flag_anchring.py)
  + `DryadsFlag.AcceptArg`: 作为叶子的值, 表示该选项还接收一个可选参数, 并将参数放在变量DryadsArg中, 例子在[AcceptArg](./test/flag_accept_arg_valid.py), 还有两个非法的例子, [AcceptArg Invalid](./test/flag_accept_arg_invalid1.py) | [AcceptArg Invalid](./test/flag_accept_arg_invalid2.py)
  + `DryadsFlag.InVisible`: 作为叶子的值, 表示执行的脚本是否打印, 默认打印, 使用该标志表示不打印, 例子在[InVisible](./test/flag_invisiable.py)
  + `DryadsFlag.IgnoreErr`: 作为叶子的值, 表示命令执行出错后是否停止, 默认停止, 使用该标志表示不停止, 例子在[IgnoreErr](./test/flag_ignore_err.py)
  + `DryadsFlag.PrefixCmd`: 作为某个节点的键, 其值对应的脚本为子树中所有脚本的前置脚本, 例子在[PrefixCmd](./test/flag_prefix_cmd.py)
    + 该标记只能用于`dict`不能用于`list`，但是我们往往是对叶子节点`list`中的一系列命令设置前置脚本，通过再套一层dict解决。

## TODO

+ 缩进支持中文
+ 美化`help`效果
+ debug: help option显示`-h/--help`本身
