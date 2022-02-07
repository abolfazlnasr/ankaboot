from connections.database_connection import get_connection


class DF:
    __df = None

    def __init__(self):
        pass

    @staticmethod
    def get_df():
        if DF.__df is None:
            DF.__df = {}

            with get_connection() as (cursor, conn):
                stmt = """
                select df, docs_count
                from df_models
                order by id desc
                limit 1
                """
                cursor.execute(stmt)
                result = cursor.fetchone()

            DF.__df['df_model'] = result['df']
            DF.__df['docs_count'] = result['docs_count']

        return DF.__df
