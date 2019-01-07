from flask import Flask, render_template, request, make_response
import kanbancard

app = Flask(__name__)

template_file = 'templates/card_template.tex'
csv_save_dir = 'out_files'


@app.route('/')
def index():
	return render_template('landing.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
	filename, csv_data = request.files['csv'].filename, request.files['csv'].read()
	pdf = kanbancard.generate_pdfs(data_filename=filename, csv_data=csv_data, csv_save_dir=csv_save_dir, template_file=template_file)
	response = make_response(pdf)
	response.headers['Content-Disposition'] = "inline; filename='booking.pdf"
	response.mimetype = 'application/pdf'
	return response


@app.route('/download_example', methods=['GET'])
def download_example():
	with open('./data/test.xlsx', 'rb') as f:
		csv = f.read()
	response = make_response(csv)
	response.headers['Content-Disposition'] = "inline; filename='example_sequence.xlsx"
	response.mimetype = 'application/vnd.ms-excel'
	return response


if __name__ == '__main__':
	app.run(debug=True)
