# MS_Booker
A simple web app for booking mass spec machines

Now it has a webpage!  Go to https://nickdelgrosso.github.io/MS_Booker/ to see this readme in more detail. 

![Kanban](https://kanbanize.com/blog/wp-content/uploads/2018/09/Spotify-Kanban-IT-operations-board.png)

## Installation

with Docker:
```
docker-compose build
```

without Docker, using Conda:
```
conda create --name msbookedr python=3.6
conda activate msbooker
git clone https://github.com/nickdelgrosso/MS_Booker
cd MS_Booker
python setup.py install
```

## Run

with Docker:
```
docker-compose up
```

without Docker:
```
cd MS_Booker
conda activate msbooker
python run.py
```
