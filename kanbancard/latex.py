"""
Latex templating code, templated with Jinja2 and rendered with pdflatex.
"""

import os
import jinja2
import subprocess

def fill_latex_template(tex_filename, **options):
    """
    Renders a latex file template with data from the options dict, lookcing for \VAR{} and \BLOCK{} in the template.

    Approach taken from http://eosrei.net/articles/2015/11/latex-templates-python-and-jinja2-generate-pdfs
    """
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
    template = env.get_template(tex_filename)
    rendered_tex = template.render(**options)
    return rendered_tex


def pdflatex(tex, output_dir='.'):
    subprocess.run(r'pdflatex -output-directory {dir}'.format(dir=output_dir), input=tex.encode())


def render_to_pdf(tex_filename, output_dir, options):
    """Do full rendering pipeline, passing options dict to the jinja2 latex template and building with pdflatex."""
    tex = fill_latex_template(tex_filename, **options)
    pdflatex(tex=tex, output_dir=output_dir)