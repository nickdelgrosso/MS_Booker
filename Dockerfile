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

RUN apt-get install build-essential chrpath libssl-dev libxft-dev libfreetype6-dev libfreetype6 libfontconfig1-dev libfontconfig1 -y
RUN wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
RUN sudo tar xvjf phantomjs-2.1.1-linux-x86_64.tar.bz2 -C /usr/local/share/
RUN sudo ln -s /usr/local/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin/



COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

CMD echo Starting Gunicorn.
#CMD python run.py
CMD gunicorn --bind 0.0.0.0:5000 card_app:app --workers 2