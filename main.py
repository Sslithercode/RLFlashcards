from flask import Flask,render_template, request, Response
import urllib
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/find")
def track_species():
    return render_template("camera.html")

@app.route('/save-image', methods=['POST'])
def save_image():
    img_data = request.get_data().decode()
    resp = urllib.request.urlopen(img_data) 
    with open('image.jpg', 'wb') as f:
        f.write(resp.file.read())
    return "Image saved to server."
   

if __name__ == "__main__":
    app.run()