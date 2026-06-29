SECURITY_HEADERS = [

    "Content-Security-Policy",

    "Strict-Transport-Security",

    "X-Content-Type-Options",

    "X-Frame-Options",

    "Referrer-Policy",

    "Permissions-Policy"

]


def check_security_headers(headers):

    result = []

    score = 0

    for header in SECURITY_HEADERS:

        present = header in headers

        if present:
            score += 1

        result.append({

            "name": header,

            "present": present

        })

    return {

        "score": score,

        "total": len(SECURITY_HEADERS),

        "headers": result

    }