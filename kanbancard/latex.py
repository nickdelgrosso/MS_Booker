"""
Latex templating code, templated with Jinja2 and rendered with pdflatex.

modified from http://eosrei.net/articles/2015/11/latex-templates-python-and-jinja2-generate-pdfs
"""

import os
import jinja2

def get_latex_template(tex_filename):
    env = jinja2.Environment(
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
    return env.get_template(tex_filename)


def write(template, filename, directory='output2'):
    if not os.path.exists(directory):  # create the build directory if not existin
        os.mkdir(directory)

    with open(directory + '/' + filename, "w") as f:  # saves tex_code to outpout file
        f.write(template)


def pdflatex(tex_filename, output_dir='.'):
    os.system(r'pdflatex -output-directory {dir} {dir}/{file}'.format(dir=output_dir, file=tex_filename))


def render_to_pdf(tex_filename, ouput_filename, output_dir, options):
    """Do full rendering pipeline, passing options dict to the jinja2 latex template and building with pdflatex."""
    template = get_latex_template(tex_filename)
    renderer_template = template.render(**options)
    write(renderer_template, filename=ouput_filename, directory=output_dir)
    pdflatex(ouput_filename, output_dir=output_dir)