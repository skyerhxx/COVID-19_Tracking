import requests
import json
import time
import pymysql
from selenium.webdriver import Chrome,ChromeOptions
import traceback
import sys

#返回历史数据和当日详细数据
def get_tencent_data():
    url1 = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    url2 = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_other"
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
    }
    r1 = requests.get(url1, headers)
    r2 = requests.get(url2, headers)

    #json字符串转字典
    res1 = json.loads(r1.text)
    res2 = json.loads(r2.text)

    data_all1 = json.loads(res1["data"])
    data_all2 = json.loads(res2["data"])

    #历史数据
    history = {}
    for i in data_all2["chinaDayList"]:
        ds = "2020." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")  # 匹配时间
        ds = time.strftime("%Y-%m-%d", tup)  #改变时间输入格式，不然插入数据库会报错，数据库是datatime格式
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        history[ds] = {"confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead}
    for i in data_all2["chinaDayAddList"]:
        ds = "2020." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")  # 匹配时间
        ds = time.strftime("%Y-%m-%d", tup)  #改变时间输入格式，不然插入数据库会报错，数据库是datatime格式
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        history[ds].update({"confirm_add": confirm, "suspect_add": suspect, "heal_add": heal, "dead_add": dead})

    #当日详细数据
    details = []
    update_time = data_all1["lastUpdateTime"]
    data_country = data_all1["areaTree"]  #list 25个国家
    data_province = data_country[0]["children"] #中国各省
    for pro_infos in data_province:
        province = pro_infos["name"] #省名
        for city_infos in pro_infos["children"]:
            city = city_infos["name"]
            confirm = city_infos["total"]["confirm"]
            confirm_add = city_infos["today"]["confirm"]
            heal = city_infos["total"]["heal"]
            dead = city_infos["total"]["dead"]
            details.append([update_time, province, city, confirm, confirm_add, heal, dead])
    return history, details


def get_conn():
	#建立连接
	conn = pymysql.connect(host="127.0.0.1", user="root", password="root", db="cov", charset="utf8")
	#创建游标
	cursor = conn.cursor()
	return conn,cursor

def close_conn(conn,cursor):
	if cursor:
		cursor.close()
	if conn:
		conn.close()

#插入details数据
def update_details():
	cursor = None
	conn = None
	try:
		li = get_tencent_data()[1] #0是历史数据，1是当日详细数据
		conn,cursor = get_conn()
		sql = "insert into details(update_time,province,city,confirm,confirm_add,heal,dead) values(%s,%s,%s,%s,%s,%s,%s)"
		sql_query = "select %s=(select update_time from details order by id desc limit 1)"  #对比当前最大时间戳
		#对比当前最大时间戳
		cursor.execute(sql_query,li[0][0])
		if not cursor.fetchone()[0]:
			print(f"{time.asctime()}开始更新数据")
			for item in li:
				cursor.execute(sql,item)
			conn.commit()
			print(f"{time.asctime()}更新到最新数据")
		else:
			print(f"{time.asctime()}已是最新数据！")
	except:
		traceback.print_exc()
	finally:
		close_conn(conn,cursor)


#插入history数据
def insert_history():
    cursor = None
    conn = None
    try:
        dic = get_tencent_data()[0]#0代表历史数据字典
        print(f"{time.asctime()}开始插入历史数据")
        conn,cursor = get_conn()
        sql = "insert into history values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for k,v in dic.items():
            cursor.execute(sql,[k, v.get("confirm"),v.get("confirm_add"),v.get("suspect"),
                           v.get("suspect_add"),v.get("heal"),v.get("heal_add"),
                           v.get("dead"),v.get("dead_add")])
        conn.commit()
        print(f"{time.asctime()}插入历史数据完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn,cursor)


#更新历史数据
def update_history():
    cursor = None
    conn = None
    try:
        dic = get_tencent_data()[0]#0代表历史数据字典
        print(f"{time.asctime()}开始更新历史数据")
        conn,cursor = get_conn()
        sql = "insert into history values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = "select confirm from history where ds=%s"
        for k,v in dic.items():
            if not cursor.execute(sql_query,k):
                cursor.execute(sql,[k, v.get("confirm"),v.get("confirm_add"),v.get("suspect"),
                               v.get("suspect_add"),v.get("heal"),v.get("heal_add"),
                               v.get("dead"),v.get("dead_add")])
        conn.commit()
        print(f"{time.asctime()}历史数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn,cursor)


#返回百度疫情热搜
def get_baidu_hot():
	option = ChromeOptions() #创建谷歌浏览器实例
	option.add_argument("--headless")#隐藏浏览器
	option.add_argument("--no-sandbox")  #禁用沙盘    部署在linux上访问chrome要求这样
	
	url = 'https://voice.baidu.com/act/virussearch/virussearch?from=osari_map&tab=0&infomore=1'
	brower = Chrome(options = option)
	brower.get(url)
	#找到展开按钮
	but = brower.find_element_by_css_selector('#ptab-0 > div > div.VirusHot_1-5-5_32AY4F.VirusHot_1-5-5_2RnRvg > section > div') #定位到点击展开按钮
	but.click() #点击展开

	time.sleep(1)#爬虫与反爬，模拟人等待1秒
	
	c = brower.find_elements_by_xpath('//*[@id="ptab-0"]/div/div[2]/section/a/div/span[2]')
	context = [i.text for i in c]  #获取标签内容
	print(context)
	return context


#将疫情热搜插入数据库
def update_hotsearch():
	cursor = None
	conn = None
	try:
		context = get_baidu_hot()
		print(f"{time.asctime()}开始更新热搜数据")
		conn, cursor = get_conn()
		sql = "insert into hotsearch(dt,content) values(%s,%s)" 
		ts = time.strftime("%Y-%m-%d %X")
		for i in context:
			cursor.execute(sql,(ts,i))  #插入数据
		conn.commit() #提交事务保存数据
		print(f"{time.asctime()}数据更新完毕")
	except:
		traceback.print_exc()
	finally:
		close_conn(conn,cursor)



# his,de = get_tencent_data()
# print(his)
# print(de)
if __name__ == "__main__":
    l = len(sys.argv)
    if l == 1:
        s = """
        请输入参数
        参数说明，
        up_his 更新历史记录表
        up_hot 更新实时热搜
        up_det 更新详细表
        """
        print(s)
    else:
        order = sys.argv[1]
        if order == "up_his":
            update_history()
        elif order == "up_det":
            update_details()
        elif order == "up_hot":
            update_hotsearch()