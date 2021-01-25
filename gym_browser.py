from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_binary
import datetime

# Chrome起動

class InqueryGym:

    def __init__(self):
        self.driver = webdriver.Chrome()


    def inqueryByDate(self, inquery_date):
        # 空き施設照会
        INQUERY_URL = "https://www.net.city.nagoya.jp/cgi-bin/sp04001"
        driver = self.driver
        driver.get(INQUERY_URL)
        try:
            wait = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located)

            element1 = driver.find_element_by_name("syumoku")
            select1 = Select(element1)
            select1.select_by_visible_text("バスケットボール")

            month_str = "{:02d}".format(inquery_date.month)
            element2 = driver.find_element_by_name("month")
            select2 = Select(element2)
            select2.select_by_visible_text(month_str)

            day_str = "{:02d}".format(inquery_date.day)
            element3 = driver.find_element_by_name("day")
            select3 = Select(element3)
            select3.select_by_visible_text(day_str)

            element4 = driver.find_element_by_xpath(".//input[@type='radio' and @name='joken' and @value='2']")
            element4.click()

            element5 = driver.find_element_by_name("kyoyo1")
            select5 = Select(element5)
            select5.select_by_visible_text("全供用")

            element6 = driver.find_element_by_xpath(".//input[@type='submit' and @name='button' and @value='照会']")
            element6.click()

        except (TimeoutException, NoSuchElementException):
            ### 例外処理
            driver.quit()
            return 0

    def inqueryDate():
        date_now = datetime.datetime.now()
        weekday_now = date_now.weekday()
        weekday = ["月","火","水","木","金","土","日"]
        weekday_offset = weekday.index("土") - weekday_now
        inquery_date = []
        for i in range(0, 8):
            # 8週間後まで検索
            day_offset = weekday_offset + i * 7
            date = date_now + datetime.timedelta(days=day_offset)
            inquery_date.append(date)
        return inquery_date

    def getInqueryResult(self):
        driver = self.driver
        self.inquery_results = []
        try:
            wait = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located)

            table = driver.find_element_by_xpath(".//table[@border='1']")
            trs = table.find_elements_by_tag_name("tr")
            # ヘッダ行を除く情報の取得
            for i in range(1, len(trs)):
                tds = trs[i].find_elements_by_tag_name("td")
                area = tds[1].text
                facility = tds[2].text
                date = tds[3].text
                time = tds[4].text
                inquery_result = InqueryResult(area, facility, date, time)
                self.inquery_results.append(inquery_result)
        except (TimeoutException, NoSuchElementException):
            ### 例外処理
            driver.quit()


    def printInqueryResult(self):
        print("---照会結果-------------")
        if len(self.inquery_results) == 0:
            print("該当なし")
        else:
            for i in range(0, len(self.inquery_results)):
                ir = self.inquery_results[i]
                print(f"No.{i + 1}")
                print(f"    地域：{ir.area}")
                print(f"    施設：{ir.facility}")
                print(f"    日付：{ir.date}")
                print(f"    時間：{ir.time}")
        print("-----------------------")


class InqueryResult:
    def __init__(self, area, facility, date, time):
        self.area = area
        self.facility = facility
        self.date = date
        self.time = time
