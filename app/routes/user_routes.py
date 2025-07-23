from ..controllers.user_controllers import (delete_user, is_admin, register_user, login, get_users, get_user, update_password, update_user)

def handel_user_routes(app):
    # register user (options and post)
    @app.options("/register")
    def route(req):
         req.send(204, "")

    @app.post("/register")
    def route(req):
        return register_user(req)


    # register user (options and post)
    @app.options("/login")
    def route(req):
         req.send(204, "")

    @app.post("/login")
    def route(req):
        return login(req)

    # get user by id
    @app.get("/get-user/:id")
    def route(req):
        return get_user(req)

    # get users
    @app.get("/get-users")
    def route(req):
        return get_users(req)

    # update user (options and put)
    @app.options("/update-user/:user_id")
    def route(req):
        req.send(204, "")

    @app.put("/update-user/:user_id")
    def route(req):
        return update_user(req)
    # update password (options and put)
    @app.options("/update-password/:user_id")
    def route(req):
        req.send(204, "")
    
    @app.put("/update-password/:user_id")
    def route(req):
        return update_password(req)

    # delete user by id (delete and options)
    @app.options("/delete-user/:req_id/:user_id")
    def route(req):
        req.send(204, "")

    @app.delete("/delete-user/:req_id/:user_id")
    def route(req):
        return delete_user(req)


    # is admin
    @app.get("/is-admin/:id")
    def route(req):
        return is_admin(req)
