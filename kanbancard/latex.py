"""
Latex templating code, templated with Jinja2 and rendered with pdflatex.

modified from http://eosrei.net/articles/2015/11/latex-templates-python-and-jinja2-generate-pdfs
"""

import os
import jinja2
import subprocess

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


def pdflatex(tex, output_dir='.'):
    subprocess.run(r'pdflatex -output-directory {dir}'.format(dir=output_dir), input=tex.encode())


def render_to_pdf(tex_filename, ouput_filename, output_dir, options):
    """Do full rendering pipeline, passing options dict to the jinja2 latex template and building with pdflatex."""
    template = get_latex_template(tex_filename)
    renderer_template = template.render(**options)
    pdflatex(tex=renderer_template, output_dir=output_dir)