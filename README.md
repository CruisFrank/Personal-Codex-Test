# 初中物理电路图绘制器 1.0

该项目提供一个基于 PyQt5 的初中物理电路图绘制器，可通过拖放方式组合电路元件。

## 功能特性

- 组件库包含常见的初中物理实验元件：电源、开关、电流表、电压表、滑动变阻器、定值电阻、电阻箱、小灯泡、电动机、电铃、单刀双掷开关等。
- 画布带有网格背景，支持缩放、框选、拖动对齐。
- 工具栏提供导线绘制、旋转、删除、清空等操作。
- “关于”对话框内容留空以满足题目要求。

## 运行

```bash
pip install -r requirements.txt
python -m app.main
```

## 打包为 Windows 可执行文件

项目提供了预配置的 PyInstaller 打包脚本，输出会被移动到仓库根目录下的 `release/` 文件夹。以下是面向初学者的详细步骤：

1. **准备环境**
   - 在 Windows 电脑上安装 [Python 3.10 或更新版本](https://www.python.org/downloads/windows/)，安装时勾选“Add python.exe to PATH”。
   - 打开“开始菜单 → Windows PowerShell”或“命令提示符”。
   - 使用 `cd` 命令切换到项目所在的文件夹，例如：`cd C:\Users\你的用户名\Downloads\Personal-Codex-Test`。

2. **安装依赖**
   - 输入并执行：`pip install -r requirements.txt pyinstaller`
   - 如果提示 `pip` 未找到，请重新打开终端或手动将 Python 的 `Scripts` 目录加入环境变量。

3. **运行打包脚本**
   - 在项目根目录执行：`python packaging/win/build_release.py`
   - 首次运行时 PyInstaller 会创建临时缓存，过程可能持续数分钟；终端停在“Building”阶段属正常现象。

4. **查找生成的文件**
   - 脚本完成后，会在 `release/CircuitDesigner-1.0/` 目录生成 `CircuitDesigner-1.0.exe`。
   - 同时生成的 `release/CircuitDesigner-1.0.zip` 便于分享或上传到 GitHub Release。

> 由于当前运行环境无法访问外网，无法在此直接生成 exe 文件。请在可联网的 Windows 环境中执行上述脚本以获得最终产物。

## 项目结构

```
app/
  components.py   # 电路元件图形定义
  main.py         # 应用程序入口
packaging/
  win/            # Windows 打包配置与脚本
release/          # 打包输出目录（需在本地构建）
requirements.txt  # 运行依赖
```
