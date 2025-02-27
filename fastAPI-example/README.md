## Getting Started

### Set Working Directory
Make sure to set your working directory to `fastAPI-example`:
```sh
cd /C:/Users/henva/Desktop/FireGuard/fastAPI-example
```

### Installation
To install the necessary dependencies, use `poetry`:
```sh
poetry install
```

### Running the Application
Change directory to `scripts` and in terminal, run:
```sh
cd scripts
poetry run uvicorn main:app --reload
```

### Testing with Postman

In Postman, it's possible to test the GET and POST requests with ease. Just connect to the IP address where Uvicorn is running. By default, it is `127.0.0.1:8000`.