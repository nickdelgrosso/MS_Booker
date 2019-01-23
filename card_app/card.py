from io import BytesIO
from . import latex
from .models import Sequence
from . import utils


def df_to_xcalibur_csv(df, bracket=4):
    """Returns an XCalibur-formatted csv as a string (with 'bracket' put in the header), given a pandas DataFrame."""
    return 'Bracket Type={}{}\n{}'.format(bracket, ',' * (df.shape[1] - 1), df.to_csv(index=False))


def df_to_card_pdf(template_tex, sequence, post_fields=()):


    tex = latex.render_templated_tex(template_tex, Sequence=sequence, PostFields=post_fields)


    fig = utils.plot_gradient(sequence.gradient)
    figfile = BytesIO()
    fig.savefig(figfile, format='png')
    figfile.seek(0)
    pdf = latex.pdflatex(tex=tex, **{'gradient.png': figfile.read()})
    return pdf
