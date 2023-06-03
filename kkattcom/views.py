from django.http import HttpResponse
from django.shortcuts import render , redirect , reverse
from db.models import *
from django.db.models import Q , F
from django.template import loader
from django import forms

import os, random
from pptx import Presentation
from pptx.enum.dml import MSO_COLOR_TYPE
from pptx.dml.color import RGBColor

#from django.views.decorators.csrf import csrf_exempt , login_required
import webbrowser

def index(request):
    #path = 'index'
    if 'id' in request.session:
        id = request.session['id']
        name = request.session['name']
    

    #return render(request, 'index.html', locals())
    return redirect(stdgindex)

def swkm(request):
    return redirect(stdgindex)

def about(request):
    return HttpResponse("<TABLE border=2;background-color: #96D4D4;><TR><td>This is col one</td><td>This is col 2</td></TR></TABLE>")

def app(request, appno):
    return HttpResponse(f'Application #{appno}')

def dashboard(request):
    if 'id' in request.session:
        id = request.session['id']
        row = user.objects.filter(relation='kkattmos49kkattmos94', id=id)
        if row.count() == 0:
            return redirect(stdgindex)
    else:
        return redirect(stdgindex)
    
    #Giveaway SWKM - 000
    d000 = giveawaycontroller2.objects.first()
    
    if request.method == 'POST':
        giveawayHistory.objects.all().delete()
        giveawaycontroller2.objects.all().delete()
        #review.objects.all().delete()
        #kwamnaijai.objects.all().delete()    
        for r in theme.objects.all():
            (r.count) == 0
        for r in pack.objects.all():
            (r.count) == 0
        form = giveawaycontrolForm(request.POST)
        active = giveawaycontroller2.objects.first()
        print(active)
        form.save()
        Form000 = None
    else:
        Form000 = giveawaycontrolForm()  

    return render(request, 'dashboard.html', locals())

def kkattdrop(request):
    if 'id' in request.session:
        id = request.session['id']
        name = request.session['name']
        profile = user.id.get(id=id)
        return render(request, 'kkattdrop.html', {'id':id,'name':name,'profile':profile})
    
    return render(request, 'kkattdrop.html')

def stdgindex(request):
    x = giveawaycontroller2.objects.filter(active=True)
    c = giveawayHistory.objects.count()

    if 'id' in request.session:
        id = request.session['id']
        name = request.session['name']
        return render(request, 'stdgindex.html',{'id':id,'name':name,'x':x, 'c':c})
    else:
        id = None
        return render(request, 'stdgindex.html',{'x':x,'c':c})

def logout(request):
    request.session.modified = True
    if 'id' in request.session:
        del request.session['id']

    return redirect(stdgindex)

# @csrf.exempt
def login(request):
    err_msg =''
    if request.method == 'POST':
        form = signinForm(request.POST)
        e = request.POST.get('Email', '')
        p = request.POST.get('Password','')

        row = user.objects.filter(
            Q(email = e) & Q(pwd = p)
        )

        if row.count() == 1:
            request.session['id'] = row[0].id
            request.session['name'] = row[0].name
            request.session.modified = True
            return redirect(stdgindex)
            #History.back()
        else:
            login = None
            err_msg = 'อีเมลล์หรือรหัสผ่านไม่ถูกต้อง'

    else:
        form = signinForm()
        login = None

    return render(request, 'account.html', {'form':form,'login':login,'err_msg':err_msg,'header':'เข้าสู่ระบบ','buttonlabel':'เข้าสู่ระบบ','accountreq':0})

def changepassword (request):
    if 'id' in request.session:
        id = request.session['id']
        
    else:
        return redirect(login)
    err_msg = ''

    if request.method == 'POST':
        form = changepwdForm(request.POST)
        x = request.POST.get('prepwd','')
        y = request.POST.get('newpwd','')

        row = user.objects.filter(id = id, pwd = x)
        if row.count() == 1 and y is not None:
            for r in row:
                user.objects.filter(id = id).update(pwd = y)
                return redirect(accountedit)
        else:
            err_msg = 'รหัสผ่านไม่ถูกต้อง'
    else:
        form = changepwdForm()
    
    return render(request, 'account.html', {'form':form,'header':'แก้ไขรหัสผ่าน','buttonlabel':'บันทึกข้อมูล','accountreq':3, 'err_msg':err_msg})

