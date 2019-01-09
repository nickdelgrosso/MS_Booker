from flask import Flask, render_template, request, make_response
import pandas as pd
from io import BytesIO
import kanbancard


app = Flask(__name__)

template_file = 'templates/card_template.tex'


@app.route('/')
def index():
    return render_template('landing.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    filename, csv_data = request.files['csv'].filename, request.files['csv'].read()
    df = pd.read_csv(BytesIO(csv_data), skiprows=[0])
    metadata = dict([el.strip() for el in item.split(':')] for item in df['Comment'][0].split(','))

    pdf = kanbancard.generate_card_pdf(
        template_file=template_file,
        sequence_filename=filename,
        df=df,
        comments=metadata,
    )

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
