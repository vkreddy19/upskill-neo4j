import threading, urllib3
import queue

urls_to_load = ["http://api.dataatwork.org/v1/jobs?offset=0&limit=500", "http://api.dataatwork.org/v1/jobs?offset=500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=1000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=1500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=2000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=2500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=3000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=3500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=4000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=4500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=5000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=5500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=6000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=6500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=7000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=7500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=8000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=8500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=9000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=9500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=10000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=10500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=11000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=11500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=12000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=12500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=13000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=13500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=14000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=14500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=15000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=15500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=16000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=16500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=17000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=17500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=18000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=18500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=19000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=19500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=20000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=20500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=21000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=21500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=22000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=22500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=23000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=23500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=24000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=24500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=25000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=25500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=26000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=26500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=27000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=27500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=28000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=28500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=29000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=29500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=30000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=30500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=31000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=31500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=32000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=32500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=33000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=33500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=34000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=34500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=35000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=35500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=36000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=36500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=37000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=37500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=38000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=38500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=39000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=39500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=40000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=40500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=41000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=41500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=42000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=42500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=43000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=43500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=44000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=44500&limit=500", "http://api.dataatwork.org/v1/jobs?offset=45000&limit=500", "http://api.dataatwork.org/v1/jobs?offset=45500&limit=500"
]

def read_url(url, queue):
    import requests
    data = requests.get(url)
    print('Fetched from %s' % (url))
    queue.put(data.json())

def fetch_parallel():
    result = queue.Queue()
    threads = [threading.Thread(target=read_url, args=(url, result)) for url in urls_to_load]
    for t in threads:
        t.start()
    for t in threads:
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
with open('jobs.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    while not res.empty():
        # print(res.get())
        temp = res.get()[:-1]
        dict_writer.writerows(temp)



