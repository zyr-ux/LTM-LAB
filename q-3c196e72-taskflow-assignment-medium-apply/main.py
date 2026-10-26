from sqlalchemy import create_engine, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="todo")


def apply_ops(seed, ops):
    """Seed the repo, then apply ops in order. Each op is a dict with "op":
      - "create":        {"op":"create","title":..,"status":..}
      - "update_status": {"op":"update_status","id":..,"status":..}
      - "rename":        {"op":"rename","id":..,"title":..}
      - "delete":        {"op":"delete","id":..}
    Ops targeting a missing id are safe no-ops. Return
    {"count": <n>, "tasks": [ {"id","title","status"} sorted by id ]}."""
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        for r in seed:
            session.add(Task(title=r["title"], status=r.get("status", "todo")))
        session.commit()
        for op in ops:
            kind = op["op"]

            if kind == "create":
                # Insert a brand-new task
                new_task = Task(title=op["title"], status=op.get("status", "todo"))
                session.add(new_task)
                session.commit()

            elif kind == "update_status":
                # Change the status of an existing task; skip if id not found
                task = session.get(Task, op["id"])
                if task is not None:
                    task.status = op["status"]
                    session.commit()

            elif kind == "rename":
                # Change the title of an existing task; skip if id not found
                task = session.get(Task, op["id"])
                if task is not None:
                    task.title = op["title"]
                    session.commit()

            elif kind == "delete":
                # Remove an existing task; skip if id not found
                task = session.get(Task, op["id"])
                if task is not None:
                    session.delete(task)
                    session.commit()

        # Read all remaining tasks, ordered by id
        all_tasks = session.query(Task).order_by(Task.id).all()

        # Build and return the summary dict
        task_list = []
        for task in all_tasks:
            task_list.append({"id": task.id, "title": task.title, "status": task.status})

        return {"count": len(task_list), "tasks": task_list}