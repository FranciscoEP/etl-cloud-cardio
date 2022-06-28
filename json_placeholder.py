import requests
from prefect import task, Flow

API = 'https://jsonplaceholder.typicode.com/posts'


@task
def extract(url):
    response = requests.get(url)
    response = response.json()
    return response


@task
def load(response):
    print([data["title"] for data in response])


with Flow("JSON Placeholder") as flow:
    raw = extract(API)
    load(raw)

if __name__ == "__main__":
    flow.run()
