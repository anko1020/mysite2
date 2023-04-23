from openpyxl import Workbook, load_workbook
from .models import Account
from django.utils import timezone
from mysite2.settings import BASE_DIR
import os

wageTime_dir = 'excel_sheets/wageTime_sheets 2023'
dailyReport_sheet = 'C:/Users/anko1/Documents/web_django/QB Daily Report.xlsx'
salesReport_sheet = 'C:/Users/anko1/Documents/web_django/Sales Report QB 2023.xlsx'

def WriteAttendance(account):

    now = timezone.localtime(timezone.now())
    username = account.user.username
    excel_name = 'time sheet '+str(now.month)+'.xlsx'
    sheet_path = BASE_DIR/wageTime_dir/excel_name
    wb = load_workbook(sheet_path)
    ws = wb[username]

    t_start = timezone.localtime(account.start_time)
    t_end = timezone.localtime(account.end_time)
    print(t_start)

    ws.cell(row=t_start.day+2, column=5, value=t_end.strftime("%H:%M"))
    ws.cell(row=t_start.day+2, column=4, value=t_start.strftime("%H:%M"))

    wb.save(sheet_path)
    wb.close()

def test():
    now = timezone.localtime(timezone.now())
    sheet_path = BASE_DIR/wageTime_dir/'/time sheet 4.xlsx'
    wb = load_workbook(sheet_path)
    ws = wb["ss"]

    t_start = now.strftime("%H:%M")
    print(t_start)
    t_end = "15:10"

    ws.cell(row=20+2, column=5, value=t_end)
    ws.cell(row=20+2, column=4, value=t_start)

    wb.save(sheet_path)
    wb.close()



def AddSheet(user): 
    #xw.App(visible=False)
    excel_name = 'time sheet '+str(timezone.now().month)+'.xlsx'
    sheet_path = BASE_DIR/wageTime_dir/excel_name
    wb = load_workbook(sheet_path)

    try:
        ws = wb.copy_worksheet(wb["ひな形"])
        ws.freeze_panes = 'A3'
        ws.title = user
        ws["E1"] = user

        wb.save(sheet_path)
    except:
        print('Write excel error')
