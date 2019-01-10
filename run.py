from flask import Flask, render_template, request, make_response
import pandas as pd
from io import BytesIO
from datetime import datetime
from uuid import uuid4
from kanbancard.card import df_to_card_pdf


app = Flask(__name__)


template_file = 'templates/card_template.tex'
with open(template_file) as f:
    template_tex = f.read()


@app.route('/')
def index():
    return render_template('landing.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    filename, csv_data = request.files['csv'].filename, request.files['csv'].read()
    df = pd.read_csv(BytesIO(csv_data), skiprows=[0])
    batch_id = str(uuid4())[:5].upper()
    date = datetime.now()
    pdf = df_to_card_pdf(template_tex=template_tex, df=df, filename=filename, batch_id=batch_id, date=date)

    response = make_response(pdf)
    response.headers['Content-Disposition'] = "inline; filename='booking.pdf"
    response.mimetype = 'application/pdf'
    return response


@app.route('/download_example', methods=['GET'])
def download_example():
    with open('./data/test.csv') as f:
        csv = f.read()
    response = make_response(csv)
    response.headers['Content-Disposition'] = "inline; filename='example_sequence.csv"
    response.mimetype = 'text/csv'
    return response


if __name__ == '__main__':
    app.run(debug=True)
