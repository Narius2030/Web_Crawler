from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd

driver = webdriver.Chrome()
df = pd.DataFrame(columns=['Loại', 'Quý 2-2022', 'Quý 3-2022', 'Quý 4-2022', 'Quý 1-2023'])

driver.get("https://s.cafef.vn/bao-cao-tai-chinh/bid/incsta/2023/1/0/0/ket-qua-hoat-dong-kinh-doanh-.chn")
table = driver.find_element(By.XPATH, "/html/body/form/div[3]/div[2]/div[1]/div/div/div/div[2]/div[2]/div[9]/div[2]/table")
row_groups = table.find_elements(By.CSS_SELECTOR, "tr.r_item, tr.r_item_a")
for row_group in row_groups:
    rows = row_group.find_elements(By.CSS_SELECTOR, "td")
    data = [row.text for row in rows if rows.index(row) < 5]
    df.loc[len(df)] = data


driver.get("https://s.cafef.vn/bao-cao-tai-chinh/bid/incsta/2023/2/-1/0/ket-qua-hoat-dong-kinh-doanh-.chn")
table = driver.find_element(By.XPATH, "/html/body/form/div[3]/div[2]/div[1]/div/div/div/div[2]/div[2]/div[9]/div[2]/table")
row_groups = table.find_elements(By.CSS_SELECTOR, "tr.r_item, tr.r_item_a")
data = []
for row_group in row_groups:
    rows = row_group.find_elements(By.CSS_SELECTOR, "td")
    data.append(rows[4].text)
df['Quý 2-2023'] = data

print(df.head(5))

df.to_csv('kqkd_bidv.csv')
    