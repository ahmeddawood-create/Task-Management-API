from sqlmodel import SQLModel, Field, Session, create_engine

class tasks(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    done: bool = Field(default=False)

engine = create_engine("sqlite:///mytasks.db", echo=True)

def create_db_tables():
    SQLModel.metadata.create_all(engine)



