from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from .models import PelosiTrade, NancyPelosi

def RunPelosiScraper():
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    driver.get("https://www.quiverquant.com/congresstrading/politician/Nancy%20Pelosi-P000197")

    # Gathering Pelosi information
    net_worth = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div[1]/div[2]/div[1]/strong').text
    trade_volume = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div[1]/div[2]/div[2]/strong').text
    total_trades = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div[1]/div[2]/div[3]/strong').text
    last_traded = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div[1]/div[2]/div[4]/strong').text

   # Check if a NancyPelosi object already exists
    if NancyPelosi.objects.exists():
        # update
        pelosi = NancyPelosi.objects.first()  # there shall only be one
        pelosi.net_worth = net_worth
        pelosi.trade_volume = trade_volume
        pelosi.total_trades = total_trades
        pelosi.last_traded = last_traded
        pelosi.save()
    else:
        # create
        pelosi = NancyPelosi.objects.create(net_worth=net_worth, trade_volume=trade_volume, total_trades=total_trades, last_traded=last_traded)

    # Scroll to the trade table
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2.25);")

    # Get info from trade table
    # time.sleep(999)

    # Get table info
    table = driver.find_element(By.XPATH, "//*[@id='tradeTable']")
    rows = table.find_elements(By.XPATH, ".//tbody/tr")

    # Extract each row's data
    for row in rows:
        # Extract data from each column in the row
        columns = row.find_elements(By.XPATH, ".//td")
        if len(columns) >= 6:
            stock_symbol = columns[0].find_element(By.XPATH, ".//a/div/strong").text
            name = columns[0].find_element(By.XPATH, ".//a/div/span[1]").text
            trade_type = columns[0].find_element(By.XPATH, ".//a/div/span[2]").text
            transaction_type = columns[1].find_element(By.XPATH, ".//a/strong").text
            trade_date = columns[2].find_element(By.XPATH, ".//a/strong").text
            trade_price = columns[1].find_element(By.XPATH, ".//a/span").text
            since_transaction = columns[5].find_element(By.XPATH, ".//a/strong").text
            cover_url = columns[0].find_element(By.XPATH, './/a/img')
            src = cover_url.get_attribute("src")
            print(src)
            
            # Print or process the extracted data
            trade = PelosiTrade(stock_symbol=stock_symbol, name=name, trade_type=trade_type, transaction_type=transaction_type, trade_date=trade_date, trade_price=trade_price, since_transaction=since_transaction, photo_url=src)

            trade.save()

        else:
            print("Not enough columns in the row")

    print(len(rows))

    driver.quit()