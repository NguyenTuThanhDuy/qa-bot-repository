from database.postgres_db.base import PostgresConnector


postgres_connector = PostgresConnector()


def get_db_session():
    """ Dependency function for FastAPI routes """
    yield from postgres_connector.get_db()
