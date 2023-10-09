from services.jira_client import get_organizations


def org_names():
    return [val["name"] for val in get_organizations()["values"]]
