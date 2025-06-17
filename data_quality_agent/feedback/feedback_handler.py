"""Store user feedback on suggested rules."""

from __future__ import annotations

from typing import Iterable

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)
    rule = Column(String)
    accepted = Column(Integer)  # 1 for accepted, 0 for rejected
    comment = Column(String)


def init_db(path: str = "feedback.db"):
    engine = create_engine(f"sqlite:///{path}")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)


def add_feedback(Session, rule: str, accepted: bool, comment: str = "") -> None:
    session = Session()
    session.add(Feedback(rule=rule, accepted=1 if accepted else 0, comment=comment))
    session.commit()
    session.close()


def list_feedback(Session) -> Iterable[Feedback]:
    session = Session()
    rows = session.query(Feedback).all()
    session.close()
    return rows


if __name__ == "__main__":
    Session = init_db()
    add_feedback(Session, "col_A IS NOT NULL", True)
    for fb in list_feedback(Session):
        print(f"{fb.rule} -> {fb.accepted}")
