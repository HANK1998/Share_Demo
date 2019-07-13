from django.shortcuts import render
from django.views.generic import View
from .models import Upload
from django.http import HttpResponsePermanentRedirect,HttpResponse
import random
import string
import datetime
import json

# Create your views here.
class HomeView(View):
    def get(self,request):
        return render(request,'base.html',{})

    def post(self,request):
        if request.FILES:
            file = request.FILES.get("file")#获取文件
            name = file.name
            size = int(file.size)
            with open('static/file/'+name,'wb')as f:
                f.write(file.read())
            code = ''.join(random.sample(string.digits,8))
            u = Upload(
                path='static/file/'+name,
                name=name,
                Filesize=size,
                code=code,
                PCIP=str(request.META['REMOTE_ADDR']),#获取上传文件的用户IP
            )
            u.save()
            return HttpResponsePermanentRedirect("/s/"+code)
        # HttpResponsePermanentRedirect 重定向到展示文件的页面.这里的 code 唯一标示一个文件。

class DisplayView(View):
    def get(self,request,code):
        u = Upload.objects.filter(code=str(code))
        if u:
            for i in u:
                i.DownloadDocunt += 1
                i.save()
        return render(request,'content.html',{"content":u})

class MyView(View):
    def get(self,request):
        IP = request.META['REMOTE_ADDR']
        u = Upload.objects.filter(PCIP=str(IP))
        for i in u:
            i.DownloadDocunt += 1
            i.save()
        return render(request,'content.html',{"content":u})


class SearchView(View):
    def get(self,request):
        code = request.GET.get("kw")
        u = Upload.objects.filter(name=str(code))
        data = {}
        if u:
            for i in range(len(u)):
                u[i].DownloadDocunt += 1
                u[i].save()
                data[i] = {}
                data[i]['download'] = u[i].DownloadDocunt
                data[i]['filename'] = u[i].name
                data[i]['id'] = u[i].id
                data[i]['ip'] = str(u[i].PCIP)
                data[i]['size'] = u[i].Filesize
                data[i]['time'] = str(u[i].Datatime.strftime('%Y-%m-%d %H:%M'))
                #时间格式化
                data[i]['key'] = u[i].code
        return HttpResponse(json.dumps(data),content_type="application/json")