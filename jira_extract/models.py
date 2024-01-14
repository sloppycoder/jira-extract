from dataclasses import dataclass

from sqlalchemy import JSON, TEXT, Integer, String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()


@dataclass
class JiraIssue(Base):
    __tablename__ = "jira_issues"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # noqa: A003, VNE003
    key: Mapped[str] = mapped_column(String(16))
    issue_type: Mapped[str] = mapped_column(String(16))
    labels: Mapped[list[str]] = mapped_column(JSON)
    title: Mapped[str] = mapped_column(String(1024))
    description: Mapped[str] = mapped_column(TEXT)
    priority: Mapped[str] = mapped_column(String(16))
    sprint: Mapped[str] = mapped_column(String(1024), nullable=True)
    release: Mapped[str] = mapped_column(String(64), nullable=True)
