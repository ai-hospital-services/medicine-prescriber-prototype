# medicine-prescriber-prototype

[![Build](https://github.com/ai-hospital-services/medicine-prescriber-prototype/actions/workflows/build.yml/badge.svg)](https://github.com/ai-hospital-services/medicine-prescriber-prototype/actions/workflows/build.yml)
[![CodeCov](https://codecov.io/gh/ai-hospital-services/medicine-prescriber-prototype/branch/main/graph/badge.svg)](https://codecov.io/gh/ai-hospital-services/medicine-prescriber-prototype)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/github/license/ai-hospital-services/medicine-prescriber-prototype)](/LICENSE)


> Medicine prescriber prototype for AI-HOSPITAL.SERVICES


![](media/prototype1-demo-recording-1.gif)

Table of Contents:
- [medicine-prescriber-prototype](#medicine-prescriber-prototype)
	- [Built With](#built-with)
	- [Getting Started](#getting-started)
		- [Prerequisites](#prerequisites)
		- [Setup backend api](#setup-backend-api)
		- [Run locally](#run-locally)
		- [Deployment](#deployment)
	- [Authors](#authors)
	- [🤝 Contributing](#-contributing)
	- [Show your support](#show-your-support)
	- [Acknowledgments](#acknowledgments)
	- [📝 License](#-license)

## Built With

- Flutter v3
- Python v3.9.14 & Flask v2.2.2
- MongoDB v6.0.1
- Docker
- Kubernetes & Helm chart
- Tensorflow v2.10.0


## Getting Started

To get a local copy up and running, follow these simple example steps.

### Prerequisites
- Install python 3.9.13: https://www.python.org/downloads/release/python-3913/
- Install docker desktop: https://docs.docker.com/get-docker/
- Install local kubernetes by docker desktop: https://docs.docker.com/desktop/kubernetes/
- Install helm: https://helm.sh/docs/intro/install/
- Install gcloud cli: https://cloud.google.com/sdk/docs/install

### Setup backend api
```sh
# change directory
cd backend/api

# create a virtual environment
# assuming you have "python3 --version" = "Python 3.9.13" installed in the current terminal session
python3 -m venv ./venv

# activate virtual environment
# for macos or linux
source ./venv/bin/activate
# for windows
.\venv\Scripts\activate

# upgrade pip
python -m pip install --upgrade pip

# install python dependencies
pip install -r ./requirements.txt -r ./requirements_dev.txt

# lint python code
pylint .
```

### Run locally
1. Run the flask app:
```sh
# change directory
cd backend

# argument --debug-mode = true or false (default) to enable debug mode logging
FLASK_DEBUG=1 python -m api.app --debug-mode true --port 8080

# curl to hit backend api
curl http://localhost:8080
>>> Welcome to backend api!
```

2. Or, build and run in docker container:
```sh
# change directory
cd backend/api

# build docker image
# --build-arg FLASK_DEBUG = debug mode for flask - 1 (default) or 0
# --build-arg MONGODB_URL = mongodb connection url - "mongodb://localhost:27017/" (default)
# --build-arg TENANT_DOMAIN = oauth2 tenant domain
# --build-arg REDIRECT_URL = oauth2 redirect url
# --build-arg TENANT_DOMAIN = oauth2 tenant domain
# --build-arg CLIENT_ID = oauth2 client id
# --build-arg CLIENT_SECRET = oauth2 client secret
docker build \
	--build-arg FLASK_DEBUG="1" \
	--build-arg MONGODB_URL="<MONGODB_URL>"
	--build-arg TENANT_DOMAIN="<TENANT DOMAIN>"
	--build-arg REDIRECT_URL="<REDIRECT URL>"
	--build-arg CLIENT_ID="<CLIENT ID>"
	--build-arg CLIENT_SECRET="<CLIENT SECRET>"
	-t ai-hospital-services:api .

# run docker image
docker run -it -p 8080:80 --name backendapi ai-hospital-services:api api --debug-mode true --port 80

### Usage


### Run tests
```sh
# change directory
cd backend

# run unit tests
pytest -v --cov=api
```

### Deployment



## Authors

👤 **Ankur Soni**

- [![Github](https://img.shields.io/github/followers/ankursoni?style=social)](https://github.com/ankursoni)
- [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/ankursoniji)
- [![Twitter](https://img.shields.io/twitter/url/https/twitter.com/fold_left.svg?style=social&label=Follow%20%40ankursoniji)](https://twitter.com/ankursoniji)


## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

Feel free to check the [issues page](../../issues/).


## Show your support

Give a ⭐️ if you like this project!


## Acknowledgments



## 📝 License

This project is [Apache](./LICENSE) licensed.
