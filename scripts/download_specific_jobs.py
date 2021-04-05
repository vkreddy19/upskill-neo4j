from py2neo.bulk import create_relationships
import pandas as pd

df = pd.read_csv("../data/Filtered data.xlsx")
data = []
cache = {}
for index, row in df.iterrows():
    if row[1]:
        try:
            related_jobs = row[1].split("_")
        except:
            print(row, index)
            continue
        cur_job = row[0]
        print(cur_job)
        for job2 in related_jobs:
            key = min(cur_job, job2)+max(cur_job, job2)
            if job2 != cur_job and key not in cache:
                data.append((( cur_job ), {}, (job2)))
                cache[key] = True

        if index % 1000 == 0:
            print("ingesting", index)
            create_relationships(g.auto(), data, "related",
                                 start_node_key=("Job", "uuid"), end_node_key=("Job", "uuid"))
            data = []
            print(index, "done")

if data:
    create_relationships(g.auto(), data, "related",
                         start_node_key=("Job", "uuid"), end_node_key=("Job", "uuid"))


# g = Graph()
# keys = ["name", "age"]
# data = [
#     ["Alice", 33],
#     ["Bob", 44],
#     ["Carol", 55],
# ]
# create_nodes(g.auto(), data, labels={"Person"}, keys=keys)
# g.nodes.match("Person").count()