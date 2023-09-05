import os
import time
from datetime import datetime
import logging
import sys

import openpyxl
from dotenv import load_dotenv
from openpyxl.worksheet.worksheet import Worksheet
from selenium import webdriver
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire import undetected_chromedriver as uc
from seleniumwire.utils import decode
from bs4 import BeautifulSoup


calendar_string = "body > div.sv-page-content > div > div > div > div.sv-row > div.sv-col-md-5 > div > div > div.sv-tiled-container > div > div > div:nth-child(2) > a > div > span.tiled-icon-large.sv-hidden-xs.glyphicon.lar.la-calendar"
calendar_popup = "#sits_dialog > center > div > div > div:nth-child(2) > a > h1 > i"
search_string = "#poddatasection > div.sv-panel.sv-panel-primary > div.sv-panel-footer > div > input.sv-col-xs-12.sv-col-sm-2.sv-btn.sv-btn-primary"


FACULTIES = {
    "A": {
        "name": "FACULTY OF ARTS AND SOCIAL SCIENCES",
        "code": "FSSS"
    },
    "AA": {
        'name': "FACULTY OF BUSINESS AND ECONOMICS",
        "code": "FEP"
    },
    "B": {
        'name': "FACULTY OF BUILT ENVIRONMENT",
        'code': 'FAB'
    },
    "C": {
        'name': "FACULTY OF BUSINESS AND ACCOUNTANCY",
        'code': 'FPP'
    },
    "D": {
        'name': "FACULTY OF DENTISTRY",
        'code': 'FOD'
    },
    "E": {
        'name': "FACULTY OF ECONOMICS AND ADMINISTRATION",
        'code': 'UNK1'
    },
    "F": {
        'name': "CENTRE FOR FOUNDATION STUDIES IN SCIENCE",
        'code': 'UNK2'
    },
    "G": {
        'name': "UNIVERSITY",
        'code': ('CITrA', 'PD')
    },
    "H": {
        'name': "INSTITUTE FOR ADVANCED STUDIES",
        'code': 'UNK3'
    },
    "I": {
        'name': "ACADEMY OF ISLAMIC STUDIES",
        'code': 'API'
    },
    "J": {
        'name': "ACADEMY OF MALAY STUDIES",
        'code': 'APM'
    },
    "K": {
        'name': "FACULTY OF ENGINEERING",
        'code': 'FK'
    },
    "L": {
        'name': "FACULTY OF LAW",
        'code': 'FUU'
    },
    "M": {
        'name': "FACULTY OF MEDICINE",
        'code': 'FOM'
    },
    "O": {
        'name': "FACULTY OF PHARMACY",
        'code': "PHARMACY"
    },
    "P": {
        'name': "FACULTY OF EDUCATION",
        'code': 'FEDU'
    },
    "Q": {
        'name': "ASIA EUROPE INSTITUTE",
        'code': 'UNK4'
    },
    "R": {
        'name': "FACULTY OF CREATIVE ARTS",
        'code': 'PK'
    },
    "S": {
        'name': "FACULTY OF SCIENCE",
        'code': 'FS'
    },
    "T": {
        'name': "FACULTY OF LANGUAGES AND LINGUISTICS",
        'code': 'FBL'
    },
    "U": {
        'name': "LIBRARY",
        'code': 'LIBRARY'
    },
    "V": {
        'name': "FACULTY OF SPORTS AND EXERCISE SCIENCE",
        'code': 'PSSE'
    },
    "W": {
        'name': "FACULTY OF COMPUTER SCIENCE AND INFORMATION TECHNOLOGY",
        'code': 'FSKTM'
    },
    "Z": {
        'name': "INTERNATIONAL INSTITUTE OF PUBLIC POLICY AND MANAGEMENT",
        'code': 'UNK5'
    }
}

