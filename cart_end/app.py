import flask

cart_end_app = flask.Blueprint(
    name= "cart_end_app" ,
    import_name= "app",
    template_folder= "cart_end/templates",
    static_folder= "cart_end/static"
)