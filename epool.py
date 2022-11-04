#main epool file

from init import create_app
from models import db

app = create_app(db)

if __name__ == "__main__":
    app.run()