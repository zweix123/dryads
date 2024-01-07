有功能类似的工具[Just](https://github.com/casey/just)，但是个人认为我的用起来比它的简单。

# Dryad

非侵入式命令行构建工具以及脚本管理工具

+ 推荐阅读: [Line Interface Guidelines](https://clig.dev/)
+ 如果构建工业级命令行项目，推荐其他框架，比如argparse，click，typer~~实际就是推荐typer~~，不过理论上本框架也行

+ 使用该框架的实例
  + [BusTub lab test script](https://github.com/zweix123/bustub_2023spring_backup/blob/master/script.py#L146): [介绍](https://github.com/zweix123/CS-notes/blob/master/README.md#CMU15445)
  + [Note Analysis Tool](https://github.com/zweix123/CS-notes/blob/master/script.py#L205)

+ 发心：

  命令行软件也是软件，那么怎么描述我们的需求呢？不断添加修饰词，如果把相同的修饰词汇总起来，这就形成一个树形结构。

  我们拿我们在CMU15445的过程中遇到需求，在这个过程中，测试，格式化，打包，每个动作都需要对应的一系列的命令，而每个动作还能细分，比如Lab分成多个Project，每个Project分成多个Task，于是就可能出现“测试Project1 Task1相关代码”，同理，其实格式化和打包也有类似的，所以这就是一个树形结构。

  我们再进一步，我们发现同是脚本语言，Python的表意能力要比Bash强得多，如果运维相关的操作有点复杂，用Python实现可能要比Bash实现容易的多。

  或者说，如果我们有一系列的命令，比如独立的或者需要一起执行一批命令同时还需要能执行其中的部分，这样的情况也可以将其根据选项描述成树形结构

## Install

目前该库没有放到PyPI，但是可以通过下面命令安装
```bash
pip install git+https://github.com/zweix123/dryad.git@master
```

## Use

我们只需要描述好树形结构即可，即通过`dict`类型的变量，参数解析和执行交给框架
```python
# test/example.py
from dryad import Dryad, DryadContainer, DryadFlag, run_shell_cmd


def create_python():
    run_shell_cmd(f"poetry new {DryadContainer.DryadArg}")


def create_rust():
    run_shell_cmd(f"cargo new {DryadContainer.DryadArg}")


cmd_tree = {
    "echo": {
        "English": "echo Hello World",
        "Chinese": "echo 我可以吞下玻璃而不收到伤害",
        "Math": ["echo 42", "echo 3.14"],
    },
    "work": {
        DryadFlag.PrefixCmd: ["cd Project"],
        "build": "cd build && make -j`nproc`",
        "run": "./build/bin/work",
    },
    "create": {
        "python": [
            DryadFlag.Anchoring,
            DryadFlag.AcceptArg,
            create_python,
        ],
        "rust": [
            DryadFlag.Anchoring,
            DryadFlag.AcceptArg,
            create_rust,
        ],
    },
    ("-d", "--dryad"): "echo Hello Dryad",
}


Dryad(cmd_tree)
```

+ 基本元素：
  + 以嵌套的`dict`来描述树形结构
  + `dict`的键只能是`str`或者`tuple[str]`来描述选项
    + `tuple`即多选项
  + 叶子节点为`str`/`Callable`/`list[str | Callable]`类型表示具体的命令执行内容
    + 每个str作为一个shell脚本一起交给shellypx
      + 如果命令中包含`cd`，需要放在一个`str`字面量中

+ `--help`: help option比不可少
  + 根help option：`python3 script.py`/`python3 script.py -h`/`python3 script.py --help`
    ```bash
    该脚本命令可分为两大类
      Shell Commands, help会输出命令本身
      Python Function, help会输出函数的__doc__
    echo English: echo Hello World
    echo Chinese: echo 我可以吞下玻璃而不收到伤害
    echo Math: echo 42
              echo 3.14
    work DryadFlag.PrefixCmd: cd Project
    work build: cd build && make -j`nproc`
    work run: ./build/bin/work
    create python: DryadFlag.Anchoring
                  DryadFlag.AcceptArg
                  Create Python
    create rust: DryadFlag.Anchoring
                DryadFlag.AcceptArg
                Create Rust
    -d/--dryad: echo Hello Dryad
    env: Print Dryad environment variable.
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
  + `DryadFlag.Anchoring`: 作为叶子的值，表示该叶子中的命令都是以执行脚本的路径开始, 默认从脚本所在的路径开始, 例子在[Anchoring](./test/flag_anchring.py)
  + `DryadFlag.AcceptArg`: 作为叶子的值, 表示该选项还接收一个可选参数, 并将参数放在变量DryadArg中, 例子在[AcceptArg](./test/flag_accept_arg_valid.py), 还有两个非法的例子, [AcceptArg Invalid](./test/flag_accept_arg_invalid1.py) | [AcceptArg Invalid](./test/flag_accept_arg_invalid2.py)
  + `DryadFlag.InVisible`: 作为叶子的值, 表示执行的脚本是否打印, 默认打印, 使用该标志表示不打印, 例子在[InVisible](./test/flag_invisiable.py)
  + `DryadFlag.IgnoreErr`: 作为叶子的值, 表示命令执行出错后是否停止, 默认停止, 使用该标志表示不停止, 例子在[IgnoreErr](./test/flag_ignore_err.py)
  + `DryadFlag.PrefixCmd`: 作为某个节点的键, 其值对应的脚本为子树中所有脚本的前置脚本, 例子在[PrefixCmd](./test/flag_prefix_cmd.py)

## TODO

+ 缩进支持中文
+ debug: help option显示`-h/--help`本身
