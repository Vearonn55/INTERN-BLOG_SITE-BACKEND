from app import create_app
from app.engine import engine
from sqlmodel import Session, select
from app.models.user import User

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
