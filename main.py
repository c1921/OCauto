import os
import shutil
import subprocess

def clear_folder(folder_path, folder_name):
    """清理指定文件夹的内容"""
    try:
        if not os.path.exists(folder_path):
            print(f"{folder_name}不存在！")
            return False
            
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            try:
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                print(f"已删除: {item}")
            except Exception as e:
                print(f"删除 {item} 时出错: {str(e)}")
                return False
                
        print(f"{folder_name}清理完成！")
        return True
        
    except Exception as e:
        print(f"处理{folder_name}时发生错误: {str(e)}")
        return False

def copy_items(source, target, is_folder=False):
    """复制文件或文件夹到目标目录"""
    try:
        if not os.path.exists(source):
            print(f"源路径 {source} 不存在！")
            return False
        
        if not os.path.exists(target):
            os.makedirs(target)
            print(f"已创建目标目录: {target}")
        
        if is_folder:
            target_path = os.path.join(target, os.path.basename(source))
            shutil.copytree(source, target_path)
        else:
            shutil.copy2(source, target)
        
        print(f"已成功复制: {os.path.basename(source)}")
        return True
        
    except Exception as e:
        print(f"复制过程中发生错误: {str(e)}")
        return False

def check_and_copy_startup():
    """检查并复制启动项文件"""
    startup_dir = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"
    startup_file = "YellowStar.exe"
    startup_path = os.path.join(startup_dir, startup_file)
    
    try:
        # 检查启动项文件是否存在
        if not os.path.exists(startup_path):
            print(f"\n未检测到启动项 {startup_file}，准备复制...")
            
            # 获取源文件路径（从resources文件夹）
            resource_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
            source_path = os.path.join(resource_dir, startup_file)
            
            if os.path.exists(source_path):
                shutil.copy2(source_path, startup_path)
                print(f"已成功将 {startup_file} 复制到启动项目录")
            else:
                print(f"错误：resources文件夹中未找到 {startup_file}！")
                return False
        else:
            print(f"\n启动项 {startup_file} 已存在")
        return True
        
    except Exception as e:
        print(f"处理启动项时发生错误: {str(e)}")
        return False

def check_resource_folder():
    """检查资源文件夹是否存在并包含所需文件"""
    try:
        # 获取当前脚本所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        resource_dir = os.path.join(current_dir, "resources")
        
        # 检查资源文件夹是否存在
        if not os.path.exists(resource_dir):
            print("错误：未找到resources文件夹！")
            return False
        
        # 需要检查的文件和文件夹列表
        required_items = [
            ("thirdparty", True),
            ("c4doctane", True),
            ("license", False),
            ("otoy_credentials", False),
            ("YellowStar.exe", False),
            ("YellowStar.xdl64", False)
        ]
        
        # 检查必需的文件/文件夹是否存在
        missing_items = []
        for item_name, is_folder in required_items:
            item_path = os.path.join(resource_dir, item_name)
            if not os.path.exists(item_path):
                missing_items.append(item_name)
        
        if missing_items:
            print(f"警告：resources文件夹中缺少以下文件/文件夹：{', '.join(missing_items)}")
            print("程序将跳过缺失的文件...")
        else:
            print("resources文件夹检查完成，所有必需文件都存在")
        
        return True
        
    except Exception as e:
        print(f"检查资源文件夹时发生错误: {str(e)}")
        return False

def run_yellowstar():
    """运行 YellowStar.exe"""
    try:
        # 获取 YellowStar.exe 的路径（从资源文件夹）
        resource_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
        exe_path = os.path.join(resource_dir, "YellowStar.exe")
        
        if not os.path.exists(exe_path):
            print("错误：未找到 YellowStar.exe")
            return False
            
        print("\n正在启动 YellowStar.exe...")
        # 使用 subprocess 运行程序
        subprocess.Popen(exe_path)
        print("YellowStar.exe 已启动")
        return True
        
    except Exception as e:
        print(f"启动 YellowStar.exe 时发生错误: {str(e)}")
        return False

