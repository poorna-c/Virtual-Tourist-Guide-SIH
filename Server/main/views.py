from django.shortcuts import render, redirect
from django.http import JsonResponse
import re
import base64
import numpy as np
import json
import cv2
from keras.models import load_model
from django.conf import settings
from django.contrib.auth.models import User
from .models import details, comments, check_in_data
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

model = None
c = ['AGONDA_BEACH',
'ANJUNA_WEDNESDAY_MARKET',
'ARAMBOL_HIPPIE_FESTIVAL',
'ASILICA_OF_BOM_JESUS',
'BAGA_BEACH',
'CASINO_IN_PANJIM',
'CHAPORA_FORT',
'CHURCH_OF_OUR_LADY_OF_IMMACULATE_CONCEPTION',
'DUDHSAGAR_FALLS',
'FORT_AGUADA',
'FORT_CABO_DE_RAMA',
'GO_KART_RACING',
'GRANDE_ISLAND',
'HALASSA_RESTAURANT',
'HILL_TOP_CLUB_IN_ANJUNA',
'LATIN_QUARTER',
'NAVAL_AVIATION_MUSEUM',
'PARAGLIDING_IN_ARAMBOL',
'TEREKHOL_FORT']

classes = [i.replace("_"," ") for i in c]
data_info = json.load(open('data.json','r'))

# Create your views here.
@login_required
def main(request):
    if not settings.STATS:
        init_stats()
    cmnts = comments.objects.all().order_by('-id')
    context = {"comments":cmnts}
    return render(request,'main/index.html',context)

def livedata(request):
    if request.method == "POST":
        IMAGEDATA = request.POST.get('IMAGEDATA')
        if IMAGEDATA:
            file_ = writeImage(IMAGEDATA)
        img = cv2.imread(file_,cv2.IMREAD_GRAYSCALE)/255
        img = cv2.resize(img,(50,50))
        predictions = predict(img)
        prediction = np.argmax(predictions)
        class_ = classes[prediction]
        try:
            check_in_data(user=request.user,place=str(prediction),p = str(class_)).save()
        except:
            pass
        try:
            settings.STATS[class_] += 1
        except KeyError as e:
            init_stats()
        except:
            pass

        description = data_info[class_]
        data = {
            'prediction':str(class_),
            'description':str(description),
        }
    return JsonResponse(data)

def writeImage(live_data):
    dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
    ImageData = dataUrlPattern.match(live_data).group(2)
    extension =  dataUrlPattern.match(live_data).group(1)
    ImageData = base64.b64decode(ImageData)
    with open('file.'+extension,'wb') as f:
        f.write(ImageData)
    return 'file.'+extension

def predict(img):
    global model
    if not model:
        model = load_model('model.h5')
    predictions = model.predict_proba(img.reshape(-1,50,50))
    return predictions



def init_stats():
    for i in data_info.keys():
        settings.STATS[i] = 0

def stats(request):
    data = settings.STATS
    print(list(data.items()))
    return render(request,'main/stats.html',{'stats':list(data.items())})


def register(request):
    message = []
    if request.method == "POST":
        data = request.POST
        uname = data.get('uname')
        fname = data.get('fname')
        lname = data.get('lname')
        email = data.get('email')
        pass_ = data.get('pass')
        cpass = data.get('cpass')
        mobile = data.get('mobile')
        if User.objects.filter(username = uname).first() is None:
            if len(mobile) > 15:
                message.append("Enter a valid Mobile Number !!!")
                return redirect("register_page")
            elif pass_ != cpass:
                message.append("Both Passwords doesn't match")
                return redirect("register_page")
            try:
                User(username = uname,email=email,first_name=fname,last_name=lname).save()
                u = User.objects.get(username=uname)
                u.set_password(pass_)
                u.save()
                if details.objects.filter(user=u).first() is None:
                    details(user = u,mobile=mobile).save()
                message.append("Registration Successfull with username "+u.username)
                return redirect('login_page')
            except Exception as e:
                message.append(str(e))
        else:
            message.append("User Name Already Taken")
            return redirect('register_page')
        
    return render(request,'main/register.html',{'messages' : message})


def login_(request):
    message = []
    if request.method == "POST":
        uname = request.POST.get("uname")
        pass_ = request.POST.get("pass")
        try:
            user = authenticate(request,username=uname, password=pass_)
            if user is None:
                message.append("User not Found!!!")
                return redirect('login_page',{'messages':message})
            login(request,user)
            return redirect('main_page')
        except Exception as e:
            # message.append("Login Failed, Verify Details... "+str(e))
            pass
    return render(request,'main/login.html',{'messages':message})


def delete_comment(request,id):
    comments.objects.get(id=id).delete()
    return redirect('main_page')

def add_comment(request):
    c = request.POST.get('comment')
    if c != "":
        comments(user=request.user,comment = c).save()
    return redirect('main_page')

def checkins(request):
    data = None
    u = User.objects.all()
    if request.method == "POST":
        p = request.POST.get('place')
        user = request.POST.get('users')
        if p == "" or p == None:
            user = User.objects.get(username = user)
            data = check_in_data.objects.filter(user=user)
        else:
            data = check_in_data.objects.filter(place=p)
    return render(request,'main/data.html',{'data':data,'users':u})