from config import app_config
from web.base import create_app


def run_api_app(app_config):
    api_app = create_app(app_config)
    return api_app


app = run_api_app(app_config)

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
