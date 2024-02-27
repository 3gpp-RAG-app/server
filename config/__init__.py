from config.settings import load_config

def init_config(app):
    config = load_config()
    app.config.from_object(config)
  