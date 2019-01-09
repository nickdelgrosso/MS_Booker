import os
from os import path
from datetime import datetime
import pandas as pd
from . import latex
from io import BytesIO
from uuid import uuid4


def generate_pdfs(data_filename, csv_data, csv_save_dir, template_file):

    # Read / Validate CSV Sequence File
    batch_name = str(uuid4()).split('-')[0]
    df = pd.read_csv(BytesIO(csv_data), skiprows=[0])
    pre_header = csv_data.splitlines()[0].decode()

    metadata = dict([el.strip().lstrip() for el in item.split(':')] for item in df['Comment'][0].split(','))

    # Render to PDF Card via Latex
    options = {
        'Project': metadata['Project'],
        'BatchID': batch_name,
        'Date': datetime.now().strftime('%d.%m.%Y'),
        'Filename': path.basename(data_filename),
        'df': df,
        'Comments': metadata,
        'Researcher': metadata['Researcher'],
    }


    with open(template_file) as f:
        tex = latex.render_templated_tex(tex=f.read(), **options)

    if not path.exists(csv_save_dir):
        os.mkdir(csv_save_dir)

    new_filename = "{}_{}.csv".format(path.join(csv_save_dir, path.splitext(path.basename(data_filename))[0]), batch_name)
    with open(new_filename, 'w') as f:
        f.write(pre_header + '\n')
        df.to_csv(f, index_label=False, index=False)


    pdf = latex.pdflatex(tex=tex)
    return pdf
