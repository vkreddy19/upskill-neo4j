import threading
import queue
import pandas as pd
import requests

urls_to_load = []
df = pd.read_csv("../data/filtered_jobs_data.csv")
for job_id in df.iloc[:,0]:
    urls_to_load.append((job_id, "http://api.dataatwork.org/v1/jobs/%s/related_jobs"%job_id))

#
def read_url(url, queue):
    data = requests.get(url[1])
    # print('Fetched from %s' % (url[1]))
    queue.put((url[0], data.json()))

import time
def fetch_parallel():
    result = queue.Queue()
    threads = [threading.Thread(target=read_url, args=(url, result)) for url in urls_to_load]
    for i, t in enumerate(threads):
        t.start()
        print(i)
        if i%200 ==0:
            time.sleep(1)
    for t in threads:
        print("join")
        t.join()
    return result

def fetch_sequencial():
    result = queue.Queue()
    for url in urls_to_load:
        read_url(url, result)
    return result

import csv
res = fetch_parallel()
keys = ["uuid","title","normalized_job_title","parent_uuid"]
with open('../data/related_jobs.csv', 'w', newline='') as output_file:
    csv_writer = csv.writer(output_file)
    while not res.empty():
        temp  = res.get()
        uuid = temp[0]
        temp2 = temp[1].get("related_job_titles", [])
        related_job_ids = ",".join([x.get("uuid") for x in temp2])
        csv_writer.writerow([uuid, related_job_ids])



