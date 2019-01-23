from io import BytesIO
from . import latex
from .models import Sequence
from . import utils


def df_to_xcalibur_csv(df, bracket=4):
    """Returns an XCalibur-formatted csv as a string (with 'bracket' put in the header), given a pandas DataFrame."""
    return 'Bracket Type={}{}\n{}'.format(bracket, ',' * (df.shape[1] - 1), df.to_csv(index=False))


def df_to_card_pdf(template_tex, df, filename, batch_id, date, lc_settings, gradient,
                   post_fields=['Tip Box', 'Concentration Measurement Method', 'Measured Concentration', 'Predicted Sample Amount (ng)', 'LC Used', 'MS Used']):

    comments = dict([el.strip() for el in item.split(':')] for item in df['Comment'][0].split(','))
    samples = [row for _, row in df.iterrows()]
    lc_settings.index = lc_settings.index.str.replace('reEquilibration', '')
    lc_settings = lc_settings.to_latex(bold_rows=True, column_format='rccc', na_rep='', index_names=False)

    seq = Sequence(
        filename=filename,
        date=date,
        lc_settings=lc_settings,
        gradient=gradient,
        comments=comments,
        samples=samples,
        table=df,
    )

    run_time = seq.run_time

    tex = latex.render_templated_tex(template_tex, BatchID=batch_id, Date=date.strftime('%d.%m.%Y'), Filename=filename,
                                     Comments=comments, Samples=samples, LC_Settings=lc_settings, Gradient=gradient,
                                     PostFields=post_fields, RunTime=run_time)


    fig = utils.plot_gradient(gradient)
    figfile = BytesIO()
    fig.savefig(figfile, format='png')
    figfile.seek(0)
    pdf = latex.pdflatex(tex=tex, **{'gradient.png': figfile.read()})
    return pdf
