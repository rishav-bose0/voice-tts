import re

from marshmallow import ValidationError

from common.utils.unique_id_generator import UniqueIdGenerator
import constants


class RzpID:
    def __init__(self, id=""):
        self.id: str = id

    def build(self, input_id):
        if self.__validate(input_id):
            self.id = input_id

    def create(self):
        self.id = UniqueIdGenerator().generate_unique_id()

    def value(self):
        return self.id

    def __validate(self, input_id):
        is_length_valid = len(input_id) == constants.rzp_id_length
        is_pattern_valid = re.search(constants.regex_alpha_numeric, input_id)

        if not (is_length_valid and is_pattern_valid):
            raise ValidationError(f'{input_id} is not a valid Razorpay Id.')
        return True
