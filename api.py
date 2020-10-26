import os

from flask import Flask, request, jsonify, redirect, flash, url_for,render_template
import base64
import label_image_new

app = Flask(__name__)
app.secret_key = "testkey"
app.config["IMAGE_UPLOADS"] = 'C:\\Users\\anmol\\Downloads\\TOC Project'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024


@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/imagerec')
def imagerec():
    return render_template('imagereceived.html')

@app.route('/location')
def location():
    return render_template('location.html')

# @app.route('/encode_img', methods=['POST'])
def encode_img():
    filename = os.path.abspath(os.path.join(os.path.dirname(__file__), 'man.jpg'))
    with open(filename, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string

def convert_to_img(imgstring):

    imgdata = base64.b64decode(imgstring)
    filename = 'input.jpg'
    with open(filename, 'wb') as f:
        f.write(imgdata)

@app.route('/getImg', methods=['GET','POST'])
def getImg():
    #result = {}
    if request.method== 'POST':
        if request.files:
            image = request.files['file']
            if image.filename != '':
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
                return redirect(url_for('imagerec'))
            else:
                return redirect(request.url)
    return redirect(url_for('homepage'))
    # data_param = request.get_json(force=True)
    # # imgstring = encode_img()
    # # return imgstring
    # imgstring = data_param['img']
    # convert_to_img(imgstring)
    # result = label_image_new.allFunctCall()
    # return jsonify({'output': result})

if __name__ == '__main__':
    app.run(port=7000,debug=True)

