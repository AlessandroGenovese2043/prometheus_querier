import os
from napa.querier.thread_querier import ThreadQuerier

os.environ["METRIC_ENDPOINT"] = "http://localhost:9090"
os.environ["CONF"] = "CONF_0"

if __name__ == "__main__":
    print("Start")
    # Init thread in order to do queries on prometheus
    thread = ThreadQuerier()
    print("Finish")
