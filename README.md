# pywallpaper

![](https://img.shields.io/github/v/tag/colinxu2020/pywallpaper?include_prereleases&sort=semver)
![](https://img.shields.io/github/repo-size/colinxu2020/pywallpaper)
![](https://img.shields.io/github/languages/code-size/colinxu2020/pywallpaper)
![](https://img.shields.io/badge/total%20lines-100-blue.svg)

**pyWallPaper可以从Bing接口(默认)获取图片并设为壁纸**

# 用法
- 先运行 init.py 安装第三方库
- 通过 config.toml 自定义源(自带 Bing 源)
- 运行 main.py 获取最新壁纸并设为桌面
- 运行 run_schedule.pyw 定时设置桌面

# 优点
- 支持自定义获取源
- 提供定时支持

# 许可证
**GNU AFFERO GENERAL PUBLIC LICENSE**

# todo
- [ ] GUI支持(十分有限的支持,位于 ui.py )
- [ ] 视频支持
- [x] 自定义获取源(通过配置文件)
- [x] 定时支持(通过第三方库schedule)下