from io import BytesIO
from . import latex
from .models import Sequence
from . import utils


def df_to_card_pdf(template_tex, sequence: Sequence, post_fields=()):
    tex = latex.render_templated_tex(template_tex, Sequence=sequence, PostFields=post_fields)
    fig = utils.plot_gradient(sequence.gradient)
    pdf = latex.pdflatex(tex=tex, figures={'gradient.png': fig})
    return pdf
