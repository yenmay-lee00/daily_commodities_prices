"""
Author: yenmay
"""
from helpers import *
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
from selenium import webdriver
from datetime import date, datetime, timedelta
import sqlite3
import pandas as pd
import requests
import numpy as np
import os
import xlrd

main_folder_path = "change/to/your/path" # change to your path

class Commodity:
    def __init__(self):
        pass
        
    def get_soup(self, url, header_general={'User-Agent': 'insert your header'}): # insert your header
        response = requests.get(url, headers=header_general, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

class Rubber(Commodity):
    def __init__(self, date_obj):
        self.date_obj = date_obj

    @classmethod
    def get_json(cls, url):
        response = requests.get(url, verify=False)
        data = response.json()
        return data

    def get_price(self):
        url = "https://www.lgm.gov.my/webv2api/api/rubberprice/currentprice"

        if self.date_obj:
            data = Rubber.get_json(url)
            for dict_obj in data:
                if parse_date(dict_obj['tarikh'], "%Y-%m-%dT%H:%M:%S") == self.date_obj and dict_obj['grade'] == 'SMR 20' and dict_obj['masa'] == 'Noon':
                    val = dict_obj['sellers']
                    return val
        return None  

class PalmOil(Commodity):
    def __init__(self, date_obj):
        self.date_obj = date_obj

    @classmethod
    def get_dynamic_soup(cls, url):
        driver = webdriver.Edge()
        driver.get(url)
        html_content = driver.page_source
        driver.quit()
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup

    def get_price(self):    
        url = "https://bepi.mpob.gov.my/admin2/chart_cpomsia_mini.php"

        if self.date_obj:
            soup = PalmOil.get_dynamic_soup(url)   
            date_element = soup.find('font', {'size': '2'})
            date_text = date_element.get_text() if date_element else None
            formatted_date = parse_date(date_text.split(': ')[1], "%d %B %Y") if date_text else None

            price_element = soup.find('font', {'size': '3'})
            price_text = price_element.get_text() if price_element else None
            formatted_price = float(price_text.split()[-1].replace(',', '')) if price_text else None

            if formatted_date == self.date_obj:
                return formatted_price
        return None 

class Mdex(Commodity):
    base_url = "https://www.bursamalaysia.com"
    url = "https://www.bursamalaysia.com/market_information/market_statistic/derivatives"

    def __init__(self, date_obj):
        self.date_obj = date_obj
    
    @classmethod
    def download_file(cls, base_url, url, filename):
        with open(filename, 'wb') as f:
            response = requests.get(f'{base_url}{url}')
            f.write(response.content)

    @classmethod
    def find_header_row_index(cls, sheet, header_text, instance=1):
        count = 0
        for row_index in range(sheet.nrows):
            if sheet.cell_value(row_index, 2) == header_text:  # Assuming header is in column C   
                if count == instance:
                    return row_index
                count += 1
        return None
    
    @classmethod
    def delete_file(cls, file_path):
        try:
            os.remove(file_path)
        except OSError as e:
            print(f"Error: {file_path} - {e.strerror}")

    @classmethod
    def extract_vals(cls, publication_file, date_to_record):
        workbook = xlrd.open_workbook(publication_file)
        sheet = workbook.sheet_by_name("TS_All Prods ")
        header_row_index = cls.find_header_row_index(sheet, "CRUDE PALM OIL FUTURES (FCPO)")
        date_to_record_future = date_to_record + relativedelta(months=2) # future1

        for row_index in range(header_row_index + 1, sheet.nrows):
            cell_date_future_str = sheet.cell_value(row_index, 2)
            cell_date_future_obj = parse_date(cell_date_future_str, "%B,%Y", "%b,%Y")
            if date_to_record_future.day < 16 and cell_date_future_obj.year == date_to_record_future.year and cell_date_future_obj.month == date_to_record_future.month:
                current_val = sheet.cell_value(row_index - 2, 9)  # current1
                future_val = sheet.cell_value(row_index, 9)  # future1
                break
            elif date_to_record_future.day >= 16 and cell_date_future_obj.year == date_to_record_future.year and cell_date_future_obj.month == date_to_record_future.month:
                current_val = sheet.cell_value(row_index - 1, 9)  # current2
                future_val = sheet.cell_value(row_index + 1, 9)  # future2
                break
        
        if current_val and future_val:            
            return current_val, future_val
        else:
            return None, None
        
    def get_price(self):
        if self.date_obj:
            global main_folder_path
            soup = super().get_soup(Mdex.url)
            daily_table = soup.find_all('table', class_='bm_table plain-table g-mb-30')[0].find_all('span', class_='bm_download_xls')
            day_keys = [parse_date(day.a['title'][:-4], '%Y-%m-%d') for day in daily_table if day.a]
            day_vals = [day.a['href'] for day in daily_table if day.a]
            
            for key, val in zip(day_keys, day_vals):
                if key == self.date_obj:
                    filename = os.path.join(main_folder_path, f"{format_date(self.date_obj, '%Y-%m-%d')}.xls")
                    print(filename)
                    Mdex.download_file(self.base_url, val, filename)

            current_val, future_val = Mdex.extract_vals(filename, self.date_obj)
            Mdex.delete_file(filename)
            return current_val, future_val
        return None, None

class Cocoa(Commodity):
    def __init__(self, date_obj):
        self.date_obj = date_obj

    def get_price(self):
        url = f"https://sso.koko.gov.my/api/carian_HHarian?tarikh={format_date(self.date_obj, '%Y-%m-%d')}&bahasa=English&wpgetapi=[%22api_koko%22,%22carian_harian%22,%22none%22,0]"

        if self.date_obj:
            smc2_avrg_center_list = []
            soup = super().get_soup(url)
            soup = soup.find('tbody').find_all('tr')
            for row in soup:
                td_elements = row.find_all('td')
                smc2_avrg_center = float(td_elements[9].get_text(strip=True).replace(',', '')) # SMC2 Average is the 10th element in each row
                smc2_avrg_center_list.append(smc2_avrg_center)

            if smc2_avrg_center_list:
                average = np.mean(smc2_avrg_center_list)
                return average
            else:
                return None
        return None       

class OPEC(Commodity):
    def __init__(self, date_obj):
        self.date_obj = date_obj

    def get_price(self):
        url = "https://www.opec.org/basket/basketDayArchives.xml"

        if self.date_obj:
            soup = super().get_soup(url)
            basketlist = soup.find('basketlist', data = format_date(self.date_obj, '%Y-%m-%d'))
            if basketlist:
                val = basketlist['val']
                return val
            else:
                return None
        return None
