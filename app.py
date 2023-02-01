""" Flask application

"""

__author__ = "Jeanne Michel"
__contact__ = "jeanne.michel@he-arc.ch"
__copyright__ = "© 2023 HE-Arc"
__date__ = "25/01/2023"

import json
from flask import Flask, render_template, url_for, request, redirect, Response, jsonify, send_file
# import fft_lib
import imageio
# from flask_socketio import SocketIO
from threading import Thread
import cv2
import base64
import datetime
import numpy as np
import matplotlib.pyplot as plt
import io
from io import BytesIO
import random
import os
from lib.Gif import Gif
import time
# from flask_socketio import SocketIO, emit

# launch server : flask --app app --debug run

# allows cors requests
from flask_cors import CORS


thread = None
gif: Gif = None
is_startup = True

""" Flask application """
app = Flask(__name__)
CORS(app)


@ app.route('/')
@ app.route('/home')
def home():
    """ Render home page """
    return render_template('home.html')


def gen():
    """Video streaming generator function."""
    while True:
        global gif
        frame = gif.get_last_image()

        if len(frame.shape) == 2:
            frame = cv2.normalize(frame, None, 0, 1, cv2.NORM_MINMAX)
            img = (np.clip(frame, 0, 1) * 255).astype(np.uint8)
            ret, jpeg = cv2.imencode('.jpeg', img)
            img_bytes = bytes(jpeg)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img_bytes + b'\r\n')

        else:
            ret, bmp = cv2.imencode('.bmp', frame)
            img_bytes = bytes(bmp)

            yield (b'--frame\r\n'
                   b'Content-Type: image/bmp\r\n\r\n' + img_bytes + b'\r\n')

        time.sleep(0.1)


@app.route('/image_feed')
def image_feed():
    return Response(gen(), mimetype="multipart/x-mixed-replace; boundary=frame")


@ app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        """ Render generate page """
        image = request.files.get('image')
        json_file = request.files.get('json_file')
        image_data = image.read()
        json_data = json.load(json_file)

        new_gif = Gif(image_data=image_data, json_data=json_data)
        new_gif.start()
        gif_data = new_gif.generate(return_bytes=True)
        gif_data_base64 = base64.b64encode(gif_data).decode("ascii")
        return render_template('generate.html', gif_data_base64=gif_data_base64)

    return render_template('generate.html')


@ app.route('/about')
def about():
    """ Render about page """
    return render_template('about.html')


@app.route('/get_last_image_')
def get_last_image_():
    global gif
    global fig
    global plot
    global is_startup

    image = gif.get_last_image()

    if is_startup:
        fig = plt.Figure()
        plot = fig.add_subplot(111).imshow(image, cmap='gray')
        plt.xticks([]), plt.yticks([])

        is_startup = False

    plot.set_data(image)
    plot.autoscale()
    buf = io.BytesIO()
    fig.savefig(buf, format="jpg")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return jsonify(data)


def calculate_image_data():
    global gif
    gif = Gif("logo.png", "parameters.json", True)
    print("calculate_image_data")
    gif.start()
    pass


@app.before_first_request
def activate_job():
    global thread
    if thread is None:
        thread = Thread(target=calculate_image_data)
        thread.start()


if __name__ == '__main__':
    app.run(debug=False)
