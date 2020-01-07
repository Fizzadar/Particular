from flask import render_template

from particular_admin.app import app


@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(405)
def error_401(error):
    return render_template('error.html', error=error), error.code
