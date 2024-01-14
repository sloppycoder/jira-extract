import jira_extract


def test_jira_access():
    jira = jira_extract.jira_client()
    for issue in jira_extract.enumber_epic_and_stories(jira, "BBX"):
        print(issue.key, issue.fields.issuetype.name)
