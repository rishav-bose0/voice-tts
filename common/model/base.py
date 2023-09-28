from flask import abort
from marshmallow import ValidationError
from sqlalchemy.ext.hybrid import hybrid_property

from logger import logger
from common.model import db
from common.utils.unique_id_generator import UniqueIdGenerator
from common.utils.time_utils import get_curr_time


class Base(db.Model):
    __abstract__ = True

    created_at = db.Column(db.Integer, nullable=False, index=True,
                           default=get_curr_time)
    created_at._creation_order = 9996

    updated_at = db.Column(db.Integer, nullable=False, index=True,
                           default=get_curr_time, onupdate=get_curr_time)
    updated_at._creation_order = 9997

    deleted_at = db.Column(db.Integer, nullable=True, index=True)
    deleted_at._creation_order = 9998

    # If this is true, system will generate 14 characters unique id while model creation
    generate_id_on_create = True

    def __init__(self):
        self.created_at = get_curr_time()
        self.updated_at = get_curr_time()

    @hybrid_property
    def is_not_deleted(self):
        return self.deleted_at.is_(None)

    @staticmethod
    def generate_unique_id():
        return UniqueIdGenerator().generate_unique_id()

    @staticmethod
    def model_load(schema, data):
        try:
            schema.load(data)
        except ValidationError as err:
            logger.error(err.messages)
            abort(400, err.messages)

    def build(self):
        if self.generate_id_on_create:
            self.id = self.generate_unique_id()

    def edit(self, input):
        for key in input.keys():
            setattr(self, key, input[key])
        self.updated_at = get_curr_time()
