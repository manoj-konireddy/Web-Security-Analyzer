from flask import Flask, render_template, request

import config
from scanner import start_scan

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        url = request.form.get("url")

        result = start_scan(url)

        return render_template(
            "report.html",
            result=result
        )

    return render_template("index.html")


if __name__ == "__main__":

    app.run(
        debug=config.DEBUG,
        host=config.HOST,
        port=config.PORT
    )