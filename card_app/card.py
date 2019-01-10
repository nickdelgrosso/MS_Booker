from . import latex


def df_to_xcalibur_csv(df, bracket=4):
    """Returns an XCalibur-formatted csv as a string (with 'bracket' put in the header), given a pandas DataFrame."""
    return 'Bracket Type={}{}\n{}'.format(bracket, ',' * (df.shape[1] - 1), df.to_csv(index=False))


def df_to_card_pdf(template_tex, df, filename, batch_id, date):
    comments = dict([el.strip() for el in item.split(':')] for item in df['Comment'][0].split(','))
    samples = [row for _, row in df.iterrows()]
    tex = latex.render_templated_tex(template_tex, BatchID=batch_id, Date=date.strftime('%d.%m.%Y'), Filename=filename,
                                     Comments=comments, Samples=samples)
    pdf = latex.pdflatex(tex=tex)
    return pdf
