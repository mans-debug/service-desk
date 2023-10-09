import requests


headers = {
    "Accept": "application/json",
    "Authorization": "Basic di5lcmdhc2hldmFAc3RhcmZpc2gyNC5jb206QVRBVFQzeEZmR0YweHo2NWtQcElVN3BFM1VuMXdBNHpIc2RUNVd4c3JlLTVaMzZDTUJkMkZGd1NaSUJUUkIwQVRQSjFNU2NHNUp0ZGVRRG94UThoOVZMZTljSUdKWjNpMTFzRUF4Vm5MUEs2MjNlS1N0cTJlOUZMVG9vQjdHMFdVM0FJT0Exc3NzcHVzYzdDUlRFLVQ5N2JETlF1ZDhOaE9WSW9SeHdTR21wQ1lmUkZDbjNjLTY0PTg0NzMxQTY2",
}


def get_organizations():
    url = "https://starfish24.atlassian.net/rest/servicedeskapi/organization"
    return requests.request("GET", url, headers=headers).json()


def create_ticket(title, text, company_id):
    url = "https://starfish24.atlassian.net/rest/api/3/issue"
    querystring = {
        "updateHistory": "true",
        "applyDefaultValues": "false",
        "skipAutoWatch": "true",
    }
    payload = {
        "fields": {
            "project": {"id": "10006"},
            "issuetype": {"id": "10020"},
            "customfield_10010": "itsm/systemproblem",
            "reporter": {"id": "62e905d6e50f2f2a395489c9"},
            "summary": title,
            "description": {
                "version": 1,
                "type": "doc",
                "content": [
                    {"type": "paragraph", "content": [{"type": "text", "text": text}]}
                ],
            },
            "priority": {
                "id": "2",
                "name": "Major C",
                "iconUrl": "https://starfish24.atlassian.net/images/icons/priorities/high.svg",
            },
            "customfield_10002": [company_id],
        },
        "update": {},
        "watchers": ["62e905d6e50f2f2a395489c9"],
    }
    return requests.request(
        "POST", url, json=payload, headers=headers, params=querystring
    ).json()
