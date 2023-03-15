from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html', os=os, app=app)


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('file')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))


@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        filenames = request.form.getlist('filename')
        dataframes = []
        for filename in filenames:
            if filename.endswith('.csv'):
                df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            elif filename.endswith('.xlsx'):
                df = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            dataframes.append(df)
        # perform data processing on dataframes
        result = pd.concat(dataframes)
        # render template with data
        return render_template('data.html', data=result.to_html(index=False))


if __name__ == '__main__':
    app.run(debug=True)
