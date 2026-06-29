import copy
import json
import os
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.enums import TA_CENTER

from reportlab.lib.units import inch

from reportlab.pdfbase.pdfmetrics import stringWidth

def prepare_result(result):

    clean_result = copy.deepcopy(result)

    if "website" in clean_result:

        if "headers" in clean_result["website"]:

            clean_result["website"]["headers"] = dict(
                clean_result["website"]["headers"]
            )

        if "cookies" in clean_result["website"]:

            cookies = []

            for cookie in clean_result["website"]["cookies"]:

                cookies.append({

                    "name": cookie.name,

                    "value": cookie.value,

                    "domain": cookie.domain,

                    "path": cookie.path

                })

            clean_result["website"]["cookies"] = cookies

    return clean_result

def save_json_report(result):

    clean_result = prepare_result(result)

    os.makedirs("reports", exist_ok=True)

    filepath = os.path.join(
        "reports",
        "security_report.json"
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            clean_result,
            file,
            indent=4
        )

    return filepath

def load_json_report():

    filepath = os.path.join(
        "reports",
        "security_report.json"
    )

    if not os.path.exists(filepath):

        return None

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)
    
def get_report_details(result):

    website = result["website"]["url"]

    website = website.replace("https://", "")

    website = website.replace("http://", "")

    website = website.replace("www.", "")

    website = website.replace("/", "")

    now = datetime.now()

    report_date = now.strftime("%d %B %Y")

    report_time = now.strftime("%I:%M:%S %p")

    return {

        "website": website,

        "generated_date": report_date,

        "generated_time": report_time

    }

