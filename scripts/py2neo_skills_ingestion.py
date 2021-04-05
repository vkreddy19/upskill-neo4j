from py2neo import Graph
from py2neo.bulk import create_nodes
from py2neo.bulk import create_relationships
import pandas as pd
import numpy as np
g = Graph("bolt://localhost:11015", password="vamshi19")


keys = ["uuid", "skill_name", "skill_type","description", "normalized_skill_name", "importance","level"]
df = pd.read_csv("../data/job_related_skills.csv",header=None, names=["skill_id", "skill_name", "skill_type","description", "normalized_skill_name", "importance","level", "job_id"], dtype={"skill_id":str, "skill_name":str, "skill_type":str,"description":str, "normalized_skill_name":str, "importance":str,"level":str ,"job_id":str})
skills_data = []
relation_data = []
cache = {}
skills_created = {}
relation_created = {}
for index, row in df.iterrows():
    # print(row)
    print(index)
    skill_id = row[0]
    job_id = row[-1]
    print(skill_id, job_id)
    if skill_id not in skills_created:
        skills_data.append(list(row)[:-1])
        skills_created[skill_id] = True

    if skill_id+job_id not in relation_created:
        relation_data.append(((job_id), {}, (skill_id)))
        relation_created[skill_id+job_id] = True

    if index%10000 == 0:
        create_nodes(g.auto(), skills_data, labels={"Skill"}, keys=keys)
        skills_data = []

    # if index%100000 ==0:
    #     print(relation_data)
    #     create_relationships(g.auto(), relation_data, "need",
    #                          start_node_key=("Job", "uuid"), end_node_key=("Skill", "uuid"))
    #     relation_data=[]
if skills_data:
    create_nodes(g.auto(), skills_data, labels={"Skill"}, keys=keys)
#
for i in range(0,len(relation_data), 10000):
        res=create_relationships(g.auto(), relation_data[i:i+10000], "need",
                             start_node_key=("Job", "uuid"), end_node_key=("Skill", "uuid"))

