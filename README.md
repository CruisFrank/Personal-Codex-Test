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

使用 [PyInstaller](https://pyinstaller.org/) 可在 Windows 平台打包为独立的 `exe` 文件：

```bash
pip install pyinstaller
pyinstaller --name circuit-designer --noconsole --onefile app/main.py
```

生成的可执行文件位于 `dist/circuit-designer.exe`。

## 项目结构

```
app/
  components.py   # 电路元件图形定义
  main.py         # 应用程序入口
requirements.txt  # 运行依赖
```
