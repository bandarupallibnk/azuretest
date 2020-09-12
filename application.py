from setuptools import setup
from kajaas import app,celery
from flask import render_template,redirect,url_for

@app.route('/')
def index():
    return redirect(url_for('index.index'))


if __name__=='__main__':
    app.run(debug=True)
# setup(
#     name='kaja',
#     packages=['kaja'],
#     include_package_data=True,
#     install_requires=[
#         'flask',
#     ],
# )
