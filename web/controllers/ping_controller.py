from web.controllers.base_controller import BaseController


class Ping(BaseController):
    def get(self):
        return {"message": "Welcome to OCR Service"}
