from sqlmodel import SQLModel, Field, create_engine,Session, select

class tasks(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    done: bool = Field(default=False)

engine = create_engine("sqlite:///mytasks.db", echo=True)

def create_db_tables():
    SQLModel.metadata.create_all(engine)

create_db_tables()

t1 = tasks(title="brush your teeth")
t3 = tasks(title="make breakfast")
t2 = tasks(title="pack your bag", done=True)

with Session(engine) as session:
        statement = select(tasks)
        alltasks = session.exec(statement).all()

        if not alltasks:
            session.add(t1)
            session.add(t2)
            session.add(t3)

            session.commit()

             

