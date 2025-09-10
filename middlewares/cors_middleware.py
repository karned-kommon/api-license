import logging
from starlette.middleware.cors import CORSMiddleware as StarletteCorsMW

class CORSMiddleware(StarletteCorsMW):
    def __init__(self, app):
        logging.info("Initializing CORSMiddleware")
        super().__init__(
            app=app,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["Content-Type", "X-License-Key", "Authorization"],
            max_age=600
        )
