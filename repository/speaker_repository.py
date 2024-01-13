from sqlalchemy import desc

from aggregate import SpeakerAggregate
from common.repository import base
from entity.speaker_entity import SpeakerEntity
from logger import logger
from models.speaker_details import SpeakerDetails


class SpeakerRepository(base.Base):
    model = SpeakerDetails

    def __init__(self):
        pass

    def create_speaker_aggregate(self, speaker_entity: SpeakerEntity):
        """
        creates model entry into database table speaker_details
        @param speaker_entity:
        :return: False, errors in case of any exception. Else commits to db and returns None.
        """

        try:
            speaker_details_model = self.model(speaker_entity)
            SpeakerRepository.commit(speaker_details_model)
        except Exception as e:
            logger.error(f"failed to create model in repository, exception: {e}")
            raise e
        return None

    def load_speaker_aggregate(self, speaker_id) -> SpeakerAggregate:
        """
        loads the speaker_aggregate with speaker_id
        @param speaker_id:
        :return: speakerAggregate
        """
        try:
            speaker_id = str(speaker_id)
            speaker_details_model = self.model.query.filter(self.model.id == speaker_id).first()
        except Exception as e:
            logger.error(e)
            raise e
        finally:
            self.model.query.session.close()
        if speaker_details_model is None:
            return None
        speaker_entity = speaker_details_model.to_entity()
        speaker_aggregate = SpeakerAggregate()
        speaker_aggregate.set_speaker_entity(speaker_entity)
        return speaker_aggregate

    # def load_speaker_aggregate_by_name(self, name) -> SpeakerAggregate:
    #     """
    #     loads the speaker_aggregate with speaker_id
    #     @param speaker_id:
    #     :return: speakerAggregate
    #     """
    #     try:
    #         speaker_details_model = self.model.query.filter(self.model.name == name).first()
    #     except Exception as e:
    #         logger.error(e)
    #         raise e
    #     finally:
    #         self.model.query.session.close()
    #     if speaker_details_model is None:
    #         return None
    #     speaker_entity = speaker_details_model.to_entity()
    #     speaker_aggregate = SpeakerAggregate()
    #     speaker_aggregate.set_speaker_entity(speaker_entity)
    #     return speaker_aggregate

    def list_all_speakers(self, user_id) -> [SpeakerEntity]:
        try:
            speaker_detail_models = self.model.query.filter(
                (self.model.speaker_type == "public") | (self.model.user_id == user_id)
            ).order_by(
                desc(self.model.created_at)
            ).all()
            # self.model.query.order_by(
            # desc(self.model.created_at)).all()
        except Exception as e:
            logger.error(e)
            raise e
        finally:
            self.model.query.session.close()

        speaker_list = []
        for speaker_detail_model in speaker_detail_models:
            speaker_list.append(speaker_detail_model.to_entity())
        return speaker_list

    def list_sample_speakers(self, speaker_ids: []):
        try:
            speaker_detail_models = self.model.query.filter(self.model.id.in_(speaker_ids)).all()
        except Exception as e:
            logger.error(e)
            raise e
        finally:
            self.model.query.session.close()

        speaker_list = []
        for speaker_detail_model in speaker_detail_models:
            speaker_list.append(speaker_detail_model.to_entity())
        return speaker_list

    def list_speakers_details_for_model(self, model_name) -> [SpeakerEntity]:
        try:
            speaker_detail_models = self.model.query.filter(self.model.model_name == model_name).order_by(
                desc(self.model.created_at)
            ).all()
        except Exception as e:
            logger.error(e)
            raise e
        finally:
            self.model.query.session.close()

        speaker_list = []
        for speaker_detail_model in speaker_detail_models:
            speaker_list.append(speaker_detail_model.to_entity())
        return speaker_list
