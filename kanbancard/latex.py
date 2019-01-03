"""
Latex templating code, templated with Jinja2 and rendered with pdflatex.

Examples:
>>>with open(tex_filename) as f:
>>>    tex = f.read()
>>>tex = render_templated_tex(tex, **options)
>>>pdflatex(tex=tex, output_dir=output_dir)
"""

import os
import jinja2
import subprocess


def render_templated_tex(tex, **options):
    """
    Renders latex code template with data from the options dict, lookcing for \VAR{} and \BLOCK{} in the template.

    Arguments:
        -tex (str): the templated latex code to be filled in

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
        loader=jinja2.BaseLoader()
    )
    template = env.from_string(tex)
    rendered_tex = template.render(**options)
    return rendered_tex


def pdflatex(tex, output_dir='.'):
    """Call pdflatex, passing the 'tex' string to the program and putting rendered files in 'output_dir'."""
    subprocess.run(r'pdflatex -output-directory {dir}'.format(dir=output_dir), input=tex.encode())

