from sqlalchemy import create_engine, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="todo")


def insert_tasks(rows):
    """Create each row as a Task in a fresh in-memory SQLite DB, then
    return every stored task as a plain dict {"id","title","status"},
    ordered by id. Missing "status" should default to "todo"."""
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        # Add a Task object for every row in the input list
        for row in rows:
            task = Task(
                title=row["title"],
                status=row.get("status", "todo"),  # default to "todo" if missing
            )
            session.add(task)

        session.commit()

        # Read all tasks back from the DB, ordered by id
        all_tasks = session.query(Task).order_by(Task.id).all()

        # Convert each Task object into a plain dict before returning
        result = []
        for task in all_tasks:
            result.append({"id": task.id, "title": task.title, "status": task.status})

        return result
