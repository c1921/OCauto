import os
import shutil
import subprocess
import logging
from datetime import datetime
from config import *
from tqdm import tqdm

# 设置日志
def setup_logging():
    log_dir = os.path.join(BASE_DIR, "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, f"OCauto_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

class YellowStarInstaller:
    def __init__(self):
        setup_logging()
        self.logger = logging.getLogger(__name__)

    def clear_folder(self, folder_path, folder_name):
        """清理指定文件夹的内容"""
        try:
            if not os.path.exists(folder_path):
                self.logger.warning(f"{folder_name}不存在！")
                return False
                
            items = os.listdir(folder_path)
            for item in tqdm(items, desc=f"清理{folder_name}"):
                item_path = os.path.join(folder_path, item)
                try:
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                except Exception as e:
                    self.logger.error(f"删除 {item} 时出错: {str(e)}")
                    return False
                    
            self.logger.info(f"{folder_name}清理完成！")
            return True
            
        except Exception as e:
            self.logger.error(f"处理{folder_name}时发生错误: {str(e)}")
            return False

    def copy_items(self, source, target, is_folder=False):
        """复制文件或文件夹到目标目录"""
        try:
            if not os.path.exists(source):
                self.logger.error(f"源路径 {source} 不存在！")
                return False
            
            if not os.path.exists(target):
                os.makedirs(target)
                self.logger.info(f"已创建目标目录: {target}")
            
            if is_folder:
                # 获取源文件夹中的所有文件和总大小
                total_size = 0
                file_list = []
                for root, _, files in os.walk(source):
                    for file in files:
                        file_path = os.path.join(root, file)
                        file_size = os.path.getsize(file_path)
                        total_size += file_size
                        file_list.append((file_path, file_size))
                
                # 使用进度条显示复制进度
                with tqdm(total=total_size, unit='B', unit_scale=True, 
                         desc=f"复制 {os.path.basename(source)}", 
                         postfix={"文件数": len(file_list)}) as pbar:
                    def copy_with_progress(src, dst, file_list):
                        if not os.path.exists(dst):
                            os.makedirs(dst)
                        for src_path, file_size in file_list:
                            rel_path = os.path.relpath(src_path, src)
                            dst_path = os.path.join(dst, rel_path)
                            # 确保目标文件夹存在
                            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                            # 使用缓冲区复制文件
                            buffer_size = 1024 * 1024  # 1MB buffer
                            with open(src_path, 'rb') as fsrc:
                                with open(dst_path, 'wb') as fdst:
                                    while True:
                                        buffer = fsrc.read(buffer_size)
                                        if not buffer:
                                            break
                                        fdst.write(buffer)
                                        pbar.update(len(buffer))
                    
                    target_path = os.path.join(target, os.path.basename(source))
                    copy_with_progress(source, target_path, file_list)
            else:
                # 单个文件复制时显示进度条
                file_size = os.path.getsize(source)
                with tqdm(total=file_size, unit='B', unit_scale=True, 
                         desc=f"复制 {os.path.basename(source)}") as pbar:
                    buffer_size = 1024 * 1024  # 1MB buffer
                    with open(source, 'rb') as fsrc:
                        with open(os.path.join(target, os.path.basename(source)), 'wb') as fdst:
                            while True:
                                buffer = fsrc.read(buffer_size)
                                if not buffer:
                                    break
                                fdst.write(buffer)
                                pbar.update(len(buffer))
            
            self.logger.info(f"已成功复制: {os.path.basename(source)}")
            return True
            
        except Exception as e:
            self.logger.error(f"复制过程中发生错误: {str(e)}")
            return False

    def check_and_copy_startup(self):
        """检查并复制启动项文件"""
        try:
            startup_path = os.path.join(STARTUP_CONFIG["dir"], STARTUP_CONFIG["file"])
            
            # 检查启动项文件是否存在
            if not os.path.exists(startup_path):
                self.logger.warning(f"\n未检测到启动项 {STARTUP_CONFIG['file']}，准备复制...")
                
                # 修正：从资源目录获取源文件
                source_path = os.path.join(RESOURCE_DIR, STARTUP_CONFIG["file"])
                
                if os.path.exists(source_path):
                    shutil.copy2(source_path, startup_path)
                    self.logger.info(f"已成功将 {STARTUP_CONFIG['file']} 复制到启动项目录")
                else:
                    self.logger.error(f"错误：源文件 {STARTUP_CONFIG['file']} 不存在！")
                    return False
            else:
                self.logger.info(f"\n启动项 {STARTUP_CONFIG['file']} 已存在")
            return True
            
        except Exception as e:
            self.logger.error(f"处理启动项时发生错误: {str(e)}")
            return False

    def ensure_resource_folder(self):
        """确保资源文件夹存在并包含所需文件"""
        try:
            # 如果资源文件夹不存在，创建它
            if not os.path.exists(RESOURCE_DIR):
                os.makedirs(RESOURCE_DIR)
                self.logger.info("已创建资源文件夹")
            
            # 使用配置文件中的资源列表
            for item_name, is_folder in REQUIRED_RESOURCES:
                source = os.path.join(BASE_DIR, item_name)
                target = os.path.join(RESOURCE_DIR, item_name)
                
                # 检查源文件/文件夹是否存在
                if os.path.exists(source):
                    try:
                        # 如果目标已存在，先删除
                        if os.path.exists(target):
                            if is_folder:
                                shutil.rmtree(target)
                            else:
                                os.remove(target)
                        
                        # 移动文件/文件夹
                        shutil.move(source, target)
                        self.logger.info(f"已移动 {item_name} 到资源文件夹")
                    except Exception as e:
                        self.logger.error(f"移动 {item_name} 时出错: {str(e)}")
                        return False
                else:
                    self.logger.warning(f"警告：{item_name} 不存在于根目录")
            
            return True
            
        except Exception as e:
            self.logger.error(f"处理资源文件夹时发生错误: {str(e)}")
            return False

    def run_yellowstar(self):
        """运行 YellowStar.exe"""
        try:
            # 获取 YellowStar.exe 的路径（从资源文件夹）
            resource_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
            exe_path = os.path.join(resource_dir, "YellowStar.exe")
            
            if not os.path.exists(exe_path):
                self.logger.error("错误：未找到 YellowStar.exe")
                return False
                
            self.logger.info("\n正在启动 YellowStar.exe...")
            # 使用 subprocess 运行程序
            subprocess.Popen(exe_path)
            self.logger.info("YellowStar.exe 已启动")
            return True
            
        except Exception as e:
            self.logger.error(f"启动 YellowStar.exe 时发生错误: {str(e)}")
            return False

    def run(self):
        """执行主要安装流程"""
        try:
            self.logger.info("开始执行安装流程...")
            
            # 确保资源文件夹结构正确
            if not self.ensure_resource_folder():
                return False
            
            # 清理文件夹
            for folder_name, folder_path in FOLDERS.items():
                if not self.clear_folder(folder_path, folder_name):
                    return False
            
            # 使用配置文件中的复制项
            for item in COPY_ITEMS:
                if not self.copy_items(item["source"], item["target"], item["is_folder"]):
                    return False
            
            # 设置启动项
            if not self.check_and_copy_startup():
                return False
            
            # 运行程序
            if not self.run_yellowstar():
                return False
            
            self.logger.info("安装流程成功完成！")
            return True
            
        except Exception as e:
            self.logger.error(f"安装过程中发生错误: {str(e)}")
            return False

def main():
    print("="*50)
    print("OCAUTO")
    print("="*50)
    
    # 显示操作列表
    print("\n即将执行以下操作：")
    for i, folder in enumerate(FOLDERS.keys(), 1):
        print(f"{i}. 清理 {folder}")
    print(f"{len(FOLDERS) + 1}. 复制所需文件")
    print(f"{len(FOLDERS) + 2}. 设置启动项")
    print(f"{len(FOLDERS) + 3}. 运行 Yellow Star")
    
    # 确认执行
    if input("\n确定要执行以上操作吗？(y/n): ").lower() != 'y':
        print("操作已取消")
        input("\n按回车键退出...")
        return
    
    # 执行安装
    installer = YellowStarInstaller()
    if installer.run():
        print("\n" + "="*50)
        print("安装成功完成！")
        print("="*50)
    else:
        print("\n" + "="*50)
        print("安装过程中出现错误，请查看日志文件！")
        print("="*50)
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    main()