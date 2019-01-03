from os import path
from datetime import datetime
import pandas as pd
from kanbancard import latex, extract_comments, check_for_nonunique_columns
from flask import Flask, render_template, request, redirect, url_for
from wtforms import SubmitField, StringField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict


app = Flask(__name__)
app.secret_key = b'adfajfakfjlafj;fndjkanfklj'
app.config['UPLOAD_FOLDER'] = './tmp'

csrf = CSRFProtect(app)

class SequenceForm(FlaskForm):
	csv = FileField()
	submit = SubmitField('Sign In')


@app.route('/', methods=['GET', 'POST'])
def index():
	form = SequenceForm()
	return render_template('landing.html', form=form)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	form = SequenceForm()#CombinedMultiDict((request.files, request.form)))
	if form.validate_on_submit():
		# return str(form.csv.data.content_length)

		form.csv.data.save('testdata.txt')
		return str(form.csv.data.filename)
	else:
		print('not validated')
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