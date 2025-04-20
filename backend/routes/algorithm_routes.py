# Imports
from globals import *

from backend.application import application, db_session
from flask import render_template, session, url_for, redirect, flash, request

import cv2
from ml.find_contour import find_page_contour


@application.route("/upgrade_image/")#<string:filename>", methods=["GET"])
def upgrade_image(filename: str = "frontend/static/paper0.jpg"):
    image = cv2.imread(filename)
    points = list(map(lambda l: {"x": int(l[0]), "y": int(l[1]), "element": None}, map(list, list(find_page_contour(image)))))
    print(points)
    return render_template("upgrade_image.html", points=points, filename=filename)


@application.route("/process_pins", methods=["POST"])
def process_pins():
    pins = request.json['pins']

    print("Received pin coordinates:", pins)

    return ""