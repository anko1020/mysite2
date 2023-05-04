from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, ListView, FormView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils import timezone
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment
from openpyxl.styles.borders import Border, Side

import mimetypes
from mysite2.settings import BASE_DIR
from pathlib import Path
#import pythoncom
from . import system
import os
from .forms import AccountForm
from datetime import datetime, timedelta
from .models import Account

def Login(request):

    if request.method == 'POST':
        ID = request.POST.get('username')
        Pass = request.POST.get('password')

        user = authenticate(username=ID, password=Pass)
        if user:
            if user.is_superuser:
                login(request, user)
                return HttpResponseRedirect(reverse('AdminForm'))
            
            elif user.is_active:
                login(request, user)
                name = get_object_or_404(Account, user=User.objects.get(username=ID))
                return HttpResponseRedirect(reverse('Result'))
            else:
                return HttpResponse("Not Valid")
        else:
            msg = {
                "incorrect" :True,
            }
            return render(request, 'attendance/login_test.html', msg)
    else:
        return render(request, 'attendance/login_test.html')

@login_required
def Logout(request):
    return HttpResponse("")

@login_required
def Result(request):
    account = get_object_or_404(Account, user=request.user)
    account.is_working = not account.is_working
    now = timezone.localtime(timezone.now())
    if account.is_working:
        account.start_time = now
        working_time = now-now
        system.WriteAttendance(account)
    else:
        account.end_time = now
        working_time =  now - account.start_time
        system.WriteLeaving(account)
    
    account.save()
    logout(request)

    params = {
        "user"          :account.user,
        "is_working"    :account.is_working,
        "time_start"    :account.start_overtime,
        "time_end"      :account.end_overtime,
        "delta_h"       :int(working_time.total_seconds()/3600),
        "delta_m"       :int((working_time.total_seconds()%3600)/60),
    }
    return render(request, "attendance/attendance_form.html", params)

class AdminFrom(ListView):
    model = Account
    template_name = "attendance/admin_form.html"
    def get(self,request):
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse('Login'))
        return super().get(request)

class Registration(TemplateView):
    
    def __init__(self):
        self.params = {
        "AccountCreate":False,
        "account_form": AccountForm(),
        }

    def get(self,request):
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse('Login'))
        else:
            self.params["account_form"] = AccountForm()
            self.params["AccountCreate"] = False
            return render(request,"attendance/register.html",context=self.params)

    def post(self,request):
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse('Login'))
        else:
            self.params["account_form"] = AccountForm(data=request.POST)
            
            if self.params["account_form"].is_valid():
                account = self.params["account_form"].save()

                account.set_password(account.password)
                account.save()

                now = timezone.now()
                Account.objects.create(user=account,is_working=False,start_time=now,end_time=now)

                system.AddSheet(account.username)

                self.params["AccountCreate"] = True

            else:
                print(self.params["account_form"].errors)

            return render(request,"attendance/register.html" ,context=self.params)
        
def DownloadExcel(request,pk):
    now = timezone.localtime(timezone.now())

    account = get_object_or_404(Account,pk=pk)
    user = account.user.username

    path ='excel_sheets/wageTime_sheets 2023/'
    excel_name = '出退勤表　'+str(now.month)+'月.xlsx'
    excel_path = BASE_DIR/path/excel_name
    temp_path = BASE_DIR/path/"download_temp.xlsx"

    wb = load_workbook(excel_path)
    ws = wb[user]

    temp_book = load_workbook(temp_path)
    temp_sheet = temp_book.worksheets[0]
    temp_sheet.title = user
    temp_sheet.freeze_panes = 'D3'
    
    for column in ws.columns:
        temp_sheet.column_dimensions[column[0].column_letter].width = ws.column_dimensions[column[0].column_letter].width
        for cell in column:
            print(cell.column)
            print(cell.number_format)
            temp_cell = temp_sheet.cell(row=cell.row, column=cell.column)
            #temp_sheet[cell.coordinate].border = ws[cell.coordinate].border
            temp_cell.value = cell.value
            _top = Side(style=cell.border.top.style)
            _bottom = Side(style=cell.border.bottom.style)
            _right = Side(style=cell.border.right.style)
            _left = Side(style=cell.border.left.style)
            temp_cell.border = Border(top=_top, bottom=_bottom, right=_right, left=_left)
            temp_cell.alignment = Alignment(horizontal=ws[cell.coordinate].alignment.horizontal)
            
            if temp_cell.column == 2:
                temp_cell.number_format = 'm"月"d"日"'
            else:
                temp_cell.number_format = cell.number_format 
    
    temp_book.save(temp_path)

    #response = HttpResponse(open(path_excel, 'rb').read(), content_type='application/vnd.ms-excel')
    pdf_name = "Time Sheet:"+user+".xlsx"
    print(pdf_name)
    response = HttpResponse(open(temp_path, 'rb').read(), content_type=mimetypes.guess_type(pdf_name)[0])
    
    response['Content-Disposition'] = f'attachment; filename={pdf_name}'
    return response

def AccountEditer(request, pk):
    if request.method == 'POST':
        account = get_object_or_404(Account,pk=pk)
        prev_name = account.user.username
        user = User.objects.get(username=prev_name)

        account.user.username = request.POST.get('username')
        user.username = request.POST.get('username')
        password = request.POST.get('password')
        if request.POST.get('start_t') != None:
            account.start_time = system.ConvertOvertimeToDatetime(request.POST.get('start_t'))
        if request.POST.get('end_t') != None:
            account.end_time = system.ConvertOvertimeToDatetime(request.POST.get('end_t'))
        account.is_sending = request.POST.get('is_send') == "on"
        
        if prev_name != account.user.username:
            system.ChangeSheetName(prev_name, account.user.username)
        system.WriteAttendance(account)
        system.WriteLeaving(account)

        user.save()
        account.save()

        print(request.POST.get('start_t'))
        return HttpResponseRedirect(reverse("AdminForm"))
        
    else:
        account = get_object_or_404(Account,pk=pk)
        return render(request,"attendance/account_edit.html", {'ChangedUser':account})
    

def daily(request):
    
    path = BASE_DIR/'excel_sheets/QB Daily Report.xlsx/'
    #path_excel = str(Path(BASE_DIR+dir+'time sheet 4.xlsx').resolve())
    #path_pdf = str(Path(BASE_DIR+dir+'pdf_temp.pdf').resolve())
    
    '''pythoncom.CoInitialize()
    excel = win32com.client.Dispatch("Excel.Application")
    _wb = excel.Workbooks.Open(path_excel)
    ws = _wb.Worksheets(user)
    ws.ExportAsFixedFormat(0,path_pdf)
    _wb.Close()
    excel.Quit()

    pythoncom.CoUninitialize() '''
    '''
    wb = load_workbook(dir+'time sheet 4.xlsx')
    ws = wb['s']
    wb.save(dir+'pdf_temp.pdf',SaveFormat.PDF)'''
            
    #response = HttpResponse(open(path_excel, 'rb').read(), content_type='application/vnd.ms-excel')
    pdf_name = "QB Daily Report.xlsx"
    response = HttpResponse(open(path, 'rb').read(), content_type=mimetypes.guess_type(pdf_name)[0])
    
    response['Content-Disposition'] = f'attachment; filename={pdf_name}'
    return response

def control(request):
    now = timezone.now()
    system.TodayBehind12()
    return render(request,"attendance/outxlsx.html")