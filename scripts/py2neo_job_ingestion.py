from neo4j import GraphDatabase
import pandas as pd
class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def create_unique_constraint_on_job(self):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_constraint_on_job)
            for record in result:
                print(record)

    def create_all_job_nodes(self):
        df = pd.read_csv("../data/filtered_jobs_data.csv")
        query = ""
        for index, job in df.iterrows():
            query += '(:Job { uuid: "%s",  title: "%s",  name: "%s"}), '%(job[0], job[1], job[2])
            if (index+1)%1000 == 0:
                    print(index)
                    res = self.executeQuery("CREATE "+query[:-2])
                    query = ""
        if query:
            res = self.executeQuery("CREATE "+query[:-2])


    def executeQuery(self, query):
        tx = self.driver.session().begin_transaction()
        result = tx.run(query)
        tx.commit()
        return result

    @staticmethod
    def _create_constraint_on_job(tx):
        query = (
           "CREATE CONSTRAINT unique_job ON (job: Job) ASSERT job.id IS UNIQUE"
           # "CREATE CONSTRAINT unique_related_relation ON [r:related] ASSERT r IS UNIQUE"
        )
        result = tx.run(query)
        return [record["name"] for record in result]

if __name__ == "__main__":
    # See https://neo4j.com/developer/aura-connect-driver/ for Aura specific connection URL.
    scheme = "bolt"  # Connecting to Aura, use the "neo4j+s" URI scheme
    host_name = "localhost"
    port = 11015
    url = "{scheme}://{host_name}:{port}".format(scheme=scheme, host_name=host_name, port=port)
    user = "neo4j"
    password = "vamshi19"
    app = App(url, user, password)
    print("started")
    # app.create_unique_constraint_on_job()
    app.create_all_job_nodes()
    app.close()
