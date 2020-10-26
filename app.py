import os

from flask import Flask, request
import base64
import label_image2
app = Flask(__name__)

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

@app.route('/getImg', methods=['POST'])
def hello_world():
    result = {}
    data_param = request.get_json(force=True)
    # imgstring = encode_img()
    # return imgstring
    imgstring = data_param['img']
    convert_to_img(imgstring)
    result = label_image2.allFunctCall()
    return {'output': result}


if __name__ == '__main__':
    app.run()
