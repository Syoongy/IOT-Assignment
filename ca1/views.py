from ca1 import app
import os
import json
from flask import request, Response, render_template, redirect, jsonify
from flask_uploads import UploadSet, configure_uploads, IMAGES
from scripts import ocr_detect, item_database, read_tmp, takePiCamImg

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'ca1/static/images'
configure_uploads(app, photos)


@app.route('/')
def index():
    itemList = item_database.getItems()
    imgList = os.listdir('ca1/static/images/detected')
    print(os.listdir('ca1/static/images/detected'))
    templateData = {
        'itemData': itemList,
        'images': imgList
    }
    return render_template('home.html', **templateData)


@app.route('/getTempData', methods=['GET'])
def getTempData():
    data = read_tmp.readTemp()
    return jsonify(result=data)


@app.route('/scan')
def scan():
    return render_template('scan.html')


@app.route('/detectImg', methods=['GET', 'POST'])
def detectImg():
    if request.method == 'POST' and 'file' in request.files:
        for file in os.listdir("ca1/static/images"):
            if file.endswith(".jpg"):
                os.remove(os.path.join("ca1/static/images", file))
        myfilename = photos.save(request.files['file'])
        listOfResults = ocr_detect.ocr_space_file(
            filename='ca1/static/images/' + myfilename)
        print(listOfResults)
        templateData = {
            'response': listOfResults
        }
        return render_template('scanned.html', **templateData)
    else:
        listOfResults = ocr_detect.ocr_space_file(
            filename='ca1/static/images/test.jpg')
        print(listOfResults)
        templateData = {
            'response': listOfResults
        }
        return render_template('scanned.html', **templateData)

@app.route('/detectImgPi', methods=['POST'])
def detectImgPi():
    takePiCamImg.takeImg()
    return json.dumps({'success':True}, 200, {'ContentType':'application/json'})


@app.route('/addItem/<path:expiry>', methods=['GET', 'POST'])
def addItem(expiry):
    if request.method == 'POST':
        item_database.addItem(request.form['name'], expiry)
        return redirect('/')
    else:
        templateData = {
            'expiry': expiry
        }
        return render_template('addItem.html', **templateData)
