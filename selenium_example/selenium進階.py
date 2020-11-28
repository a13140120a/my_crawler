from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement


opts = webdriver.ChromeOptions()

#新增無頭覽測器、ip代理等參數
#opts.add_argument("--headless")
#opts.add_argument("--proxy-server=https://149.28.235.174:8080")


driver = Chrome('./chromedriver',options=opts)

url = 'https://www.tripadvisor.com.tw/Attraction_Review-g293913-d10020558-Reviews-or15-Fulong_International_Sand_Sculpture_Festival-Taipei.html#REVIEWS'
driver.get(url)

#等待並搜尋按鈕
start_search_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, '_2cMt8_9M')))#CLASS_NAME要大寫
start_search_btn.click()


#直接點擊按鈕
#driver.find_element_by_class_name('_2cMt8_9M').click()

htmltext = driver.page_source

a = driver.find_element_by_xpath('//*[@id="component_22"]/div/div/div[4]/div/div[1]/div[2]/span').text

#driver.close()
print(a)

#start_search_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, '_2cMt8_9M')))#CLASS要大寫
#start_search_btn.click()

##--------------------以下為EC用法---------------------------------------------------

# title_is  #title_is判断网页title是否与预期完全一致
#WebDriverWait(driver, 5, 0.5).until(EC.title_is('百度一下，你就知道'))
##-------------------------------------------------------------------
# title_contains  #title_contains判断网页title是否部分包含
#WebDriverWait(driver, 5, 0.5).until(EC.title_contains('百度一下，你就知道'))

# presence_of_element_located  #判断某个元素是否存在，并不代表该元素一定可见

# visibility_of_element_located

# url_contains   #判断网页url是否部分包含

# url_to_be      #判断网页url是否完全与期待一致

# url_changes    #判断网页url是否与期待不一致

# visibility_of

# presence_of_all_elements_located  #判断至少1个对象存在网页中，返回对象列表。

# text_to_be_present_in_element

# text_to_be_present_in_element_value

# frame_to_be_available_and_switch_to_it

# invisibility_of_element_located

# element_to_be_clickable

# staleness_of

# element_to_be_selected

# element_located_to_be_selected

# element_selection_state_to_be

# element_located_selection_state_to_be

# alert_is_present

#----------------滑鼠滾動-------------------------------------------
#下滾到底
#driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

# #將滾動條拖到最頂部
# js="var action=document.documentElement.scrollTop=0"
# driver.execute_script(js)