def accountcreate(request):
    if 'id' in request.session:
        return redirect(accountedit)
    
    err_msg = ''
    if request.method == 'POST':
        form = userForm(request.POST)
        e = request.POST.get('Email','')
        if form.is_valid():
            row = user.objects.filter(email=e)
            if row.count() == 0:
                form.save()
                #row = user.objects.filter(email=e)
                #request.session['id'] = row.id
                #request.session.modified = True
                return(redirect(login)) 
            else:
                err_msg = 'มีอีเมลล์นี้อยู่ในระบบแล้ว'
        else:
            err_msg = 'กรุณากรอกข้อมูลให้ครบถ้วน'
    else:
        form = userForm()

    return render(request, 'account.html', {'form':form,'header':'สร้างบัญชีใหม่','buttonlabel':'สร้างบัญชี','accountreq':1, 'err_msg':err_msg})

def accountedit(request):
    if 'id' not in request.session:
        return redirect(login)
    
    id = request.session['id']
    action = None
    err_msg = ''
    if request.method == 'POST':
        row = user.objects.get(id=id)
        form = usereditform(instance=row, data=request.POST)
        if form.is_valid():
            form.save()

            request.session['name'] = row.name
            return redirect(stdgindex)

    else:
        row = user.objects.get(id=id)
        form = usereditform(initial=row.__dict__)
        action = reverse(accountedit)
        err_msg = ''

    return render(request, 'account.html', {'form':form,'action':action,'err_msg':err_msg,'header':'จัดการบัญชี','accountreq':2,'buttonlabel':'บันทึกข้อมูล'})

def sheeterror(request):
    note_msg = ''
    if 'id' not in request.session:
        return redirect(login)
    else:
        id = request.session['id']
        name = request.session['name']

    if request.method =='POST':
        form = errorreportForm(request.POST, request.FILES)
        if form.is_valid():
            note_msg = 'แจ้งไปยังแอดมินแล้วครับ ขอบคุณที่ช่วยแจ้งจุดผิดครับ'
            form.save()
            return redirect(stdgindex)
    else:
        form = errorreportForm()

    return render(request, 'sheeterror.html',{'id':id,'name':name,'form':form})
   
def stdggiveaway(request):

    if 'id' not in request.session:
        return redirect(login)
    
    id = request.session['id']
    name = request.session['name']
    idfilter = giveawayHistory.objects.filter(userid = id)

    if idfilter.count() == 1:
        for r in idfilter:
            c = (r.pack)
            t = (r.theme)
            p = (r.pos)
            pa = (r.posall)

        u = sheetfile.objects.filter(code=c, theme=t)

        form2 = reviewForm()
        if request.method =='POST':
            x = review(userid = id, user=name, code = c, text = request.POST.get('text',None))
            x.save()

        return render(request, 'stdggiveaway2.html', {'id':id,'name':name, 'u':u, 'form2':form2, 'p':p,'pa':pa})
    
    else:
        if request.method =='POST':
            form = giveawayForm(request.POST)

            r = giveawaycontroller2.objects.first()
            s = (r.season)

            theme.objects.filter(code=request.POST.get('theme', None)).update(count=F('count')+1)
            t = theme.objects.filter(code=request.POST.get('theme', None))
            for r in t:
                h = (r.code)
            
            pack.objects.filter(grade=request.POST.get('grade', None), season=s).update(count=F('count')+1)
            p = pack.objects.filter(grade=request.POST.get('grade', None), season=s)
            for r in p:
                c = (r.code)
            
            pos = giveawayHistory.objects.filter(pack=c)
            poscount = pos.count() + 1
            
            posall = giveawayHistory.objects.all()
            posallcount = posall.count() + 1

            info = giveawayHistory(userid = id, user = name, pack=c, theme=h, pos=poscount, posall=posallcount)
            info.save()

            return redirect(stdggiveaway)
        else:
            x = giveawaycontroller2.objects.filter(active=True)
            form = giveawayForm()
            return render(request, 'stdggiveaway1.html', {'id':id,'name':name, 'form':form,'x':x})

def themelist(request):
    t = theme.objects.order_by('code')

    if 'id' in request.session:
        id = request.session['id']
        name = request.session['name']
        return render(request, 'stdgtheme.html', {'id':id,'name':name, 't':t})
    
    return render(request, 'stdgtheme.html', {'t':t})

def resetgiveaway(request):
    if 'id' in request.session:
        id = request.session['id']
        row = user.objects.filter(relation='kkattmos49kkattmos94', id=id)
        if row.count() == 0:
            return redirect(stdgindex)
    else:
        return redirect(stdgindex)
    
    theme.objects.all().update(count=0)
    pack.objects.all().update(count=0)
    giveawayHistory.objects.all().delete()

    return HttpResponse("Reset Successfully")

def save_file(dir, file):
    if not dir.endswith('/'):
        dir += '/'
    
    with open('f{dir}{file.name}','wb+') as target:
        for chunk in file.chunks():
            target.write(chunk)