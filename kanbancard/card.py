from datetime import datetime
from uuid import uuid4
from . import latex
from collections import namedtuple


Sample = namedtuple('Sample', 'Type Position')


def df_to_xcalibur_csv(df, bracket=4):
    """Returns an XCalibur-formatted csv as a string (with 'bracket' put in the header), given a pandas DataFrame."""
    return 'Bracket Type={}{}\n{}'.format(bracket, ',' * (df.shape[1] - 1), df.to_csv(index=False))


def generate_card_pdf(template_file, sequence_filename, comments, samples):
    # Render to PDF Card via Latex
    batch_id = str(uuid4()).split('-')[0]
    date = datetime.now().strftime('%d.%m.%Y')

    with open(template_file) as f:
        tex = f.read()
    tex = latex.render_templated_tex(tex, BatchID=batch_id, Date=date, Filename=sequence_filename, Comments=comments, Samples=samples)

    pdf = latex.pdflatex(tex=tex)
    return pdf
