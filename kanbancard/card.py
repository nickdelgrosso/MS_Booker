from os import path
from datetime import datetime
from uuid import uuid4
from . import latex


def df_to_xcalibur_csv(df, bracket=4):
    """Returns an XCalibur-formatted csv as a string (with 'bracket' put in the header), given a pandas DataFrame."""
    return 'Bracket Type={}{}\n{}'.format(bracket, ',' * (df.shape[1] - 1), df.to_csv(index=False))


def generate_pdfs(df, filename, template_file):

    # Read / Validate CSV Sequence File
    batch_name = str(uuid4()).split('-')[0]

    metadata = dict([el.strip().lstrip() for el in item.split(':')] for item in df['Comment'][0].split(','))

    # Render to PDF Card via Latex
    options = {
        'Project': metadata['Project'],
        'BatchID': batch_name,
        'Date': datetime.now().strftime('%d.%m.%Y'),
        'Filename': path.basename(filename),
        'df': df,
        'Comments': metadata,
        'Researcher': metadata['Researcher'],
    }

    with open(template_file) as f:
        tex = latex.render_templated_tex(tex=f.read(), **options)

    pdf = latex.pdflatex(tex=tex)
    return pdf
