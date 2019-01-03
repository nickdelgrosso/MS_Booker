from os import path
from datetime import datetime
import pandas as pd
from kanbancard import latex, extract_comments, check_for_nonunique_columns
from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('landing.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		return request.files['csv'].read()

	else:
		return 'not validated'


def tbd():

	data_filename = 'data/test.csv'
	template_file = 'templates/card_template.tex'
	project_name = 'NJJF Rab10 Occupancy'

	# Read / Validate CSV Sequence File
	df = pd.read_csv(data_filename, skiprows=[0])
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
	pdf = latex.pdflatex(tex=tex)
	with open('./card.pdf', 'wb')as f:
		f.write(pdf)


if __name__ == '__main__':
	app.run(debug=True)