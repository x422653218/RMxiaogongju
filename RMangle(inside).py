from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import re #正则表达式

#日志文件
log=open("log.txt","w")
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
#driver打开网站
r = open("sources\driver路径.txt","r")
d = r.readline().strip('\n')
r.close()
driver=webdriver.Chrome(executable_path=d) #chrome
#driver = webdriver.Chrome()
driver.maximize_window() #全屏
driver.get('http://rmlogic.gmcc.net/rmlogic/reqview/reqViewList.action')
#print(driver.title)
time.sleep(2)
#登录
driver.find_element_by_css_selector('#username').send_keys('wuling2')
driver.find_element_by_css_selector('#password').send_keys('1234qwer@')
driver.find_element_by_css_selector('#loginbtn').click()
print('登录成功')
log.write(rq+" : 登录成功\n")
time.sleep(3)
try:
    driver.find_elements_by_css_selector('#fastMenuDiv > ul > li')[2].click()
    time.sleep(2)
except:
    #print('跳过快捷菜单')
    pass

#读文件进行单号检索（可批量）
f = open('sources\RM单号.txt','r')
#逐行处理
i = 0
for line in f:
    line = line.strip('\n') #去掉结尾的回车
    i = i + 1
    #print(line)
    driver.find_element_by_css_selector('#searchUserRequirementCode').send_keys(line)
    ActionChains(driver).click(driver.find_element_by_id('searchBtn')).perform()
    print('点击【查询】')
    time.sleep(2)
    #driver.find_element_by_css_selector('td[title='+line+'] ~ td > a').click()
    ActionChains(driver).click(driver.find_element_by_css_selector('td[title='+line+'] ~ td > a')).perform()
    time.sleep(2)
    # 获取一下businessId
    url = driver.current_url
    #print(url)
    start = re.search('userRequirementId=',url).end()
    end = re.search('&topId=',url).start()
    businessId = url[start:end]
    #print('businessId:  '+businessId)
    driver.get('http://rmlogic.gmcc.net/rmlogic/docedit/userRequirementDocumentShow.action?businessId='+businessId)
    #print('进入需求书界面')
    time.sleep(5)
    ActionChains(driver).click(driver.find_element_by_css_selector('#documentTitle ~ div > a')).perform()
    print(f'{line} 下载成功')
    log.write(rq + " : "+line+"下载成功\n")
    time.sleep(5)
    driver.get('http://rmlogic.gmcc.net/rmlogic/reqview/reqViewList.action')
    time.sleep(2)
print("共{0}个文件下载完成".format(i.__str__()))
log.write(rq+" : 共{0}个文件下载完成".format(i.__str__())+"\n")
log.write("-----------------------------\n")
f.close()
log.close()
driver.close()

#http://rmlogic.gmcc.net/rmlogic/docedit/userRequirementDocumentShow.action?businessId=40288cd162896d540162a44a3dc32bc8
#var url = "/rmlogic/exportword/exportDocument.action?businessId=" + businessId + "&documentType=" + documentType + "&documentId="+documentId;