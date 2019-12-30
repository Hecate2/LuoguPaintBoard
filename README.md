#洛谷冬日绘板
2020年1月1日，洛谷冬日绘板  
https://www.luogu.com.cn/paintBoard  

##鸣谢
首先感谢：  
https://github.com/ouuan/LuoguPaintBoard  
这个项目的图片数据导入工作就用上面这位大佬的/data/ImageToData.py。本仓库的example.bmp，picture.json，ImageToData.py，图片转json.bat都来自这位大佬。  
本仓库的代码功能并不比上面这位大佬的多，但潜在性能十分恐怖。**千万不要**把这些性能全部发挥出来。此外本仓库代码更加花里胡哨，更加适合Python入门者学习。  
  
然后感谢：  
缇亚忒·示巴·伊格那雷奥  
把最先进的宇宙战舰（之一）拿来民用！  

##使用方法
首先需要Python，版本大于等于3.7。安装时注意pip要添加到PATH。确保你的命令行可以正确运行pip。  
然后双击"安装依赖库.bat"。实际上就是pillow，gevent，requests和tornado。我知道可以用pip导出requirement.txt，不过双击bat其实更快更容易哒！  
接着你需要准备需要画的图片。参考https://github.com/ouuan/LuoguPaintBoard。用ImageToData.py输入图片输出json。注意在我的程序中默认输入是picture.json而不是board.json  
最后你需要准备自己的账号。用浏览器登录洛谷，取出cookie，按照示例填入cookie.json。特别注意json文件里的逗号！逗号多了少了都不行。**一个方括号[]或花括号{}中最后一个成员的后面不可以加逗号。**  
  
本程序**支持多个账号**，但**暂不支持一次性多张图片**。硬要支持的话你可以把多张图片的json合为1个文件。**暂不支持各种神奇的修复、随机乱涂操作**（我鸣谢的这位大佬的仓库支持这些操作）。  
  
最后运行LuoguPaintBoard.py！这是一个HTTP服务器。启动后可以用浏览器访问http://localhost:55568。 

##注意
严禁使用宇宙战舰发起CC攻击。  
不要把你的cookie透露给别人。这样几乎等于交出你的账号密码。  