def clear_and_copy():
    try:
        # 检查资源文件夹是否存在
        if not check_resource_folder():
            print("资源文件夹检查失败，是否继续？(y/n): ")
            if input().lower() != 'y':
                return False
        
        # 定义需要清理的文件夹路径
        folders_to_clear = {
            "C4D程序插件目录": r"C:\Program Files\Maxon Cinema 4D 2023\plugins",
            "C4D用户插件目录": r"C:\Users\Administrator\AppData\Roaming\Maxon\Maxon Cinema 4D 2023_BCDB4759\plugins",
            "Octane缓存目录": r"C:\Users\Administrator\AppData\Local\OctaneRender",
            "Octane配置目录": r"C:\Users\Administrator\AppData\Roaming\OctaneRender"
        }
        
        # 执行清理
        for folder_name, folder_path in folders_to_clear.items():
            print(f"\n开始清理{folder_name}...")
            if not clear_folder(folder_path, folder_name):
                return False
        
        # 获取资源文件夹路径
        resource_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
        
        # 定义需要复制的文件和文件夹
        items_to_copy = [
            # Octane相关文件
            (os.path.join(resource_dir, "thirdparty"), r"C:\Users\Administrator\AppData\Local\OctaneRender", True),
            (os.path.join(resource_dir, "license"), r"C:\Users\Administrator\AppData\Roaming\OctaneRender", False),
            (os.path.join(resource_dir, "otoy_credentials"), r"C:\Users\Administrator\AppData\Roaming\OctaneRender", False),
            
            # C4D插件相关文件
            (os.path.join(resource_dir, "c4doctane"), r"C:\Program Files\Maxon Cinema 4D 2023\plugins", True),
            (os.path.join(resource_dir, "YellowStar.xdl64"), r"C:\Program Files\Maxon Cinema 4D 2023\plugins", False)
        ]
        
        # 执行复制
        for source, target, is_folder in items_to_copy:
            print(f"\n开始复制 {os.path.basename(source)}...")
            if not copy_items(source, target, is_folder):
                return False
        
        # 检查并复制启动项
        if not check_and_copy_startup():
            return False
            
        # 在所有操作成功完成后运行 YellowStar.exe
        if not run_yellowstar():
            return False
            
        return True
        
    except Exception as e:
        print(f"执行过程中发生错误: {str(e)}")
        return False

def main():
    print("即将执行以下操作：")
    print("1. 检查 resources 文件夹及必需文件")
    print("2. 清理 C4D程序插件目录")
    print("3. 清理 C4D用户插件目录")
    print("4. 清理 Octane缓存目录")
    print("5. 清理 Octane配置目录")
    print("6. 从 resources 复制 thirdparty 文件夹到 Octane缓存目录")
    print("7. 从 resources 复制 license 和 otoy_credentials 文件到 Octane配置目录")
    print("8. 从 resources 复制 c4doctane 文件夹到 C4D插件目录")
    print("9. 从 resources 复制 YellowStar.xdl64 到 C4D插件目录")
    print("10. 从 resources 复制 YellowStar.exe 到系统启动项")
    print("11. 运行 YellowStar.exe")
    
    # 添加确认提示
    confirm = input("\n确定要执行以上操作吗？(y/n): ")
    if confirm.lower() == 'y':
        print("\n开始执行操作...\n")
        if clear_and_copy():
            print("\n" + "="*50)
            print("所有操作已成功完成！")
            print("="*50)
            input("\n按回车键退出...")
        else:
            print("\n" + "="*50)
            print("操作过程中出现错误，请检查以上提示信息！")
            print("="*50)
            input("\n按回车键退出...")
    else:
        print("操作已取消")
        input("\n按回车键退出...")

if __name__ == "__main__":
    main()