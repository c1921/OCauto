import os

# 基础路径配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR = os.path.join(BASE_DIR, "resources")

# 目标路径配置
FOLDERS = {
    "C4D 程序插件目录": r"C:\Program Files\Maxon Cinema 4D 2023\plugins",
    "C4D 用户插件目录": r"C:\Users\Administrator\AppData\Roaming\Maxon\Maxon Cinema 4D 2023_BCDB4759\plugins",
    "Octane 缓存目录": r"C:\Users\Administrator\AppData\Local\OctaneRender",
    "Octane 配置目录": r"C:\Users\Administrator\AppData\Roaming\OctaneRender"
}

# 需要复制的文件配置
COPY_ITEMS = [
    {
        "source": os.path.join(RESOURCE_DIR, "thirdparty"),
        "target": FOLDERS["Octane 缓存目录"],
        "is_folder": True
    },
    {
        "source": os.path.join(RESOURCE_DIR, "license"),
        "target": FOLDERS["Octane 配置目录"],
        "is_folder": False
    },
    {
        "source": os.path.join(RESOURCE_DIR, "otoy_credentials"),
        "target": FOLDERS["Octane 配置目录"],
        "is_folder": False
    },
    {
        "source": os.path.join(RESOURCE_DIR, "c4doctane"),
        "target": FOLDERS["C4D 程序插件目录"],
        "is_folder": True
    },
    {
        "source": os.path.join(RESOURCE_DIR, "YellowStar.xdl64"),
        "target": FOLDERS["C4D 程序插件目录"],
        "is_folder": False
    }
]

# 启动项配置
STARTUP_CONFIG = {
    "dir": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup",
    "file": "YellowStar.exe"
}

# 资源文件配置
REQUIRED_RESOURCES = [
    ("thirdparty", True),
    ("c4doctane", True),
    ("license", False),
    ("otoy_credentials", False),
    ("YellowStar.exe", False),
    ("YellowStar.xdl64", False)
] 