from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR, TIMESTAMP, Boolean, Text

Base = declarative_base()

class PullRequest(Base):
    __tablename__ = "pull_requests"
    id = Column(Integer, primary_key=True)
    owner_login = Column(VARCHAR(255), nullable=False)
    repo_name = Column(VARCHAR(255), nullable=False)
    number = Column(Integer, nullable=False)
    state = Column(VARCHAR(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=True)
    comment_or_not = Column(Boolean, nullable=True)


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    pull_request_id = Column(Integer, nullable=False)
    comment_id = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    body = Column(Text, nullable=True)