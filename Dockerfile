FROM python:3.6

RUN apt-get update
RUN apt-get install -y texlive-full  # This works, but it is massive (4.5 GB).
#RUN apt-get install xzdec
#RUN tlmgr init-usertree
#RUN tlmgr option repository ctan
#RUN tlmgr install latex
#\usepackage{dashrule}
#\usepackage{tikz}
#\usepackage{bbding}

RUN pip install gunicorn
EXPOSE 5000

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

CMD echo Starting Gunicorn.
#CMD python run.py
CMD gunicorn --bind 0.0.0.0:5000 card_app:app --workers 2