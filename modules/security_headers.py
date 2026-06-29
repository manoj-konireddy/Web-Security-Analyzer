SECURITY_HEADERS = {
    "Content-Security-Policy": "Prevents Cross-Site Scripting (XSS)",
    "Strict-Transport-Security": "Forces HTTPS connections",
    "X-Content-Type-Options": "Prevents MIME sniffing",
    "X-Frame-Options": "Prevents Clickjacking attacks",
    "Referrer-Policy": "Controls referrer information",
    "Permissions-Policy": "Restricts browser capabilities"
}


def analyze_security_headers(headers):

    results = []

    score = 0

    for header, purpose in SECURITY_HEADERS.items():

        present = header in headers

        if present:
            score += 1

        results.append({
            "header": header,
            "present": present,
            "purpose": purpose
        })

    percentage = round(score / len(SECURITY_HEADERS) * 100)

    return {
        "score": score,
        "total": len(SECURITY_HEADERS),
        "percentage": percentage,
        "headers": results
    }