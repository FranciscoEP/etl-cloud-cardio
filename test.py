
from prefect import task, Flow


@task
def load():
    print("Task initialized")


with Flow("Testing framework") as flow:
    load()

if __name__ == "__main__":
    flow.run()
