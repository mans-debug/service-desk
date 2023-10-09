import psql_util


def template_names():
    return [template[1] for template in find_all()]


def find_all():
    q = "select * from templates order by id asc"
    return psql_util.execute_PG_query(q)
