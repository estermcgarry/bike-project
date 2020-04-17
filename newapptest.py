from flask import request
@app.route('/station/<station>/<weekday>', method=['POST'])
def getvalue():
    station = request.form["station"]
    #weekday = request.form["station"]
    return