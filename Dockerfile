FROM python:3.6

RUN apt-get update
RUN apt-get install -y texlive-full
#RUN apt-get install xzdec
#RUN tlmgr init-usertree
#RUN tlmgr option repository ctan
#RUN tlmgr install latex
#\usepackage{dashrule}
#\usepackage{tikz}
#\usepackage{bbding}

COPY . /app
WORKDIR /app
RUN pip install .
RUN pip install gunicorn
EXPOSE 5000

CMD echo Starting Gunicorn.
#CMD python run.py
CMD gunicorn --bind 0.0.0.0:5000 card_app:app --workers 2