from os import path
from io import BytesIO
from datetime import datetime
import zipfile
from flask import render_template, request, make_response, redirect, url_for, flash, get_flashed_messages
from . import latex
from . import app
from . import utils
from .forms import CleaningForm
from .models import Sequence, SequenceFileError, MethodFileError

template_file = path.join(app.root_path, 'templates', 'card_template.tex')
cleaning_template_file = path.join(app.root_path, 'templates', 'cleaning_card_template.tex')


@app.route('/')
@app.route('/index')
def index():
    cleaning_form = CleaningForm()
    return render_template('landing.html', cleaning_form=cleaning_form)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    filename, csv_data = request.files['csv'].filename, request.files['csv'].read()
    method_filename, method_data = request.files['method'].filename, request.files['method'].read()

    with open(template_file) as f:
        template_tex = f.read()

    try:
        sequence = Sequence.from_xcalibur_csv_and_method(
            filename=filename, csv_data=csv_data, method_filename=method_filename, method_data=method_data,
        )
    except (SequenceFileError, MethodFileError) as e:
        flash("{}: {}\nPlease submit a new file and generate the pdf again.".format(type(e).__name__, e.args[0]))
        return redirect(url_for('index'))
    except Exception as e:
        flash("Unexpected Error: {}: {}.".format(type(e).__name__, e.args[0]))

    post_fields = ['Tip Box Name', '',  # Putting a space will make a double-width column
                   'Concentration Measurement Method', '',
                   'Concentration', 'Sample Amount (ng)',
                   'LC Used', 'MS Used']

    tex = latex.render_templated_tex(template_tex, Sequence=sequence, PostFields=post_fields)
    fig = utils.plot_gradient(sequence.gradient)
    pdf = latex.pdflatex(tex=tex, figures={'gradient.png': fig})

    response = make_response(pdf)
    response.headers['Content-Disposition'] = "inline; filename='booking.pdf"
    response.mimetype = 'application/pdf'
    return response


@app.route('/download_example', methods=['GET'])
def download_example():
    f = BytesIO()
    with zipfile.ZipFile(f, mode='w') as zip:
        zip.write(path.join(app.root_path, 'data', 'test_sequence.csv'), arcname='test_sequence.csv')
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


@app.errorhandler(500)
@app.errorhandler(400)
@app.errorhandler(404)
def page_not_found(e):
    flash(str(e))
    return redirect(url_for('index'))
