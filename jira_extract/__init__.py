import os
from typing import Iterator

from jira import JIRA
from jira.resources import Issue
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def sql_session(engine=None):
    if engine is None:
        engine = create_engine(os.environ.get("DATABASE_URL"))
    Session = sessionmaker(bind=engine)
    return Session()


def jira_client() -> JIRA:
    return JIRA(
        options={"server": os.environ.get("JIRA_SERVER")},
        basic_auth=(os.environ.get("JIRA_USERNAME", ""), os.environ.get("JIRA_API_TOKEN", "")),
    )


def custom_mappings(jira: JIRA, keys: list[str]) -> dict[str, str]:
    fields = jira.fields()
    return {field["name"]: field["id"] for field in fields if field["name"] in keys}


def enumber_epic_and_stories(jira: JIRA, project_key: str) -> Iterator[str | Issue]:
    for epic in jira.search_issues(f'project={project_key} AND issuetype="Epic"', maxResults=False):
        yield epic

        for story in jira.search_issues(
            f"project={project_key} AND issuetype='Story' AND 'Epic Link' = {epic.key}", maxResults=False
        ):
            yield story
