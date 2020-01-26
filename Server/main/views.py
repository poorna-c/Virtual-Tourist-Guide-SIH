from django.shortcuts import render
from django.http import JsonResponse
import re
import base64
import numpy as np
import json
import cv2
from keras.models import load_model

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
def main(request):
    context = {}
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