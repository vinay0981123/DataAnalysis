import selenium
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd

# Creating Chrome Webdriver Instance
chrome_options = Options()
chrome_options.add_argument("--headless")

# Initialising WebDriver with Chrome options
driver = webdriver.Chrome(options=chrome_options)

# Navigating to the URL
driver.get("http://www.sunsirs.com/futures-price-2023-0927-daily.html")
table = driver.find_element(By.XPATH, '//span[@id="date"]//parent::div//following-sibling::div/table/tbody')

# Getting all the rows in table_rows
table_rows = table.find_elements(By.TAG_NAME, "tr")
# Extract the data from the table
table_data = []
for indexrow in range(len(table_rows)): #Iterating for rows
    table_row = []
    table_col = driver.find_elements(By.XPATH,f"//tbody/tr[{indexrow+1}]/td") #getting all column elements
    for index in range(len(table_col)): #iterating for column
        element=driver.find_element(By.XPATH,f"//tbody/tr[{indexrow+1}]/td[{index+1}]") #getting each data from current row 
        textdata = element.get_attribute("textContent") #invoking text from element
        textdata=textdata.strip()   #removing extra space and new line
        table_row.append(textdata) #storing all column data in a single array of the current row
            
    table_data.append(table_row)

df = pd.DataFrame(table_data[1:], columns=table_data[0])
#storing data in excel file
df.to_excel('RawData.xlsx',index=False)
df["Sectors"] = df["Sectors "] + df["09-27"]
print(f"dataframe is {df}")

# Counting total number of rows in the DataFrame
total_rows = df.shape[0]
print(f"total number of data rows is::{total_rows}")
# Converting the "09-28" column to a numeric data type
df["09-28"] = df["09-28"].str.replace(",", "").astype(float)

# Finding row with the highest closing price in the "09-28" column
max_closing_row = df[df["09-28"] == df["09-28"].max()]

# Extracting commodity name from the highest closed price row
commodity_with_highest_price = max_closing_row.iloc[0]["Commodity"]
#Handling if name is not there
if(commodity_with_highest_price):
    print(f"Commidity name is:{commodity_with_highest_price}")
else:
    print('Commodity name not found')
# Extracting highest closing price
highestClosingPrice = max_closing_row.iloc[0]["09-28"]
ChangePercentage = max_closing_row.iloc[0]["Change"]
print(f"Highest closing price is {highestClosingPrice} with the change of {ChangePercentage}")

driver.quit()


# class TestAssertions(unittest.TestCase):
    
#     def test_assertIs(self):
#         self.assertIs("Selenium Python", "Sthon", "Comparison Done")

# assertIs ("Selenium Python", "Selenium Python", "Comparison Done")
# assertIsNot ("Selenium Python", "Selenium", "Comparison Done")
# assertListEqual ([5,6], [1,3], message) if the list equal
# assertTupleEqual ((4,5), (4,5), message)
# assertSetEqual ( s1, s2, message)
# assertDictEqual ({1:4, 2:5},  {2:5, 3:6}, message)
# assertAlmostEqual (0.2,0.3)
# assertGreater ( 3, 2, "Comparison Done") should pass
# assertLess ( 3, 2, "Comparison Done") should fail
# assertRegexpMatches ("Selenium Python", "Selenium", "Search Done") if the text contains

