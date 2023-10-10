from services.jira_client import get_organizations
import psql_util


def org_names():
    return [val["name"] for val in get_organizations()["values"]]


def db_org_names():
    q = "select name from tenants order by priority asc"
    return list(map(lambda x: x[0], psql_util.execute_PG_query(q)))


def find_ord_by_name(name):
    q = f"select jira_id from tenants where name == {name}"
    return psql_util.execute_PG_query(q)[0][0]