# DALAM GROUP, YANG ADA HURUP M TU UNTUK INTERNATIONAL STUDEN
YEAR = '2022'  # 2022 maksudnya 2022/2023 so kalau YEAR = 2012 maksudnya 2012/2013
SEM  = 'S2'    # S2 maksudnya Semester 2, tengok bawah untuk ref
"""
<select id="POP_UDEF.EE0B048CE1C34074975DE4D9D363418B.POP.MENSYS.2-1" name="POP_UDEF.POP.MENSYS.2-1"
    class="sv-mandatory" data-altid="chosen" style="display: none;">
    <option value="A1">SEMESTER 1 - SPECIAL PROGRAMME ARABIC LANGUAGE</option>
    <option value="A2">SEMESTER 2 - SPECIAL PROGRAMME ARABIC LANGUAGE</option>
    <option value="C1">SEMESTER 1 - RESEARCH (PUBLIC HEALTH)</option>
    <option value="C2">SEMESTER 2 - RESEARCH (PUBLIC HEALTH)</option>
    <option value="CS">SPECIAL SEMESTER - RESEARCH (PUBLIC HEALTH)</option>
    <option value="D1">SEMESTER 1 - DIPLOMA KSK</option>
    <option value="D2">SEMESTER 2 - DIPLOMA KSK</option>
    <option value="E1">SEMESTER 1 - AEI</option>
    <option value="E2">SEMESTER 2 - AEI</option>
    <option value="ES">SPECIAL SEMESTER - AEI</option>
    <option value="F1">SEMESTER 1 - FOUNDATION</option>
    <option value="F2">SEMESTER 2 - FOUNDATION</option>
    <option value="J1">SEMESTER 1 - SPECIAL PREPARATORY PROGRAM (JAPAN)</option>
    <option value="J2">SEMESTER 2 - SPECIAL PREPARATORY PROGRAM (JAPAN)</option>
    <option value="J3">SEMESTER 3 - SPECIAL PREPARATORY PROGRAM (JAPAN)</option>
    <option value="J4">SEMESTER 4 - SPECIAL PREPARATORY PROGRAM (JAPAN)</option>
    <option value="L1">SEMESTER 1 - ADVANCED DIPLOMA KSK</option>
    <option value="L2">SEMESTER 2 - ADVANCED DIPLOMA KSK</option>
    <option value="L3">SEMESTER 3 - ADVANCED DIPLOMA KSK</option>
    <option value="R1">SEMESTER 1 - RESEARCH PROGRAM</option>
    <option value="R2">SEMESTER 2 - RESEARCH PROGRAM</option>
    <option value="S1">SEMESTER 1</option>
    <option value="S2">SEMESTER 2</option>
    <option value="SS">SPECIAL SEMESTER</option>
    <option value="T1">TERM 1</option>
    <option value="T2">TERM 2</option>
    <option value="TM">TERM</option>
</select>
"""


def str_fil(x: str):
    if x.strip() == "":
        return False
    return True


def mentor_map(x: str):
    return x.strip()


