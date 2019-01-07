from os import path
from datetime import datetime
import pandas as pd
from kanbancard import latex, extract_comments, check_for_nonunique_columns
from flask import Flask, render_template, request, make_response
from io import BytesIO
from uuid import uuid4
from PyPDF2 import PdfFileMerger


app = Flask(__name__)


@app.route('/')
def index():
	return render_template('landing.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
	filename, csv_data = request.files['csv'].filename, request.files['csv'].read()
	pdf = generate_pdfs(data_filename=filename, csv_data=csv_data)
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


def generate_pdfs(data_filename, csv_data, template_file='templates/card_template.tex'):

	# Read / Validate CSV Sequence File
	if 'csv' in path.splitext(data_filename)[1]:
		batch_name = str(uuid4()).split('-')[0]
		df = pd.read_csv(BytesIO(csv_data), skiprows=[0])
		batches = {batch_name: df}
	else:
		excel_reader = pd.ExcelFile(BytesIO(csv_data))
		batches = {sheet_name: excel_reader.parse(sheet_name, skiprows=[0]) for sheet_name in excel_reader.sheet_names}

	pdf_merger = PdfFileMerger()
	for batch_name, df in batches.items():

		metadata = dict([el.strip().lstrip() for el in item.split(':')] for item in df['Comment'][0].split(','))

		# Render to PDF Card via Latex
		options = {
			'Project': metadata['Project'],
			'BatchID': batch_name,
			'Date': datetime.now().strftime('%d.%m.%Y'),
			'Filename': path.basename(data_filename),
			'df': df,
			'Comments': metadata,
			'Researcher': metadata['Researcher'],
		}


		with open(template_file) as f:
			tex = latex.render_templated_tex(tex=f.read(), **options)


		pdf = latex.pdflatex(tex=tex)
		pdf_merger.append(BytesIO(pdf))

	with BytesIO() as f:
		pdf_merger.write(f)
		f.seek(0)
		return f.read()



if __name__ == '__main__':
	app.run(debug=True)