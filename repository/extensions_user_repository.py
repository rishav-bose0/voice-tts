from sqlalchemy.exc import IntegrityError

from aggregate import ExtensionsUserAggregate
from common.repository import base
from logger import logger
from models.extensions_user_details import ExtensionsUserDetails


class ExtensionsUserRepository(base.Base):
    model = ExtensionsUserDetails

    def __init__(self):
        pass

    def create_extensions_user_aggregate(self, extensions_user_aggregate: ExtensionsUserAggregate):
        """
        creates model entry into database table user_details
        @param extensions_user_aggregate:
        :return: False, errors in case of any exception. Else commits to db and returns None.
        """

        extensions_user_entity = extensions_user_aggregate.get_extensions_user_entity()
        try:
            logger.info("user commit")

            extensions_user_details_model = self.model(extensions_user_entity)
            ExtensionsUserRepository.commit(extensions_user_details_model)
            logger.info("user commited")
        except IntegrityError:
            logger.info("user exists")
        except Exception as e:
            logger.error(f"failed to create model in repository, exception: {e}")
            raise e
        finally:
            self.model.query.session.close()
        return extensions_user_entity.id.value()
