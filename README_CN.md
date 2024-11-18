# Renweb 作业获取工具

这是一个自动从Renweb获取作业列表的工具。程序会自动登录你的Renweb账号，并获取所有作业信息。

## 所需文件清单

使用前请确保你有以下所有文件：
1. `python-3.x.x-amd64.exe` - Python安装程序
2. `wing-9.1.2.0.exe` - Wing IDE编辑器安装程序
3. `msedgedriver.exe` - Edge浏览器驱动程序
4. `main.py` - 主程序文件
5. `Download the required libraries.cmd` - 安装必要库的脚本

## 使用前准备

1. 安装Python环境
   - 双击运行文件夹中的 `python-3.x.x-amd64.exe`
   - 安装时必须勾选 "Add Python to PATH"
   ![Python安装界面](<PIC/Python install.png>)
   - 点击 "Install Now" 开始安装

2. 安装开发环境(Wing IDE)
   - 双击运行文件夹中的 `wing-9.1.2.0.exe`
   - 按照默认选项完成安装即可
   - 首次运行时会自动检测Python安装路径

3. 安装必要的库
   - 双击运行 `Download the required libraries.cmd`
   - 等待安装完成，窗口会自动关闭

4. 准备浏览器驱动
   - 默认使用Microsoft Edge浏览器
   - 将 `msedgedriver.exe` 放在与 `main.py` 相同的目录下
   
   如果你想使用Chrome浏览器：
   1. 检查你的Chrome版本
      - 打开Chrome
      - 点击右上角三个点
      - 点击"帮助" > "关于Google Chrome"
      - 记下版本号
   
   2. 下载对应版本的ChromeDriver
      - 访问 https://chromedriver.chromium.org/downloads
      - 下载与你的Chrome版本相匹配的驱动
      - 解压下载的文件
   
   3. 配置驱动路径
      - 将chromedriver.exe放在任意位置
      - 在 `main.py` 开头找到 `driver_path` 变量
      - 填入chromedriver.exe的完整路径，例如：
      ```python
      driver_path = "C:/WebDriver/chromedriver.exe"  # 改为你的chromedriver路径
      ```
      - 如果放在当前目录，可以直接写：
      ```python
      driver_path = "chromedriver.exe"
      ```

## 配置程序

1. 用Wing IDE打开 `main.py`
2. 修改文件开头的登录信息：
```python
username = "...@..."  # 改为你的Renweb用户名
password = "......."  # 改为你的Renweb密码
```
![配置界面](<PIC/Code Change.png>)

## 运行程序
![IDE界面](<PIC/IDE interface.png>)
1. 在Wing IDE中打开 `main.py`
2. 点击工具栏的运行按钮（绿色三角形图标）或按F5
3. 程序会自动：
   - 打开浏览器
   - 登录账号
   - 获取作业
   - 显示作业信息
   - 关闭浏览器

## 常见问题解决

1. 提示 "msedgedriver.exe not found"
   - 检查驱动文件是否在正确位置

2. 提示 "Module not found"
   - 重新运行库安装脚本

3. 无法登录
   - 检查用户名密码
   - 检查网络连接

4. Wing IDE无法运行Python
   - 检查Python安装时是否勾选了"Add Python to PATH"
   - 重启Wing IDE
   - 在Wing IDE中检查Python解释器设置（编辑 > 首选项 > Python配置）