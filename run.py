from os import path
from datetime import datetime
import pandas as pd
from kanbancard import latex, extract_comments, check_for_nonunique_columns
from flask import Flask, render_template, request, send_file, make_response
from io import StringIO, BytesIO


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('landing.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		filename, csv_data = request.files['csv'].filename, request.files['csv'].read()
		pdf = generate_pdf(data_filename=filename, csv_data=csv_data)
		response = make_response(pdf)
		response.headers['Content-Disposition'] = "inline; filename='booking.pdf"
		response.mimetype = 'application/pdf'
		return response

	else:
		return 'not validated'


def generate_pdf(data_filename, csv_data, project_name='NJJF Rab10 Occupancy', template_file='templates/card_template.tex'):

	# Read / Validate CSV Sequence File
	df = pd.read_csv(BytesIO(csv_data), skiprows=[0])
	# return df._repr_html_()
	df.columns = [col[3:] if col[0] == 'L' else col for col in df.columns]
	check_for_nonunique_columns(df, columns=['Project ID', 'Researcher', 'Comment'])

	# Render to PDF Card via Latex
	options = {
		'Project': project_name,
		'BatchID': 1,
		'Date': datetime.now().strftime('%d.%m.%Y'),
		'Filename': path.basename(data_filename),
		'df': df,
		'Comment': extract_comments(df['Comment'][0]),
	}

	with open(template_file) as f:
		tex = latex.render_templated_tex(tex=f.read(), **options)
	pdf_str = latex.pdflatex(tex=tex)
	return pdf_str


if __name__ == '__main__':
	app.run(debug=True)