import sys
# fix pycache issue
sys.dont_write_bytecode = True

from app.core import App
from app.routes.cat_route import handel_cat_routes
from app.routes.user_routes import handel_user_routes
from app.db.client import DB
from app.db.schema import create_tables

db = DB()
app = App()

create_tables()
handel_cat_routes(app)
handel_user_routes(app)


app.run()
