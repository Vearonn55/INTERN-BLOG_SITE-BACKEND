from sqlmodel import create_engine, Session

DATABASE_URL = "postgresql://vearon:A29132C9BDy.@localhost:5432/blogdb"

# Create the SQLModel engine
engine = create_engine(DATABASE_URL, echo=True)

# Session generator (you can import and use in routes or CRUD)
def get_session():
    with Session(engine) as session:
        yield session
