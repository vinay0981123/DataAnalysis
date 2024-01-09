import selenium
import pandas as pd
from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
from datetime import datetime
fileExists=False
def is_valid_date(date_string):
    try:
        # Attempt to parse the date string
        datetime.strptime(date_string, '%m-%d')
        return True  # The string is a valid date in the "MM-DD" format
    except ValueError:
        return False  # The string is not a valid date
def increment_date(date_str):
    try:
        date = datetime.strptime(date_str, "%Y-%m%d")
        new_date = date + timedelta(days=1)
        return new_date.strftime("%Y-%m%d")
    except ValueError:
        return "Invalid date format"

def getUpdatedLink(file_contents):
    link=file_contents
    strtofind='futures-price-'
    index=link.find(strtofind)+len(strtofind)
    original_date=link[index:index+9]
    new_date = increment_date(original_date)
    link=link[:index]+new_date+link[index+9:]
    return link
def writeInitialLink(maxdate):
    maxdate=maxdate.replace('-',"")
    with open('linkdata.txt','r') as file:
        link=file.read()
    file.close()
    strtofind='futures-price-'
    index=link.find(strtofind)+len(strtofind)
    original_date=link[index:index+9]
    original_date=original_date[0:5]+maxdate
    new_date = increment_date(original_date)
    link=link[:index]+original_date+link[index+9:]
    with open('linkdata.txt','w') as file:
        link=file.write(link)
    file.close()

def checkMaxDateInFileIfExists():
    max_date = None
    try:
        df = pd.read_excel('RawData.xlsx')
        date_columns = df.columns[2:]
        vdate=[]
        for column in date_columns:
            if(is_valid_date(column)):
                vdate.append(column)
        data = {'Date': vdate}
        df = pd.DataFrame(data)
        df['Date'] = pd.to_datetime(df['Date'], format='%m-%d')
        max_date = df['Date'].max()
        max_date=max_date.strftime('%m-%d')
    except FileNotFoundError as e:
        print('error is',e)
    return max_date
        
if(checkMaxDateInFileIfExists()!=None):
    fileExists=True
    writeInitialLink(checkMaxDateInFileIfExists())

with open('linkdata.txt', "r") as file:
        file_contents = file.read()
        file_contents=file_contents.strip()
file.close()
driver = webdriver.Chrome()

for i in range(100):
    driver.get(file_contents)
    elements=driver.find_elements(By.XPATH,'//td[text()="no data"]')
    
    if(len(elements)==0):
        file_contents=getUpdatedLink(file_contents)
        with open('linkdata.txt', "w") as file:
            file.write(file_contents)
        file.close()
        # scrapping
        table = driver.find_element(By.XPATH, '//span[@id="date"]//parent::div//following-sibling::div/table/tbody')

        # Getting all the rows in table_rows
        table_rows = table.find_elements(By.TAG_NAME, "tr")
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
        if(checkMaxDateInFileIfExists()!=None):
            fileExists=True
            olddf=pd.read_excel('RawData.xlsx')
            df = pd.DataFrame(table_data[1:], columns=table_data[0])
            SecondLastColumnName = df.columns[-2]
            SecondLastColumnData= df[SecondLastColumnName]
            olddf[SecondLastColumnName]=df[SecondLastColumnName]
            olddf.to_excel('RawData.xlsx',index=False)
            print(olddf)
        else:
            df = pd.DataFrame(table_data[1:], columns=table_data[0])
            print(df)
            df.to_excel('RawData.xlsx',index=False)
    else:
        print("There is no data for scrapping")
        break