# Octane 自动安装

## 使用方法

1. 下载本项目并解压
2. 下载 `resources.zip`（见下方资源下载）并解压
3. 将解压后的文件夹 `resources` 放在项目文件夹根目录，使项目文件结构为：

    ```text
    OCauto/
    ├── main.py                 # 主程序
    ├── resources/              # 资源文件夹
    │   ├── thirdparty/         # Octane缓存文件夹
    │   ├── c4doctane/          # C4D插件文件夹
    │   ├── license             # Octane许可证文件
    │   ├── otoy_credentials    # Octane凭证文件
    │   ├── YellowStar.exe      # 启动项程序
    │   └── YellowStar.xdl64    # C4D插件文件
    └── README.md               # 项目说明文件
    ```

4. 安装项目依赖

   ```bash
        pip install -r requirements.txt
   ```

5. 检查 `config.py` 中的路径是否正确
6. 运行 `main.py` 进行安装

## 资源下载

resources.zip，SHA-256：

```SHA-256
0D62E0225ADFD4C649F3F528AD6583569D86C5CF886051D3A225A7C6AB5BD3F0
```

- 百度网盘[下载](https://pan.baidu.com/s/1ZB7asLxufmB_hv1d7_wkKg?pwd=7r3k)，提取码：7r3k
- 夸克网盘[下载](https://pan.quark.cn/s/7fe8fdd8b2e6)，提取码：U521