def generate_pdf_report(result, report, filename):

    doc = SimpleDocTemplate(

        filename,

        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40

    )

    styles = getSampleStyleSheet()

    story = []

    title_style = styles["Title"]

    title_style.alignment = TA_CENTER

    title_style.textColor = colors.HexColor("#2563EB")

    heading_style = styles["Heading2"]

    heading_style.textColor = colors.HexColor("#2563EB")

    normal_style = styles["BodyText"]


    # ---------------------------------------------------
    # Title
    # ---------------------------------------------------

    story.append(

        Paragraph(

            "<b>WEB SECURITY ANALYZER</b>",

            title_style

        )

    )

    story.append(

        Paragraph(

            "Website Security Assessment Report",

            heading_style

        )

    )

    story.append(

        Spacer(1, 0.30 * inch)

    )


    # ---------------------------------------------------
    # Executive Summary
    # ---------------------------------------------------

    summary_data = [

        ["Target Website", result["website"]["url"]],

        ["Overall Score", f'{result["risk"]["score"]} / 100'],

        ["Risk Level", result["risk"]["risk"]],

        ["Generated Date", report["generated_date"]],

        ["Generated Time", report["generated_time"]]

    ]


    summary_table = Table(

        summary_data,

        colWidths=[170, 320]

    )

    summary_table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#2563EB")),

            ("TEXTCOLOR", (0, 0), (0, -1), colors.white),

            ("BACKGROUND", (1, 0), (1, -1), colors.whitesmoke),

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),

            ("TOPPADDING", (0, 0), (-1, -1), 10),

            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),

            ("FONTSIZE", (0, 0), (-1, -1), 10)

        ])

    )

    story.append(summary_table)

    story.append(Spacer(1, 0.35 * inch))


    # ---------------------------------------------------
    # Security Score Box
    # ---------------------------------------------------

    score = result["risk"]["score"]


    if score >= 80:

        score_color = colors.green

    elif score >= 50:

        score_color = colors.orange

    else:

        score_color = colors.red


    score_table = Table(

        [

            ["SECURITY SCORE"],

            [f"{score} / 100"],

            [result["risk"]["risk"].upper()]

        ],

        colWidths=[220]

    )

    score_table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("BACKGROUND", (0, 1), (-1, 1), colors.white),

            ("TEXTCOLOR", (0, 1), (-1, 1), score_color),

            ("BACKGROUND", (0, 2), (-1, 2), colors.HexColor("#F3F4F6")),

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),

            ("FONTSIZE", (0, 1), (-1, 1), 22),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),

            ("TOPPADDING", (0, 0), (-1, -1), 12)

        ])

    )

    story.append(score_table)

    story.append(Spacer(1, 0.40 * inch))


    # ---------------------------------------------------
    # Executive Summary Text
    # ---------------------------------------------------

    story.append(

        Paragraph(

            "<b>Executive Summary</b>",

            heading_style

        )

    )

    story.append(

        Paragraph(

            "This report provides an automated security assessment of the target website. "
            "The analysis includes Website Information, Security Headers, SSL Certificate, "
            "Cookie Analysis, HTTP Methods, robots.txt, security.txt and security "
            "recommendations based on the observed security posture.",

            normal_style

        )

    )

    story.append(

        Spacer(1, 0.40 * inch)

    )

    # ---------------------------------------------------
    # Website Information
    # ---------------------------------------------------

    story.append(
        Paragraph(
            "Website Information",
            heading_style
        )
    )

    website_data = [

        ["Status Code", str(result["website"]["status_code"])],

        ["Response Time", f'{result["website"]["response_time"]} ms'],

        ["Server", result["website"]["server"]],

        ["Content Type", result["website"]["content_type"]],

        ["Powered By", result["website"]["powered_by"]],

        ["Redirected", str(result["website"]["redirected"])]

    ]


    website_table = Table(

        website_data,

        colWidths=[170,320]

    )

    website_table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#DBEAFE")),

            ("GRID",(0,0),(-1,-1),0.6,colors.grey),

            ("BOTTOMPADDING",(0,0),(-1,-1),8),

            ("TOPPADDING",(0,0),(-1,-1),8),

            ("FONTNAME",(0,0),(-1,-1),"Helvetica")

        ])

    )

    story.append(website_table)

    story.append(Spacer(1,0.30*inch))


    # ---------------------------------------------------
    # Security Headers
    # ---------------------------------------------------

    story.append(

        Paragraph(

            "Security Headers",

            heading_style

        )

    )

    header_rows = [

        [

            "Header",

            "Status"

        ]

    ]


    for header in result["security_headers"]["headers"]:

        if header["present"]:

            status = "Present"

        else:

            status = "Missing"

        header_rows.append(

            [

                header["name"],

                status

            ]

        )


    header_rows.append(

        [

            "Headers Score",

            f'{result["security_headers"]["score"]} / {result["security_headers"]["total"]}'

        ]

    )


    header_table = Table(

        header_rows,

        colWidths=[340,150]

    )

    header_table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#2563EB")),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("GRID",(0,0),(-1,-1),0.6,colors.grey),

            ("BACKGROUND",(0,1),(-1,-2),colors.whitesmoke),

            ("BACKGROUND",(0,-1),(-1,-1),colors.HexColor("#DBEAFE")),

            ("BOTTOMPADDING",(0,0),(-1,-1),8),

            ("TOPPADDING",(0,0),(-1,-1),8),

            ("ALIGN",(1,1),(1,-1),"CENTER")

        ])

    )

    story.append(header_table)

    story.append(Spacer(1,0.30*inch))


    # ---------------------------------------------------
    # SSL Certificate
    # ---------------------------------------------------

    story.append(

        Paragraph(

            "SSL Certificate",

            heading_style

        )

    )


    ssl = result["ssl"]


    ssl_data = [

        [

            "HTTPS Enabled",

            "Yes" if ssl["enabled"] else "No"

        ],

        [

            "Certificate Valid",

            "Yes" if ssl["valid"] else "No"

        ],

        [

            "Issued To",

            ssl["issued_to"]

        ],

        [

            "Issuer",

            ssl["issuer"]

        ],

        [

            "Valid From",

            ssl["valid_from"]

        ],

        [

            "Valid Until",

            ssl["valid_until"]

        ],

        [

            "Days Remaining",

            str(ssl["days_remaining"])

        ]

    ]


    ssl_table = Table(

        ssl_data,

        colWidths=[170,320]

    )

    ssl_table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#DBEAFE")),

            ("GRID",(0,0),(-1,-1),0.6,colors.grey),

            ("BOTTOMPADDING",(0,0),(-1,-1),8),

            ("TOPPADDING",(0,0),(-1,-1),8)

        ])

    )

    story.append(ssl_table)

    story.append(Spacer(1,0.40*inch))

    # ---------------------------------------------------
    # Cookie Analysis
    # ---------------------------------------------------

    story.append(
        Paragraph(
            "Cookie Analysis",
            heading_style
        )
    )

    cookie_data = [

        ["Total Cookies", str(result["cookies"]["total"])],

        ["Secure Cookies", str(result["cookies"]["secure"])],

        ["HttpOnly Cookies", str(result["cookies"]["httponly"])],

        ["SameSite Cookies", str(result["cookies"]["samesite"])],

        ["Session Cookies", str(result["cookies"]["session"])]

    ]

    cookie_table = Table(
        cookie_data,
        colWidths=[170, 320]
    )

    cookie_table.setStyle(
        TableStyle([

            ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#DBEAFE")),

            ("GRID", (0,0), (-1,-1), 0.6, colors.grey),

            ("BOTTOMPADDING", (0,0), (-1,-1), 8),

            ("TOPPADDING", (0,0), (-1,-1), 8)

        ])
    )

    story.append(cookie_table)

    story.append(Spacer(1,0.30*inch))


    # ---------------------------------------------------
    # HTTP Methods
    # ---------------------------------------------------

    story.append(
        Paragraph(
            "HTTP Methods",
            heading_style
        )
    )

    http_rows = [

        ["Method", "Supported", "Status"]

    ]

    for method in result["http_methods"]:

        http_rows.append(

            [

                method["method"],

                "Yes" if method["supported"] else "No",

                str(method["status"])

            ]

        )

    http_table = Table(

        http_rows,

        colWidths=[120,120,180]

    )

    http_table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#2563EB")),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("BACKGROUND",(0,1),(-1,-1),colors.whitesmoke),

            ("GRID",(0,0),(-1,-1),0.6,colors.grey),

            ("BOTTOMPADDING",(0,0),(-1,-1),8),

            ("TOPPADDING",(0,0),(-1,-1),8),

            ("ALIGN",(0,0),(-1,-1),"CENTER")

        ])

    )

    story.append(http_table)

    story.append(Spacer(1,0.30*inch))


    # ---------------------------------------------------
    # robots.txt
    # ---------------------------------------------------

    story.append(

        Paragraph(

            "robots.txt",

            heading_style

        )

    )

    robots = result["robots"]

    robots_data = [

        ["Found", "Yes" if robots["found"] else "No"],

        ["URL", robots["url"]],

        ["Status Code", str(robots["status_code"])],

        ["Total Rules", str(robots["rules"])]

    ]

    robots_table = Table(

        robots_data,

        colWidths=[170,320]

    )

    robots_table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#DBEAFE")),

            ("GRID",(0,0),(-1,-1),0.6,colors.grey),

            ("BOTTOMPADDING",(0,0),(-1,-1),8),

            ("TOPPADDING",(0,0),(-1,-1),8)

        ])

    )

    story.append(robots_table)

    story.append(Spacer(1,0.30*inch))


    # ---------------------------------------------------
    # security.txt
    # ---------------------------------------------------

    story.append(

        Paragraph(

            "security.txt",

            heading_style

        )

    )

    sec = result["securitytxt"]

    security_data = [

        ["Found", "Yes" if sec["found"] else "No"],

        ["Location", sec["url"]],

        ["Status Code", str(sec["status_code"])],

        ["Security Contact", sec["contact"]],

        ["Encryption Key", sec["encryption"]],

        ["Preferred Languages", sec["preferred_languages"]],

        ["Expires", sec["expires"]]

    ]

    security_table = Table(

        security_data,

        colWidths=[170,320]

    )

    security_table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#DBEAFE")),

            ("GRID",(0,0),(-1,-1),0.6,colors.grey),

            ("BOTTOMPADDING",(0,0),(-1,-1),8),

            ("TOPPADDING",(0,0),(-1,-1),8)

        ])

    )

    story.append(security_table)

    story.append(Spacer(1,0.40*inch))

    # ---------------------------------------------------
    # Recommendations
    # ---------------------------------------------------

    story.append(
        Paragraph(
            "Recommendations",
            heading_style
        )
    )

    recommendations = result["risk"]["recommendations"]

    if recommendations:

        for item in recommendations:

            story.append(

                Paragraph(

                    f"• {item}",

                    normal_style

                )

            )

    else:

        story.append(

            Paragraph(

                "No recommendations. The website follows good security practices.",

                normal_style

            )

        )

    story.append(Spacer(1, 0.30 * inch))


    # ---------------------------------------------------
    # Disclaimer
    # ---------------------------------------------------

    story.append(

        Paragraph(

            "Disclaimer",

            heading_style

        )

    )

    story.append(

        Paragraph(

            "This report represents the security posture observed at the time of scanning. "
            "The assessment is automated and should not be considered a complete security audit. "
            "Security configurations may change after this report is generated.",

            normal_style

        )

    )

    story.append(Spacer(1, 0.30 * inch))


    # ---------------------------------------------------
    # Report Footer
    # ---------------------------------------------------

    footer_table = Table(

        [

            ["Web Security Analyzer v1.0"],

            ["Developed by Konireddy Manoj Kumar Reddy"],

            [f"Generated on {report['generated_date']} at {report['generated_time']}"]

        ],

        colWidths=[490]

    )

    footer_table.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#2563EB")),

            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke),

            ("GRID", (0,0), (-1,-1), 0.6, colors.grey),

            ("ALIGN", (0,0), (-1,-1), "CENTER"),

            ("FONTNAME", (0,0), (-1,-1), "Helvetica-Bold"),

            ("BOTTOMPADDING", (0,0), (-1,-1), 10),

            ("TOPPADDING", (0,0), (-1,-1), 10)

        ])

    )

    story.append(footer_table)

    story.append(Spacer(1, 0.20 * inch))


    # ---------------------------------------------------
    # Generate PDF
    # ---------------------------------------------------

    doc.build(story)

    return filename