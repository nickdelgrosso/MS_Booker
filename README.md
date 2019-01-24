# MS_Booker
A simple web app for booking mass spec machines


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
