import os
from flask import Flask, render_template, request, send_file
from rembg import remove
from PIL import Image, ImageEnhance

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return "No file uploaded"
    file = request.files['image']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    return render_template('index.html', filename=file.filename)

@app.route('/remove_bg/<filename>')
def remove_bg(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    with open(filepath, 'rb') as f:
        result = remove(f.read())
    output_path = os.path.join(UPLOAD_FOLDER, 'no_bg_' + filename)
    with open(output_path, 'wb') as out:
        out.write(result)
    return send_file(output_path, mimetype='image/png')

@app.route('/enhance/<filename>')
def enhance(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    image = Image.open(filepath)
    enhancer = ImageEnhance.Color(image)
    enhanced_image = enhancer.enhance(2.0)
    output_path = os.path.join(UPLOAD_FOLDER, 'enhanced_' + filename)
    enhanced_image.save(output_path)
    return send_file(output_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
