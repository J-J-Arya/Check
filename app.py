# import os
# from flask import Flask, render_template, request, redirect, url_for
# import cv2

# app = Flask(__name__)
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# def count_closed_shapes(image_path):
#     img = cv2.imread(image_path, 0)
#     _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
#     contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#     count = 0
#     for cnt in contours:
#         approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
#         if cv2.contourArea(cnt) > 100 and cv2.isContourConvex(approx):
#             count += 1
#     return count

# @app.route('/')
# def splash():
#     return render_template('splash.html')

# @app.route('/spider-check', methods=['GET', 'POST'])
# def spider_check():
#     if request.method == 'POST':
#         legs = request.form.get('legs')
#         webs = request.form.get('webs')
#         if legs == 'yes' and webs == 'yes':
#             return redirect(url_for('upload'))
#         else:
#             return render_template('spider_check.html', not_spider=True)
#     return render_template('spider_check.html', not_spider=False)

# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     if request.method == 'POST':
#         file = request.files['image']
#         if file:
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#             file.save(filepath)
#             count = count_closed_shapes(filepath)
#             return render_template('result.html', count=count)
#     return render_template('upload.html')

# @app.route('/result')
# def result():
#     return render_template('result.html')

# if __name__ == '__main__':
#     os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#     app.run(debug=True)

import os
from flask import Flask, render_template, request, redirect, url_for
import cv2

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Improved spider web loop detection
def count_closed_shapes(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Dilate to close small gaps in web lines
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilated = cv2.dilate(edges, kernel, iterations=1)

    # Find contours
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Count closed contours
    count = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 50:  # filter out noise
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            if cv2.isContourConvex(approx):
                count += 1
    return count

@app.route('/')
def splash():
    return render_template('splash.html')

@app.route('/spider-check', methods=['GET', 'POST'])
def spider_check():
    if request.method == 'POST':
        legs = request.form.get('legs')
        webs = request.form.get('webs')
        if legs == 'yes' and webs == 'yes':
            return redirect(url_for('upload'))
        else:
            return render_template('spider_check.html', not_spider=True)
    return render_template('spider_check.html', not_spider=False)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['image']
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            count = count_closed_shapes(filepath)
            return render_template('result.html', count=count)
    return render_template('upload.html')

@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
