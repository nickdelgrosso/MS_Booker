from card_app import latex


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
    latex.pdflatex(tex)
    captured = capfd.readouterr()
    assert "Output written on" in captured.out


def test_pdflatex_returns_pdf_containing_text(capfd):
    tex = r"""
        \documentclass{article}
        \begin{document}
            My name is Sir Arthur, and I search for the Holy Grail.
        \end{document}
    """
    pdf = latex.pdflatex(tex)
    assert 'PDF' in pdf[:10].decode()