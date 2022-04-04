from app import app
from flask import render_template
from flask import request, redirect, Flask, flash, url_for, json, jsonify
import os
from werkzeug.utils import secure_filename
#from final1 import trigg
from pdf2image import convert_from_path
import subprocess

app.config['ALLOWED_IMAGE_EXTENSIONS']=['JPEG', 'JPG', 'PDF', 'TIFF']
app.config['UPLOAD_FOLDER'] = '/Users/gsaketha/Desktop/Form_16/yolov5/uploads'

def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def convert_pdf_to_images(img):
    images = convert_from_path(os.path.join(app.config['UPLOAD_FOLDER'], img))
    for index, image in enumerate(images):
        image.save(os.path.join(app.config['UPLOAD_FOLDER'],f'{img}-{index}.png')) 

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            if allowed_image(image.filename):
                if image.filename[-3:] in ['PDF','pdf']:
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
                    convert_pdf_to_images(image.filename)
                else:
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
                os.chdir('/Users/gsaketha/Desktop/Form_16/yolov5')
                for filename in os.listdir('/Users/gsaketha/Desktop/Form_16/yolov5/uploads'):
                    subprocess.run(['python3', 'detect.py', '--source', os.path.join(app.config['UPLOAD_FOLDER'], f'{filename}'),'--weight', '/Users/gsaketha/Desktop/Form_16/yolov5/runs/train/weights/best.pt','--hide-labels','--save-crop'])
                #filename = secure_filename(image.filename)
                #image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
                
            
    return render_template("upload.html")

#@app.route("/display")
#def display():
#    return render_template("display.html")

# @app.route("/prepro", methods=["GET", "POST"])
# def prepro():
#     if request.method == "POST":
#         trigg()
#     return render_template("display.html")

# with open('/Users/gsaketha/Desktop/Form_16/yolov5/runs/output_json/output.json', 'r') as myfile:
#     data = myfile.read()

@app.route("/display", methods=["GET", "POST"])
def display():
    with open('/Users/gsaketha/Desktop/Form_16/yolov5/runs/output_json/output.json', 'r') as myfile:
        data = myfile.read()
    return render_template('display.html', title="page", jsonfile=json.dumps(data))