def main():
    load_dotenv()

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    driver = uc.Chrome(options=options)
    waiter = WebDriverWait(driver, 180)

    driver.get('https://maya.um.edu.my/sitsvision/wrd/siw_lgn')
    time.sleep(5)

    userInput = driver.find_element(by.CSS_SELECTOR, '[name="MUA_CODE.DUMMY.MENSYS.1"]')
    userInput.clear()

    userInput.send_keys(os.environ.get('user'))
    passInput = driver.find_element(by.CSS_SELECTOR, '[name="PASSWORD.DUMMY.MENSYS.1"]')

    passInput.clear()
    passInput.send_keys(os.environ.get('pass') + '\n')

    time_format = "%Y%m%d%H%M"
    now = datetime.now().strftime(time_format)

    wb = openpyxl.Workbook()
    ws: Worksheet = wb.active
    ws.title = now

    headers = ('FACULTY', 'CODE','COURSE NAME', 'OCCURRENCE','MEDIUM', 'REGISTERED', 'CAPACITY', 'FULL', 'WEEK', 'DAY', 'MENTOR', 'ROOM')

    ws.append(headers)
    if len(sys.argv) > 1:
        file_title = sys.argv[1]
    else:
        file_title = f'course list update - {now}.xlsx'
    wb.save(filename=file_title)

    for faculty_code in FACULTIES.keys():
        waiter.until(ec.presence_of_element_located((by.CSS_SELECTOR, calendar_string)))
        driver.execute_script('timetable_popup();')
        waiter.until(ec.presence_of_element_located((by.CSS_SELECTOR, calendar_popup))).click()
        
        driver.execute_script(
            f"document.querySelector('[name=\"POP_UDEF.POP.MENSYS.1-1\"]').value = '{YEAR}';")
        
        driver.execute_script(
            f"document.querySelector('[name=\"POP_UDEF.POP.MENSYS.2-1\"]').value = '{SEM}';")
        
        driver.execute_script(
            f"document.querySelector('[name=\"POP_UDEF.POP.MENSYS.3-1\"]').value = '{faculty_code}';")  # TODO: make for every faculty... need to complete the saving one
        
        del driver.requests

        current_url = driver.current_url

        driver.find_element(by.CSS_SELECTOR, search_string).click()

        waiter.until(ec.url_changes(current_url))

        sauce = driver.wait_for_request('/sitsvision/wrd/SIW_POD')

        html_doc = decode(sauce.response.body, sauce.response.headers.get('Content-Encoding', 'identity')).decode()

        soup = BeautifulSoup(html_doc, 'html.parser')

        try:
            subject_rows = soup.find_all('table')[1].find('tbody').find_all('tr')
        except Exception as e:
            logging.exception('bruh ' + FACULTIES[faculty_code]['name'])
            driver.find_element(by.CSS_SELECTOR, '#STUHM00').click()
            continue
        
        for subject in subject_rows:
            # module_name, occurance/group_class, activity, week, day, module tutor, room, target, actual, pro forma
            faculty = FACULTIES[faculty_code]['code'] if not isinstance(FACULTIES[faculty_code]['code'], tuple) and not FACULTIES[faculty_code]['code'].startswith('UNK') else FACULTIES[faculty_code]['name']

            # try to split
            module_name: str = subject.find_all('td')[0].text.strip()

            splitted = module_name.split('-')
            if len(splitted) < 2:
                code = ''
                course_name = module_name
            else:
                code = splitted[0].strip()
                course_name = ('-'.join(splitted[1:])).strip()


            occurrence: str = subject.find_all('td')[1].text.strip() 
            medium: str = subject.find_all('td')[2].text.strip() 
            registered: str = subject.find_all('td')[8].text.strip() 
            capacity: str = subject.find_all('td')[7].text.strip()
            try:
                full = str(int(registered) >= int(capacity)).upper()
            except:
                full = 'N/A'
            
            week: str = subject.find_all('td')[3].text.strip()
            
            try:
                day = subject.find_all('td')[4].text.strip()
                day = day.replace('\n', ' ')
                day = day.replace('\t', ' ')
                day = day.replace('\r', '')
                day = ' '.join(day.split(' '))
            except:
                day: str = subject.find_all('td')[4].text.strip()
            
            try:
                mentor_list: list = subject.find_all('td')[5].text.strip().split('\n')
                mentor = ', '.join(map(mentor_map, filter(str_fil, mentor_list)))  # 🥷
            except:
                mentor = subject.find_all('td')[5].text.strip()
            
            room: str = subject.find_all('td')[6].text.strip()

            ws.append((faculty, code, course_name, occurrence, medium, registered, capacity, full, week, day, mentor, room))
        else:
            wb.save(filename=file_title)
        driver.find_element(by.CSS_SELECTOR, '#STUHM00').click()


if __name__ == "__main__":
    main()
