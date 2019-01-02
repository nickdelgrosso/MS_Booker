from os import path
import pandas as pd
from kanbancard import latex


options = {
	'ProjectName': 'NJJF Rab10 Occupancy',
	'BatchID': 1,
}

data_filename = 'data/test.csv'
options['Filename'] = path.basename(data_filename)


df = pd.read_csv(data_filename, skiprows=[0])
df.columns = [col[3:] if col[0] == 'L' and col[1].isdigit() else col.replace(' ', '') for col in df.columns]

for col in ['ProjectID', 'Researcher']:
	assert df[col].nunique() == 1
	options[col] = df.iloc[0][col]
options['df'] = df

assert df['Comment'].nunique() == 1
comments = {}
for comment in df.iloc[0]['Comment'].split(','):
	key, val = comment.split(':')
	comments[key.lstrip().rstrip()] = val.lstrip().rstrip()
options['Comment'] = comments

for key, value in options.items():
	if isinstance(value, str):
		options[key] = value.replace('_', r'\_')

template_file = 'templates/card_template.tex'
template = latex.get_latex_template(template_file)

build_d, out_file = 'output', 'card_built.tex'
renderer_template = template.render(**options)
latex.write(renderer_template, filename=out_file, directory=build_d)
latex.pdflatex(out_file, output_dir=build_d)

#
#
#
