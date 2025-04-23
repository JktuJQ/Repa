# Imports
from backend.application import application
from flask import render_template

from backend.forms.video_cut_form import VideoCutForm

#import cv2
#from ml.find_contour import find_page_contour

#from ml.clip import make_shorts


@application.route("/upgrade_image/")  # <string:filename>", methods=["GET"])
def upgrade_image(filename: str = "frontend/static/paper0.jpg"):
    #image = cv2.imread(filename)
    #points = list(map(lambda l: {"x": int(l[0]), "y": int(l[1])}, map(list, list(find_page_contour(image)))))
    return None#render_template("upgrade_image.html", points=points, filename=filename.split("/static/")[1], image_shape=tuple(image.shape[1::-1]))


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
