# Imports
from globals import *

from backend.application import application, db_session
from flask import render_template, session, url_for, redirect, flash, request

import cv2
from ml.find_contour import find_page_contour

from backend.forms.video_cut_form import VideoCutForm

#from ml.clip import make_shorts


@application.route("/upgrade_image/")  # <string:filename>", methods=["GET"])
def upgrade_image(filename: str = "frontend/static/paper0.jpg"):
    image = cv2.imread(filename)
    points = list(
        map(lambda l: {"x": int(l[0]), "y": int(l[1]), "element": None}, map(list, list(find_page_contour(image)))))
    print(points)
    return render_template("upgrade_image.html", points=points, filename=filename)


@application.route("/process_pins", methods=["POST"])
def process_pins():
    pins = request.json['pins']

    print("Received pin coordinates:", pins)

    return ""


@application.route('/video-cutter/<string:filename>', methods=['GET', 'POST'])
def video_cutter(filename: str):
    form = VideoCutForm()

    if form.validate_on_submit():
        label = form.label.data
        start = form.start_time.data
        end = form.end_time.data

        #make_shorts("frontend/static/" + filename, "frontend/static/clips/" + filename.split("/")[-1],
        #            [t * 60 ** i for i, t in enumerate(start.split(":")[::-1])], [t * 60 ** i for i, t in enumerate(end.split(":")[::-1])],
        #            f"data/clips_base/{label}.mp4")

        return render_template('video_cutter.html', form=form, success=True)

    return render_template('video_cutter.html', form=form)
