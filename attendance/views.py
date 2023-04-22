from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, ListView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils import timezone
from openpyxl import Workbook, load_workbook
from reportlab.pdfgen import canvas

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
    now = timezone.now()
    if account.is_working:
        account.start_time = now
        working_time = now-now
    else:
        account.end_time = now
        working_time =  now - account.start_time
        system.WriteAttendance(account)
    
    account.save()
    logout(request)

    params = {
        "user"          :account.user,
        "is_working"    :account.is_working,
        "time"          :now,
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
        
def PDF(request,user):
    
    path ='excel_sheets/wageTime_sheets 2023/'
    #path_excel = str(Path(BASE_DIR+dir+'time sheet 4.xlsx').resolve())
    #path_pdf = str(Path(BASE_DIR+dir+'pdf_temp.pdf').resolve())
    path_excel = BASE_DIR/path/'time sheet 4.xlsx'
    path_pdf = BASE_DIR/path/'pdf_temp.pdf'
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
    pdf_name = "Time Sheet:"+"s"+".xlsx"
    response = HttpResponse(open(path_excel, 'rb').read(), content_type=mimetypes.guess_type(pdf_name)[0])
    
    response['Content-Disposition'] = f'attachment; filename={pdf_name}'
    return response

def control(request):
    now = timezone.now()
    system.test()
    #system.AddSheet("ttt")
    return render(request,"attendance/outxlsx.html")