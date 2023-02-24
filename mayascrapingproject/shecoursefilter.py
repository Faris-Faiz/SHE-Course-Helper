import openpyxl
from openpyxl.worksheet.worksheet import Worksheet as WS
import json
from typing import List, Dict
import sys
import os.path
from datetime import datetime

def main():
    # file_target = "course list update - 202302241814.xlsx"
    # output = 'shecourselist.xlsx'

    if len(sys.argv) < 2:
        print("USAGE: python shecoursefilter.py [filename] [?output]")
    
    if len(sys.argv) == 2:
        file_target = sys.argv[1]
        output = "shecourselist.xlsx"
    else:
        file_target = sys.argv[1]
        output = sys.argv[2]
    
    if not os.path.exists(file_target):
        return print(f"{file_target} does not exist!")

    wb: openpyxl.Workbook = openpyxl.load_workbook(filename=file_target, read_only=True)
    ws: WS = wb.active
    
    rows = ws.rows

    headers = next(rows)  # skip headers

    with open('she_courses_mod.json') as f:
        she_courses: List[Dict[str, str]] = json.load(f)
    
    wb = openpyxl.Workbook()
    ws: WS = wb.active

    headers = ('FACULTY', 'CODE', 'COURSE NAME', 'FULL', 'MEDIUM', 'REGISTERED', 'CAPICITY', 'CLUSTER')
    ws.append(headers)

    while len((subject := next(rows, tuple()))) != 0:
        code = subject[1].value
        for course in she_courses:
            if course['code'] in code:
                faculty = subject[0].value
                course_name = subject[2].value
                full = subject[7].value[0]
                medium = subject[4].value
                registered = subject[5].value
                capacity = subject[6].value
                cluster = course['cluster']

                ws.append((faculty, code, course_name, full, medium, registered, capacity, cluster))
    
    wb.save(output)

    with open('lastran.txt', 'w') as f:
        f.write(str(datetime.now()))
              

if __name__ == "__main__":
    main()
