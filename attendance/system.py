from openpyxl import Workbook, load_workbook
from .models import Account
from django.utils import timezone
from mysite2.settings import BASE_DIR
from datetime import datetime, timedelta
import os

wageTime_dir = BASE_DIR/'excel_sheets/wageTime_sheets 2023'
dailyReport_sheet = BASE_DIR/'excel_sheets/QB Daily Report.xlsx'
salesReport_sheet = 'C:/Users/anko1/Documents/web_django/Sales Report QB 2023.xlsx'
staff_sheet = BASE_DIR/'excel_sheets/staff.xlsx'

def WriteAttendance(account):

    now = timezone.localtime(timezone.now())
    username = account.user.username
    excel_name = 'time sheet '+str(now.month)+'.xlsx'
    sheet_path = wageTime_dir/excel_name
    wb = load_workbook(sheet_path)
    ws = wb[username]

    t_start = account.start_time

    account.start_overtime = str(t_start.month)+"/"+str(t_start.day)+" "
    if(t_start.minute >= 1 and t_start.minute <= 30):
        account.start_overtime += str(t_start.hour)+":30"
        #t_start = t_start.replace(minute=30)
    elif(t_start.minute >= 31 and t_start.minute <= 59):
        account.start_overtime += str(t_start.hour+1)+":00"
        #t_start = t_start.replace(hour=t_start.hour+1, minute=00) 
        #pd_time = pd.DataFrame({'time':[t_start,t_end]})
    elif(t_start.minute == 00):
        account.start_overtime += str(t_start.hour)+":00"

    ws.cell(row=t_start.day+2, column=4, value=account.start_overtime.split()[1])

    print("attendance_sheet_print:")
    print(account.start_overtime)
    # start_str = t_start.strftime("%H:%M")
    # end_str = ""

    # if(t_start.day == t_end.day):
    #     end_str = t_end.strftime("%H:%M")
    # else:
    #     end_str = str(t_end.hour+24)+":"+
    
    account.save()
    wb.save(sheet_path)
    wb.close()

def WriteLeaving(account):

    now = timezone.localtime(timezone.now())
    username = account.user.username
    excel_name = 'time sheet '+str(now.month)+'.xlsx'
    sheet_path = wageTime_dir/excel_name
    wb = load_workbook(sheet_path)
    ws = wb[username]

    user_number = 0
    for sheet in wb.sheetnames:
        if(sheet == username):
            break
        user_number = user_number+1

    print(user_number)

    t_start = account.start_time
    t_end = account.end_time

    account.end_overtime = str(t_end.month)+"/"+str(t_start.day)+" "
    hour = t_end.hour
    minute = 0
    if(t_start.day != t_end.day):
        hour = hour+24
    if(t_end.minute >= 16 and t_end.minute <= 45):
        minute = 30
    elif(t_end.minute >= 46):
        hour = hour+1
    if(hour < 10):
        account.end_overtime += "0"
    account.end_overtime += str(hour)+":"+str(minute)
    if(minute == 0):
        account.end_overtime += "0"
    if(int(((t_end-t_start).total_seconds())/60) < 30):
        account.end_overtime = account.start_overtime
    ws.cell(row=t_start.day+2, column=5, value=account.end_overtime.split()[1])
    
    print("leaving_sheet_print:")
    print(account.end_overtime)
    # start_str = t_start.strftime("%H:%M")
    # end_str = ""

    # if(t_start.day == t_end.day):
    #     end_str = t_end.strftime("%H:%M")
    # else:
    #     end_str = str(t_end.hour+24)+":"+
    
    account.save()
    wb.save(sheet_path)
    wb.close()

    if(user_number < Account.objects.all().count()):
        wb_daily = load_workbook(dailyReport_sheet)
        ws_daily = wb_daily["Revised"]
        ws_daily['O'+str(12+user_number)] = account.end_overtime.split()[1]
        ws_daily['N'+str(12+user_number)] = account.start_overtime.split()[1]
        wb_daily.save(dailyReport_sheet)
        wb_daily.close()

def ChangeSheetName(prev_name, name):
    now = timezone.localtime(timezone.now())
    excel_name = 'time sheet '+str(now.month)+'.xlsx'
    sheet_path = wageTime_dir/excel_name
    wb = load_workbook(sheet_path)
    ws = wb[prev_name]
    ws.title = name
    wb.save(sheet_path)
    wb.close()


def test():
    now = timezone.localtime(timezone.now())
    sheet_path = wageTime_dir/'/time sheet 4.xlsx'
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
    sheet_path = wageTime_dir/excel_name
    wb = load_workbook(sheet_path)
    
    wb_daily = load_workbook(dailyReport_sheet)
    ws_daily = wb_daily["Revised"]

    count = Account.objects.all().count()-1

    print(count)
    try:
        ws = wb.copy_worksheet(wb["ひな形"])
        ws.freeze_panes = 'A3'
        ws.title = user
        ws["E1"] = user
        wb.save(sheet_path)

        ws_daily["M"+str(count+12)] = user
        wb_daily.save(dailyReport_sheet)
    except:
        print('Write excel error')
        
def ConvertOvertimeToDatetime(overdatetime):
    now = timezone.localtime(timezone.now())

    date = overdatetime.split()[0]
    time = overdatetime.split()[1]
    hour = int(time.split(':')[0])
    minute = int(time.split(':')[1])

    convertedDateTime = datetime.strptime(str(now.year)+"/"+date, '%Y/%m/%d')
    if(hour/24 > 0 and hour > 24):
        convertedDateTime = convertedDateTime + timedelta(days=int(hour/24))
        hour %= 24
        
    convertedDateTime = convertedDateTime.replace(hour=hour, minute=minute)

    print("converted:")
    print(convertedDateTime)
    return convertedDateTime
