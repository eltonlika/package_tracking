import pugsql


def connect(connection_string):
    queries = pugsql.module("db/")
    queries.connect(connection_string)
    queries.create_table_package()
    queries.create_table_package_event()
    queries.create_table_package_subscription()
    return queries
