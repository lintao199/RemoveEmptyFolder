#!/usr/bin/env python3
"""
查找并删除空文件夹的工具
删除操作会将文件夹移动到回收站而不是永久删除
支持 Windows、macOS、Linux
"""

import os
import sys
import platform
import subprocess


def select_folder():
    """弹出文件夹选择对话框"""
    system = platform.system()

    if system == "Darwin":  # macOS
        script = '''
        tell application "System Events"
            activate
            set folderPath to choose folder with prompt "选择要扫描的文件夹"
            return POSIX path of folderPath
        end tell
        '''
        try:
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except Exception:
            return None

    elif system == "Windows":
        ps_script = '''
        Add-Type -AssemblyName System.Windows.Forms
        $dialog = New-Object System.Windows.Forms.FolderBrowserDialog
        $dialog.Description = "选择要扫描的文件夹"
        if ($dialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
            Write-Output $dialog.SelectedPath
        }
        '''
        try:
            result = subprocess.run(
                ['powershell', '-Command', ps_script],
                capture_output=True,
                text=True
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
            return None
        except Exception:
            return None

    else:  # Linux
        try:
            result = subprocess.run(
                ['zenity', '--file-selection', '--directory', '--title=选择要扫描的文件夹'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except Exception:
            return None


def find_empty_folders(root_path):
    """递归查找所有空文件夹"""
    empty_folders = []

    for dirpath, dirnames, filenames in os.walk(root_path, topdown=False):
        # 跳过隐藏文件夹
        if os.sep + '.' in dirpath or os.path.basename(dirpath).startswith('.'):
            continue

        # 检查文件夹是否为空（没有文件且没有非空子文件夹）
        if not filenames and not dirnames:
            empty_folders.append(dirpath)
        elif not filenames:
            # 检查所有子文件夹是否都是空的
            all_subdirs_empty = all(
                os.path.join(dirpath, d) in empty_folders for d in dirnames
            )
            if all_subdirs_empty:
                empty_folders.append(dirpath)

    return empty_folders


def move_to_trash(path):
    """跨平台移动到回收站"""
    system = platform.system()

    if system == "Darwin":  # macOS
        script = f'''
        tell application "Finder"
            delete POSIX file "{path}"
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, capture_output=True)

    elif system == "Windows":
        # 使用 PowerShell 移动到回收站
        ps_script = f'''
        Add-Type -AssemblyName Microsoft.VisualBasic
        [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteDirectory('{path}', 'OnlyErrorDialogs', 'SendToRecycleBin')
        '''
        subprocess.run(['powershell', '-Command', ps_script], check=True, capture_output=True)

    elif system == "Linux":
        # 使用 gio trash（大多数 Linux 桌面环境支持）
        subprocess.run(['gio', 'trash', path], check=True, capture_output=True)

    else:
        raise OSError(f"不支持的操作系统: {system}")


def main():
    if len(sys.argv) < 2:
        # 没有传入参数时，弹出文件夹选择对话框
        print("请选择要扫描的文件夹...")
        root_path = select_folder()
        if not root_path:
            print("已取消选择")
            sys.exit(0)
    else:
        root_path = os.path.abspath(sys.argv[1])

    if not os.path.isdir(root_path):
        print(f"错误: '{root_path}' 不是一个有效的目录")
        sys.exit(1)

    print(f"正在扫描: {root_path}\n")

    empty_folders = find_empty_folders(root_path)

    if not empty_folders:
        print("✓ 没有找到空文件夹")
        return

    print(f"找到 {len(empty_folders)} 个空文件夹:\n")
    for i, folder in enumerate(empty_folders, 1):
        print(f"  {i}. {folder}")

    print()
    response = input("是否将这些空文件夹移动到回收站? (y/n): ").strip().lower()

    if response == 'y':
        print("\n正在移动到回收站...")
        success_count = 0
        for folder in empty_folders:
            try:
                if os.path.exists(folder):  # 父文件夹可能已被删除
                    move_to_trash(folder)
                    print(f"  ✓ {folder}")
                    success_count += 1
            except Exception as e:
                print(f"  ✗ {folder} - 错误: {e}")

        print(f"\n完成! 已移动 {success_count} 个文件夹到回收站")
    else:
        print("已取消操作")


if __name__ == "__main__":
    main()
