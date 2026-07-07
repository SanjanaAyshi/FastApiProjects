from sqlmodel import SQLModel, create_engine, Session
# Database URL-This creates a file called "todos.db" in your project folder
DATABASE_URL = "sqlite:///./todos.db"

# Engine — the connection to database
engine = create_engine(DATABASE_URL, echo=True)
#                          echo=True prints SQL queries in terminal
#                          Helps us learn what's happening!
#                          Turn off in production

# Create all tables
def create_db():
    SQLModel.metadata.create_all(engine)
     # "Look at all my models and create tables for them"

# Get a session (database connection for each request)
def get_session():
    with Session(engine) as session:
        yield session
        # "yield" means:
    # 1. Create session
    # 2. Give it to the route
    # 3. When route is done, close session automatically
    # Like borrowing a library card and returning it!