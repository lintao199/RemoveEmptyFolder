# RemoveEmptyFolder

一个跨平台的空文件夹查找和删除工具，支持 Windows、macOS 和 Linux。

## 功能特点

- **跨平台支持**：兼容 Windows、macOS 和 Linux
- **安全删除**：将空文件夹移动到回收站，而非永久删除
- **图形化选择**：支持弹出文件夹选择对话框
- **递归扫描**：自动递归查找所有空文件夹（包括嵌套的空文件夹）
- **跳过隐藏文件夹**：自动忽略以 `.` 开头的隐藏文件夹
- **交互式确认**：删除前列出所有空文件夹并请求确认

## 使用方法

### 方式一：图形化选择

直接运行脚本，会弹出文件夹选择对话框：

```bash
python find_empty_folders.py
```

### 方式二：命令行指定路径

```bash
python find_empty_folders.py /path/to/folder
```

## 系统要求

- Python 3.x
- **macOS**：使用 AppleScript 和 Finder
- **Windows**：使用 PowerShell
- **Linux**：需要安装 `zenity`（用于图形对话框）和 `gio`（用于回收站功能）

## 示例输出

```
正在扫描: /Users/example/Documents

找到 3 个空文件夹:

  1. /Users/example/Documents/old_project/temp
  2. /Users/example/Documents/backup/empty
  3. /Users/example/Documents/test

是否将这些空文件夹移动到回收站? (y/n): y

正在移动到回收站...
  ✓ /Users/example/Documents/old_project/temp
  ✓ /Users/example/Documents/backup/empty
  ✓ /Users/example/Documents/test

完成! 已移动 3 个文件夹到回收站
```

## 许可证

MIT License
