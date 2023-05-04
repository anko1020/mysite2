from openpyxl import Workbook, load_workbook
from .models import Account
from django.utils import timezone
import xlwings as xw
from mysite2.settings import BASE_DIR
from datetime import datetime, timedelta, date
import calendar
import os

wageTime_dir = BASE_DIR/'excel_sheets/wageTime_sheets 2023'
dailyReport_sheet = BASE_DIR/'excel_sheets/QB Daily Report.xlsx'
salesReport_sheet = 'C:/Users/anko1/Documents/web_django/Sales Report QB 2023.xlsx'
staff_sheet = BASE_DIR/'excel_sheets/staff.xlsx'

def WriteAttendance(account):

    now = timezone.localtime(timezone.now())
    username = account.user.username
    excel_name = '出退勤表　'+str(TodayBehind12().month)+'月.xlsx'
    sheet_path = wageTime_dir/excel_name

    wb = load_workbook(sheet_path)

    maching_flg = False
    for title in wb.sheetnames:
        if title == username:
            maching_flg = True
            break

    if maching_flg:
        ws = wb[username]
    else:
        ws = wb.copy_worksheet(wb["ひな形"])
        ws.freeze_panes = 'A3'
        ws.title = username
        ws["E1"] = username
        wb.save(sheet_path)

    t_start = account.start_time

    account.start_overtime = str(TodayBehind12().month)+"/"+str(TodayBehind12().day)+" "
    
    is_over = 0
    if t_start.hour < 12:
        is_over = 24

    if(t_start.minute >= 1 and t_start.minute <= 30):
        account.start_overtime += str(t_start.hour+is_over)+":30"
        #t_start = t_start.replace(minute=30)
    elif(t_start.minute >= 31 and t_start.minute <= 59):
        account.start_overtime += str(t_start.hour+is_over+1)+":00"
        #t_start = t_start.replace(hour=t_start.hour+1, minute=00) 
        #pd_time = pd.DataFrame({'time':[t_start,t_end]})
    elif(t_start.minute == 00):
        account.start_overtime += str(t_start.hour+is_over)+":00"

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
    excel_name = '出退勤表　'+str(now.month)+'月.xlsx'
    sheet_path = wageTime_dir/excel_name
    wb = load_workbook(sheet_path)
    try:
        ws = wb[username]
    except Exception as e:
        print("error:")
        print(e)
        return

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
        for title in wb.sheetnames:
            if title == username:
                maching_flg = True
                break

        if maching_flg:
            ws = wb[username]
        else:
            ws = wb.copy_worksheet(wb["ひな形"])
            ws.freeze_panes = 'A3'
            ws.title = username
            ws["E1"] = username
            wb.save(sheet_path)

        ws_daily['O'+str(12+user_number)] = account.end_overtime.split()[1]
        ws_daily['N'+str(12+user_number)] = account.start_overtime.split()[1]
        wb_daily.save(dailyReport_sheet)
        wb_daily.close()

def ChangeSheetName(prev_name, name):
    now = timezone.localtime(timezone.now())
    excel_name = '出退勤表　'+str(now.month)+'月.xlsx'
    sheet_path = wageTime_dir/excel_name
    wb = load_workbook(sheet_path)
    ws = wb[prev_name]
    ws.title = name
    wb.save(sheet_path)
    wb.close()


def test(month):
    now = timezone.localtime(timezone.now())

    origin_excel = 'template.xlsx'
    origin_path = wageTime_dir/origin_excel
    origin_wb = xw.Book(origin_path)

    excel_name = '出退勤表　'+str(month)+'月.xlsx'
    sheet_path = wageTime_dir/excel_name
    wb = xw.Book(sheet_path)
    
    origin_wb.sheets["ひな形"].copy(after=wb.sheets[0])

    wb.sheets["Sheet1"].delete()

    origin_wb.save()
    weekDay = ["月","火","水","木","金","土","日"]
    print(calendar.monthrange(2023, month)[1])
    for i in range(calendar.monthrange(2023, month)[1]):
        dates = str(month)+"月"+str(i+1)+"日"
        weekd = weekDay[(date(2023, month, i+1).weekday())]
        wb.sheets["ひな形"].range(3+i,2).value = dates
        wb.sheets["ひな形"].range(3+i,3).value = weekd
        print(dates+weekd)

    app = xw.apps.active

    wb.save()
    origin_wb.close()
    wb.close()

    app.kill()

def makenew(month):

    excel_name = '出退勤表　'+str(month)+'月.xlsx'
    sheet_path = wageTime_dir/excel_name
    wb = xw.Book()

    wb.save(sheet_path)
    app = xw.apps.active
    wb.close()

    app.kill()

def TodayBehind12():
    now = timezone.localtime(timezone.now())
    delta = timedelta(days=1)
    if now.hour < 12:
        now -= delta
    print(now.day)
    return now

def AddSheet(user):
    #xw.App(visible=False)
    excel_name = '出退勤表　'+str(timezone.now().month)+'月.xlsx'
    sheet_path = wageTime_dir/excel_name
    wb = load_workbook(sheet_path)
    
    wb_daily = load_workbook(dailyReport_sheet)
    ws_daily = wb_daily["Revised"]

    count = Account.objects.all().count()-1

    print(count)
    try:
        ws = wb.copy_worksheet(wb["ひな形"])
        ws.freeze_panes = 'D3'
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

# def ExcelToPDF():
#     excel_name = '出退勤表　'+str(timezone.now().month)+'月.xlsx'
#     sheet_path = wageTime_dir/excel_name
    
#     workbook = load_workbook(sheet_path)
#     worksheet = workbook["tt"]

#     # PDFファイルを作成
#     pdf = FPDF()
#     pdf.add_page()

#     pdf.add_font('IPAGothic', '', '/path/to/IPAGothic.ttf', uni=True)
#     pdf.set_font('IPAGothic', '', 14)


#     # Excelファイルの各セルから値を取得してPDFに書き込む
#     for row in worksheet.iter_rows():
#         for cell in row:
#             pdf.cell(40, 10, str(cell.value))

#     # PDFファイルを保存
#     pdf.output(wageTime_dir/"example1.pdf")
#     #pdf.from_file('test.html', 'pdf1.pdf')
    