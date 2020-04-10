# COVID-19_Tracking
基于Python+Flask+Echarts的疫情爬虫&amp;数据可视化项目
***
## 步骤
>* Python网络爬虫
>* 使用Python与MySQL数据库交互
>* 使用Flask构建web项目
>* 基于Echarts数据可视化展示
>* 在Linux上部署web项目及爬虫

</br>

## 项目环境
>* Python 3.7
>* MySQL 8.0.17
>* Flask 1.1.1
>*   Linux上:
>>*        阿里云 CentOS 8.0 64位
>>*         Python3.6
>>*         MySQL 8.0

## IDE
> Pycharm / Vscode / Sublime

</br>

## 具体介绍及项目过程
> 

</br>

## 文件说明
>* app.py是flask的运行程序，整体项目也是运行它
>* spider.py是爬取各种数据并存入数据库的，定时爬虫就是定时运行它
>* utils.py是数据库的相关操作的封装，spider.py中会调用它的函数
>* templates/中
>>* index.html和test.html是写项目过程中用于测试用的，和项目运行无关，可删
>>* main.html是前端页面

## 运行方式：
> ### **本地win10上:**
	>> &emsp;&emsp;在mysql数据库中新建cov数据库，并在其中新建3张表details,history,hotsearch——具体见博客</br>
	>> &emsp;&emsp;在utils.py和spider.py中更改get_conn函数中的数据库连接，host,user,password，db </br>
	>> &emsp;&emsp;运行spider.py爬取数据写入到mysql中</br>
	>> &emsp;&emsp;运行app.py</br></br>
> ### **远程主机上:**</br>
	>> &emsp;&emsp;具体配置请见博客
