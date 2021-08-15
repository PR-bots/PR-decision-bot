from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR, TIMESTAMP, Boolean, Text, Index

Base = declarative_base()

class PullRequest(Base):
    __tablename__ = "pull_requests"
    id = Column(Integer, primary_key=True)
    owner_login = Column(VARCHAR(255), nullable=False)
    repo_name = Column(VARCHAR(255), nullable=False)
    installation_id = Column(Integer, nullable=False)
    number = Column(Integer, nullable=False)
    state = Column(VARCHAR(255), nullable=False, index=True)
    locked = Column(Boolean, nullable=True, index=True)
    created_at = Column(TIMESTAMP, nullable=False)
    last_comment_at = Column(TIMESTAMP, nullable=True) # store the time for the last comment
    comment_or_not = Column(Boolean, nullable=False, default=0)
Index("owner_repo_num", PullRequest.owner_login, PullRequest.repo_name, PullRequest.number, unique=True)

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    pull_request_id = Column(Integer, nullable=False, index=True)
    comment_id = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    body = Column(Text, nullable=True)