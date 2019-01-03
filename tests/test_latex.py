from kanbancard import latex
import tempfile


def test_latex_renderer():
    template = r"""
        \documentclass{article}
        \begin{document}
            My name is \VAR{name}, and I search for the \VAR{quest}.
        \end{document}
    """

    result = r"""
        \documentclass{article}
        \begin{document}
            My name is Sir Arthur, and I search for the Holy Grail.
        \end{document}
    """

    assert latex.render_templated_tex(template, name='Sir Arthur', quest="Holy Grail") == result


def test_pdflatex_runs(capfd):
    tex = r"""
        \documentclass{article}
        \begin{document}
            My name is Sir Arthur, and I search for the Holy Grail.
        \end{document}
    """
    latex.pdflatex(tex, output_dir=tempfile.tempdir)
    captured = capfd.readouterr()
    assert "Output written on" in captured.out