# Simple FastAPI server with root and parameterized endpoints
from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World from FastAPI!"}


@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello {name}!"}


def main():
    print("Starting FastAPI Hello World server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
