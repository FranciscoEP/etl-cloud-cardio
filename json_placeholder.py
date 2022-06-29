import requests
from datetime import timedelta
import json

from prefect import task, Flow
from prefect.schedules import IntervalSchedule

API = 'https://jsonplaceholder.typicode.com/posts/1'
schedule = IntervalSchedule(interval=timedelta(minutes=1))

@task(log_stdout=True, max_retries=3, retry_delay=timedelta(minutes=1))
def extract(url):
    print("Obtaining data from: ", url)
    response = requests.get(url)
    print("Status code: ", response.status_code)
    response = json.loads(response.text)
    with open('./transformed_data.json', 'w', encoding='utf-8') as f:
        json.dump(response, f, ensure_ascii=False, indent=4)


@task(log_stdout=True)
def transform(raw):
    print("Info: transforming raw data")
    return "title",raw['title']


@task(log_stdout=True)
def load(response):
    print("Load initialized")
    print(response)


with Flow("JSON Placeholder", schedule) as flow:
    raw = extract(API)
    transformed_data = transform(raw)
    load(transformed_data)

if __name__ == "__main__":
    flow.run()
