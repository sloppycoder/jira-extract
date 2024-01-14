import argparse
import sys

from dotenv import load_dotenv
from jira.resources import Issue
from sqlalchemy.orm import Session

from . import custom_mappings, enumber_epic_and_stories, jira_client, sql_session
from .models import JiraIssue


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", help="JIRA project key")
    options = parser.parse_args(argv)
    return options


def custom_field_value(issue: Issue, field_name: str, custom_fields: dict[str, str]):
    field_id = custom_fields.get(field_name)
    if field_id:
        return getattr(issue.fields, field_id, "")
    return ""


def save_issue(session: Session, issue: Issue, custom_fields: dict[str, str] = {}) -> JiraIssue | None:
    issue_type = issue.fields.issuetype.name
    if issue_type not in ["Epic", "Story"]:
        return None

    issue_obj = session.query(JiraIssue).filter_by(key=issue.key).first()
    if issue_obj is None:
        issue_obj = JiraIssue(key=issue.key)

    desc = issue.fields.description
    issue_obj.description = desc if desc else ""
    issue_obj.title = issue.fields.summary
    issue_obj.issue_type = issue_type
    issue_obj.labels = issue.fields.labels
    issue_obj.priority = issue.fields.priority.name
    issue_obj.release = ",".join([ver.name for ver in issue.fields.fixVersions])

    sprint = custom_field_value(issue, "Sprint", custom_fields)
    if sprint:
        issue_obj.sprint = sprint[0].name

    session.add(issue_obj)
    session.commit()

    return issue_obj


def main(argv):
    options = parse_args(argv)
    jira = jira_client()
    custom_fields = custom_mappings(jira, ["Sprint", "Release"])

    session = sql_session()
    for issue in enumber_epic_and_stories(jira, project_key=options.project):
        issue_obj = save_issue(session, issue, custom_fields)
        if issue_obj:
            print(f"saved {issue_obj.key} {issue_obj.title}")


if __name__ == "__main__":
    load_dotenv()

    main(argv=sys.argv[1:])
