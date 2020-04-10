from selenium.webdriver import Chrome,ChromeOptions
import time

option = ChromeOptions()
option.add_argument("--headless")#隐藏浏览器
option.add_argument("--no-sandbox")  #禁用沙盘    部署在linux上访问chrome要求这样
url = 'https://voice.baidu.com/act/virussearch/virussearch?from=osari_map&tab=0&infomore=1'

brower = Chrome(options = option)
#brower = Chrome()
brower.get(url)
but = brower.find_element_by_css_selector('#ptab-0 > div > div.VirusHot_1-5-5_32AY4F.VirusHot_1-5-5_2RnRvg > section > div') #定位到点击展开按钮
but.click() #点击展开


time.sleep(1)#爬虫与反爬，模拟人等待1秒
c = brower.find_elements_by_xpath('//*[@id="ptab-0"]/div/div[2]/section/a/div/span[2]')
for i in c:
	print(i.text)
