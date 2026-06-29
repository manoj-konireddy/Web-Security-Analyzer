from flask import Flask, render_template, request, send_file

import config
from scanner import start_scan

from flask import make_response
from datetime import datetime

from modules.export_report import (
    save_json_report,
    load_json_report,
    get_report_details,
    generate_pdf_report
)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        url = request.form.get("url")

        result = start_scan(url)

        if not result["website"]["reachable"]:

            return render_template(
                "index.html",
                error=result["website"]["error"],
                url=url
            )

        save_json_report(result)

        return render_template(
            "report.html",
            result=result,
            download=False
        )

    return render_template("index.html")

@app.route("/download/json")
def download_json():

    return send_file(
        "reports/security_report.json",
        as_attachment=True,
        download_name="security_report.json"
    )

@app.route("/download/pdf")
def download_pdf():

    result = load_json_report()

    if result is None:

        return "No report found. Please scan a website first."

    report = get_report_details(result)

    filename = "reports/security_report.pdf"

    generate_pdf_report(
        result,
        report,
        filename
    )

    return send_file(
        filename,
        as_attachment=True
    )


if __name__ == "__main__":

    app.run(
        debug=config.DEBUG,
        host=config.HOST,
        port=config.PORT
    )