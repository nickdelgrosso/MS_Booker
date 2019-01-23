from os import path
from io import BytesIO
from datetime import datetime
from uuid import uuid4
import zipfile
from flask import render_template, request, make_response
import pandas as pd
from XCaliburMethodReader import load_lc_data, get_lc_gradient, get_lc_settings
from .card import df_to_card_pdf
from . import latex
from . import app
from .forms import CleaningForm
from .models import Sequence

template_file = path.join(app.root_path, 'templates', 'card_template.tex')
cleaning_template_file = path.join(app.root_path, 'templates', 'cleaning_card_template.tex')


@app.route('/')
def index():
    cleaning_form = CleaningForm()
    return render_template('landing.html', cleaning_form=cleaning_form)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    filename, csv_data = request.files['csv'].filename, request.files['csv'].read()
    df = pd.read_csv(BytesIO(csv_data), skiprows=[0])
    batch_id = str(uuid4())[:5].upper()
    date = datetime.now()

    method_filename, method_data = request.files['method'].filename, request.files['method'].read()
    lc_data = load_lc_data(BytesIO(method_data))
    lc_settings = get_lc_settings(lc_data)
    gradient = get_lc_gradient(lc_data)

    with open(template_file) as f:
        template_tex = f.read()


    seq = Sequence(
        filename=filename,
        date=date,
        lc_settings=lc_settings,
        gradient=gradient,
        comments=dict([el.strip() for el in item.split(':')] for item in df['Comment'][0].split(',')),
        samples=[row for _, row in df.iterrows()],
        table=df,
    )

    post_fields = ['Tip Box', 'Concentration Measurement Method', 'Measured Concentration', 'Predicted Sample Amount (ng)', 'LC Used', 'MS Used']
    pdf = df_to_card_pdf(template_tex=template_tex, sequence=seq, post_fields=post_fields)

    response = make_response(pdf)
    response.headers['Content-Disposition'] = "inline; filename='booking.pdf"
    response.mimetype = 'application/pdf'
    return response


@app.route('/download_example', methods=['GET'])
def download_example():
    f = BytesIO()
    with zipfile.ZipFile(f, mode='w') as zip:
        zip.write(path.join(app.root_path, 'data', 'test.csv'), arcname='test.csv')
        zip.write(path.join(app.root_path, 'data', 'test.meth'), arcname='test.meth')
    f.seek(0)

    response = make_response(f.read())
    response.headers['Content-Disposition'] = "inline; filename='example_files.zip"
    response.mimetype = 'application/zip'
    return response


@app.route('/cleaning_card', methods=['GET', 'POST'])
def upload_cleaning_card():
    form = CleaningForm()
    date = datetime.now().strftime('%d.%m.%Y')

    with open(cleaning_template_file) as f:
        tex = latex.render_templated_tex(tex=f.read(), form=form, Date=date, PostFields=['Inject Time (ms)', 'NL', 'Calibration', 'Transmission Score'])

    pdf = latex.pdflatex(tex=tex)
    response = make_response(pdf)
    response.headers['Content-Disposition'] = "inline; filename='cleaning.pdf"
    response.mimetype = 'application/pdf'
    return response