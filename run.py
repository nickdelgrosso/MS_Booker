# modified from http://eosrei.net/articles/2015/11/latex-templates-python-and-jinja2-generate-pdfs

import os
import shutil
import jinja2

latex_jinja_env = jinja2.Environment(
	block_start_string='\BLOCK{',
	block_end_string='}',
	variable_start_string='\VAR{',
	variable_end_string='}',
	comment_start_string='\#{',
	comment_end_string='}',
	line_statement_prefix='%%',
	line_comment_prefix='%#',
	trim_blocks=True,
	autoescape=False,
	loader=jinja2.FileSystemLoader(os.path.abspath('.'))
)


template_file = 'templates/card_template.tex'
template = latex_jinja_env.get_template(template_file)
options = {
	'ProjectName': 'NJJF Rab10 Occupancy',
	'Researcher': 'Oezge Karayel',
	'ProjectID': '0170918AsJa',
	'BatchID': 1,
	'Filename': '832n_OsKa_K6028.dfaf.csv',
	'Comments': "LC: Easy, Column: 50cm 75um i.d. 1.8um C18, MS: QX-Series, MSMethod: DIA",
	'rows': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'],
}

comments = {}
for comment in options['Comments'].split(','):
	key, val = comment.split(':')
	comments[key.lstrip().rstrip()] = val.lstrip().rstrip()
options['Comments'] = comments

for key, value in options.items():
	if isinstance(value, str):
		options[key] = value.replace('_', r'\_')



renderer_template = template.render(**options)


build_d = 'output'
if not os.path.exists(build_d):  # create the build directory if not existing
	os.makedirs(build_d)

out_file = "{}_built".format(template_file)
with open(out_file+'.tex', "w") as f:  # saves tex_code to outpout file
	f.write(renderer_template)


os.system('pdflatex -output-directory {} {}'.format(os.path.realpath(build_d), os.path.realpath(out_file + '.tex')))

