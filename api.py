import os, glob, base64, label_image_new,sqlite3 as sql

from flask import Flask, request, jsonify, redirect, flash, url_for,render_template

app = Flask(__name__)
app.secret_key = "testkey"
app.config["IMAGE_UPLOADS"] = 'C:\\Users\\anmol\\Downloads\\TOC Project'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024


@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/imagerec')
def imagerec():
    return render_template('imagereceived.html')

@app.route('/location', methods=['GET'])
def location():
    return render_template('location.html')

@app.route('/result', methods=['GET','POST'])
def result():
    result = {}
    if request.method == 'POST':
        list_of_files = glob.glob('./*.jpg')  + glob.glob('./*.png') + glob.glob('./*.jpeg') 
        latest_file = max(list_of_files, key=os.path.getctime)
        latest_img_name = str(latest_file[2:]) #print(latest_file[2:]) gives e.g. BirthdayDP.jpg
        result = label_image_new.allFunctCall(latest_img_name)
        complaint_type = (result[:7]).title()


    if result != "Class can't be identified":
        try:
            address = request.form['addr']
            landmark = request.form['lmark']
            state = request.form['state']
            pincode = request.form['pin']
         
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO complaints (address,landmark,state,pincode,complaint_type) VALUES (?,?,?,?,?)",(address,landmark,state,pincode,complaint_type) )         
                con.commit()
                print("Record successfully added")
        except:
            con.rollback()
            print("Error in insert operation")
        finally:
            con.close()
            return render_template('result.html',complaint_type=complaint_type)
        
    else:
        os.remove(os.path.join(app.config["IMAGE_UPLOADS"], latest_img_name))
        return render_template('failure.html')
        


# @app.route('/encode_img', methods=['POST'])
# def encode_img():
#     filename = os.path.abspath(os.path.join(os.path.dirname(__file__), 'man.jpg'))
#     with open(filename, "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read())
#     return encoded_string

# def convert_to_img(imgstring):

#     imgdata = base64.b64decode(imgstring)
#     filename = 'input.jpg'
#     with open(filename, 'wb') as f:
#         f.write(imgdata)

@app.route('/getImg', methods=['GET','POST'])
def getImg():
    if request.method== 'POST':
        if request.files:
            image = request.files['file']
            if image.filename != '':
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
                return redirect(url_for('imagerec'))
            else:
                return redirect(request.url)
    return redirect(url_for('homepage'))
    

if __name__ == '__main__':
    app.run(port=7000,debug=True)

