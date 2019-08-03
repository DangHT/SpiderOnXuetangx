# SpiderOnXuetangx
:spider:一个可以爬取学堂在线全部课程信息的爬虫

爬虫的实现基于[Scrapy](https://scrapy.org/)框架

# 运行方法
1. 首先需要安装python环境:point_right:[获取python](https://wiki.python.org/moin/BeginnersGuide/Download)

2. 安装Scrapy:point_right:[安装步骤](https://docs.scrapy.org/en/latest/intro/install.html)

3. 安装MongoDB:point_right:[获取MongoDB](https://www.mongodb.com/download-center/community)

  *（注意:在安装过程中可以选择安装MongoDB Compass，这是一个可视化工具，使用它操作数据库会更方便）*

4. clone本项目到本地

5. 在**项目目录下**打开终端

6. 执行命令

   ```bash
   scrapy crawl courses
   ```

   可以看到正在爬取数据

   ![](https://github.com/DangHT/SpiderOnXuetangx/raw/master/SpiderOnXuetangx/images/runtime.jpg)

7. 爬取结束后，即可根据所选的持久化存储方法查看数据

   

# 数据持久化存储方法

修改数据持久化方法可以在项目的settings.py文件中修改ITEM_PIPLINES中对应pipeline的优先级即可

![](https://github.com/DangHT/SpiderOnXuetangx/raw/master/SpiderOnXuetangx/images/pipeline.jpg)

目前本项目提供以下方式进行数据持久化存储：

1. 存入MongoDB，可以通过MongoDB Compass查看

   ![](https://github.com/DangHT/SpiderOnXuetangx/raw/master/SpiderOnXuetangx/images/mongodb.jpg)

2. 以csv文件存储，默认新建在项目根目录下

   ![](https://github.com/DangHT/SpiderOnXuetangx/raw/master/SpiderOnXuetangx/images/csv.jpg)