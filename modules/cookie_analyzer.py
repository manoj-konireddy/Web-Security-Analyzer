def analyze_cookies(cookies):

    total = len(cookies)

    secure = 0
    httponly = 0
    samesite = 0
    session = 0

    for cookie in cookies:

        if cookie.secure:
            secure += 1

        if "HttpOnly" in str(cookie._rest):
            httponly += 1

        if "SameSite" in str(cookie._rest):
            samesite += 1

        if cookie.expires is None:
            session += 1

    return {

        "total": total,

        "secure": secure,

        "httponly": httponly,

        "samesite": samesite,

        "session": session

    }