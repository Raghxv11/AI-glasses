from flask import Flask,render_template
from Face_Recognition import face_detect
from Object_Detection import object_detect
app = Flask(__name__)


@app.route("/")
def welcome():
    return render_template('index.html') 


@app.route("/Face-Detection")
def faceRecognition():
    face_detect()
    return 'Logs Stored!'


@app.route("/Object-Detection")
def objectDetection():
    object_detect()
    return 'Logs Stored!'

if __name__ == "__main__":
    app.run(debug = True)