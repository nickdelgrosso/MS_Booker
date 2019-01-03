from os import path
from datetime import datetime
import pandas as pd
from kanbancard import latex, extract_comments, check_for_nonunique_columns

data_filename = 'data/test.csv'
template_file = 'templates/card_template.tex'
build_dir = 'output2'
out_file = 'card_built.tex'
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
latex.pdflatex(tex=tex, output_dir=build_dir)
