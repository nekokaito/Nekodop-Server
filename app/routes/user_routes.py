from ..controllers.user_controllers import (register_user, login, get_users)

def handel_user_routes(app):
    # register user
    @app.post("/register")
    def route(req):
        return register_user(req)

    # login user
    @app.post("/login")
    def route(req):
        return login(req)

    # get users
    @app.get("/get-users")
    def route(req):
        return get_users(req)
