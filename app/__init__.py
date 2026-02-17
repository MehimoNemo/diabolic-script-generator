"""The generator server"""
import os;
import sys;
from flask import Flask, render_template, request, jsonify
from .diabolic import Diabolic

def get_base_path():
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS  # PyInstaller temp folder
    return os.path.abspath(".")

base_path = get_base_path()

app = Flask(
    __name__,
    template_folder=os.path.join(base_path, "templates"),
    static_folder=os.path.join(base_path, "static"),
)

@app.route("/", methods=["GET", "POST"])
def index() -> str:
    """The main function

    Returns:
        str: HTML or JSON for given text
    """
    text = (
        request.json.get("text")
        if request.is_json
        else request.values.get("text")
        if request.method in ["GET", "POST"]
        else None
    )
    url = Diabolic(text).data_url if text is not None else None

    if request.is_json:
        return jsonify({"url": url})

    return render_template(
        "index.html",
        url=url,
        text=text,
    )
