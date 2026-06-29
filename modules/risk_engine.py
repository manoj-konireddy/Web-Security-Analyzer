def calculate_risk(result):

    score = 100

    recommendations = []

    # -------------------------
    # Security Headers
    # -------------------------

    headers = result["security_headers"]

    missing_headers = (
        headers["total"] -
        headers["score"]
    )

    score -= missing_headers * 5

    if missing_headers > 0:

        recommendations.append(
            "Add missing security headers."
        )

    # -------------------------
    # SSL
    # -------------------------

    ssl = result["ssl"]

    if not ssl["enabled"]:

        score -= 25

        recommendations.append(
            "Enable HTTPS with a valid SSL certificate."
        )

    elif not ssl["valid"]:

        score -= 15

        recommendations.append(
            "Renew the SSL certificate."
        )

    # -------------------------
    # Cookies
    # -------------------------

    cookies = result["cookies"]

    if cookies["total"] > 0:

        if cookies["secure"] < cookies["total"]:

            score -= 5

            recommendations.append(
                "Use Secure cookies."
            )

        if cookies["httponly"] < cookies["total"]:

            score -= 5

            recommendations.append(
                "Use HttpOnly cookies."
            )

    # -------------------------
    # robots.txt
    # -------------------------

    if not result["robots"]["found"]:

        score -= 2

        recommendations.append(
            "Add a robots.txt file."
        )

    # -------------------------
    # security.txt
    # -------------------------

    if not result["securitytxt"]["found"]:

        score -= 3

        recommendations.append(
            "Publish a security.txt file."
        )

    if score < 0:

        score = 0

    # -------------------------
    # Risk Level
    # -------------------------

    if score >= 90:

        risk = "Excellent"

    elif score >= 75:

        risk = "Low"

    elif score >= 50:

        risk = "Medium"

    else:

        risk = "High"

    return {

        "score": score,

        "risk": risk,

        "recommendations": recommendations

    }