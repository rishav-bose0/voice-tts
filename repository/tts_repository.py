from sqlalchemy import desc

from aggregate import TTSAggregate
from common.repository import base
from logger import logger
from models.tts_details import TTSDetails


class TTSRepository(base.Base):
    model = TTSDetails

    def __init__(self):
        pass

    def create_tts_aggregate(self, tts_aggregate: TTSAggregate):
        """
        creates model entry into database table tts_details
        @param tts_aggregate:
        :return: False, errors in case of any exception. Else commits to db and returns None.
        """

        tts_entity = tts_aggregate.get_tts_entity()
        try:
            tts_details_model = self.model(tts_entity)
            TTSRepository.commit(tts_details_model)
        except Exception as e:
            logger.error(f"failed to create model in repository, exception: {e}")
        finally:
            self.model.query.session.close()

    def load_tts_aggregate(self, tts_id) -> TTSAggregate:
        """
        loads the tts_aggregate with tts_id
        @param tts_id:
        :return: ttsAggregate
        """
        try:
            tts_details_model = self.model.query.filter(self.model.id == tts_id).first()
        except Exception as e:
            logger.error(e)
            raise e
        finally:
            self.model.query.session.close()
        if tts_details_model is None:
            return None
        tts_entity = tts_details_model.to_entity()
        tts_aggregate = TTSAggregate()
        tts_aggregate.set_tts_entity(tts_entity)
        return tts_aggregate

    def load_tts_aggregate_by_project_id(self, project_id) -> {}:
        try:
            tts_details_models = self.model.query.filter(self.model.project_id == project_id).order_by(
                desc(self.model.updated_at)).all()
        except Exception as e:
            logger.error(e)
            raise e
        finally:
            self.model.query.session.close()
        tts_entities_by_block = {}
        for tts_details_model in tts_details_models:
            tts_entity = tts_details_model.to_entity()
            if tts_entities_by_block.get(tts_entity.block_number) is None:
                tts_entities_by_block[tts_entity.block_number] = tts_entity

        return tts_entities_by_block
        # return list(tts_entities_by_block.values())
