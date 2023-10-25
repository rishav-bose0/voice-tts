from aggregate import UserAggregate
from common.repository import base
from entity.user_entity import UserEntity
from logger import logger
from models.user_details import UserDetails


class UserRepository(base.Base):
    model = UserDetails

    def __init__(self):
        pass

    def create_user_aggregate(self, user_aggregate: UserAggregate):
        """
        creates model entry into database table user_details
        :param user_aggregate:
        :return: False, errors in case of any exception. Else commits to db and returns None.
        """

        user_entity = user_aggregate.get_user_entity()
        try:
            user_details_model = self.model(user_entity)
            UserRepository.commit(user_details_model)
        except Exception as e:
            logger.error(f"failed to create model in repository, exception: {e}")
            raise e
        return user_entity.id.value()

    def update_user_aggregate(self, user_aggregate: UserAggregate):
        user_entity = user_aggregate.get_user_entity()
        user_id = user_entity.get_id()
        try:
            new_user_details_model = self.model(user_entity)
            user_details_model = self.model.query.filter(self.model.id == user_id).first()
            user_details_model.update_data(new_user_details_model)
            UserRepository.update_commit()
        except Exception as e:
            logger.error(f"failed to update model in repository, exception: {e}")
            raise e
        return user_entity.id.value()

    def load_user_aggregate(self, user_id) -> UserEntity:
        """
        loads the user_aggregate with user_id
        :param user_id:
        :return: userAggregate
        """
        try:
            user_details_model = self.model.query.filter(self.model.id == user_id).first()
        except Exception as e:
            logger.error(e)
            raise e
        finally:
            self.model.query.session.close()
        if user_details_model is None:
            return None
        user_entity = user_details_model.to_entity()
        return user_entity

    def load_user_aggregate_by_details(self, email, password) -> UserEntity:
        """
        loads the user_aggregate with user_id
        :param email:
        :param password:
        :return: userAggregate
        """
        try:
            user_details_model = self.model.query.filter(
                self.model.email == email and self.model.password == password).first()
        except Exception as e:
            logger.error("Failed to load details for {}. Exception occurred {}".format(email, e))
            raise e
        finally:
            self.model.query.session.close()
        if user_details_model is None:
            return None
        user_entity = user_details_model.to_entity()
        return user_entity
