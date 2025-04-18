# TianWen-1
目前功能包括爬取天问一号所有磁场数据文件名，自动下载天问一号磁场数据（需要登录获取Cookies，替换掉代码中用户名和密码即可）
Current functions include crawling all the magnetic field data file names of Tianwen-1, and automatically downloading the magnetic field data of Tianwen-1
(you need to log in to get Cookies, and replace the user name and password in the code)
# TianWen-1 MOMAG Download
对于磁场数据，包含了两种下载方式，第一种是在https://moon.bao.ac.cn/web/zhmanager/kxsj?missionName=HX1&zhName=MOMAG&grade=2C 下载，这需要爬取cookies，利用 download_TW1_data()函数下载，这种方式可以下载1Hz或32Hz数据。
另一种方式是利用download_TW1MOMAG_USTC()函数在https://space.ustc.edu.cn/dreams/tw1_momag/?magdata=cal下载1Hz或32Hz数据。当然，第一种下载数据方法可以扩展，下载TIANWEN-1其他仪器的数据。
For magnetic field data, download includes two kinds of ways, the first is a download at https://moon.bao.ac.cn/web/zhmanager/kxsj?missionName=HX1&zhName=MOMAG&grade=2C, the need to climb take cookies, The download_TW1_data() function can be used to download 1Hz or 32Hz data. Another way is to use download_TW1MOMAG_USTC()Function in the https://space.ustc.edu.cn/dreams/tw1_momag/?magdata=cal download 1 hz or 32 hz data. Of course, the first method of downloading data can be extended to download data from other instruments of TIANWEN-1.

#2025/4/18 
The current functionalities available in **Tianwen1_MAVEN_GUI** include:
Downloading TianWen-1 magnetic field data, downloading MAVEN magnetic field and plasma data, and an interactive interface.
