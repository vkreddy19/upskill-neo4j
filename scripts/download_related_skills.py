#!/usr/bin/python

import httpx
import asyncio
import pandas as pd
import time
async def get_async(url):
    async with httpx.AsyncClient() as client:
        return await client.get(url, timeout=160.0)

async def launch():
    resps = await asyncio.gather(*map(get_async, urls))
    return resps


urls = []

base_url = "http://api.dataatwork.org/v1/jobs/%s/related_skills"
df = pd.read_csv("../data/filtered_jobs_data.csv")
result = []
cache = {}

for index, row in df.iterrows():
    urls.append(base_url%row[0])
    if index%50 == 0:
        if urls:
            print(index, len(urls))
            data = asyncio.run(launch())
            for res in data:
                if res.status_code == 200:
                    res_json = res.json()
                    for skill in res_json.get('skills'):
                        skill['job_uuid'] = (res_json.get('job_uuid'))
                        result.append(skill)
            if result:
                df2 = pd.DataFrame(result)
                df2.to_csv("../data/job_related_skills.csv",  mode='a', header=False, index=False)
                result = []
        urls = []
        time.sleep(30)

if urls:
    print(len(urls), "last")
    data = asyncio.run(launch())
    for res in data:
        if res.status_code == 200:
            res_json = res.json()
            for skill in res_json.get('skills', []):
                skill['job_uuid'] = (res_json.get('job_uuid'))
                result.append(skill)
    if result:
        df2 = pd.DataFrame(result)
        df2.to_csv("../data/job_related_skills.csv",  mode='a', header=True, index=False)

#
# asyncio.run(launch())