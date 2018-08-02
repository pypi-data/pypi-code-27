from pyravendb.store.document_store import DocumentStore


class User:
    def __init__(self, name):
        self.name = name


if __name__ == "__main__":
    with DocumentStore(urls=["http://127.0.0.1:8081"], database="westWind") as store:
        store.initialize()
        with store.open_session() as session:
            session.store(User("Idan"))
            session.save_changes()
