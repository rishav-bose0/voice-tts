import json

from aggregate import ProjectAggregate
from common.repository import base
from entity.project_entity import ProjectEntity
from logger import logger
from models.project_details import ProjectDetails


class ProjectRepository(base.Base):
    model = ProjectDetails

    def __init__(self):
        pass

    def create_project_aggregate(self, project_aggregate: ProjectAggregate):
        """
        creates model entry into database table project_details
        @param project_aggregate:
        :return: False, errors in case of any exception. Else commits to db and returns None.
        """

        project_entity = project_aggregate.get_project_entity()
        try:
            project_details_model = self.model(project_entity)
            ProjectRepository.commit(project_details_model)
        except Exception as e:
            logger.error(f"failed to create model in repository, exception: {e}")
            raise e
        return project_entity.id.value()

    def update_project_aggregate(self, project_aggregate: ProjectAggregate):
        project_entity = project_aggregate.get_project_entity()
        project_id = project_entity.get_id()
        try:
            new_project_details_model = self.model(project_entity)
            project_details_model = self.model.query.filter(self.model.id == project_id).first()
            project_details_model.update_data(new_project_details_model)
            ProjectRepository.update_commit()
        except Exception as e:
            logger.error(f"failed to update model in repository, exception: {e}")
            raise e
        return project_entity.id.value()

    def load_project_aggregate(self, project_id) -> ProjectEntity:
        """
        loads the project_aggregate with project_id
        @param project_id:
        :return: projectAggregate
        """
        try:
            project_details_model = self.model.query.filter(self.model.id == project_id).first()
        except Exception as e:
            logger.error(e)
            raise e
        finally:
            self.model.query.session.close()
        if project_details_model is None:
            return None

        return project_details_model.to_entity()

    def load_project_details_for_user(self, user_id) -> {}:
        try:
            project_details_models = self.model.query.filter(self.model.user_id == user_id).all()
        except Exception as e:
            logger.error(e)
            raise e
        finally:
            self.model.query.session.close()

        project_entities = {}
        for project_details_model in project_details_models:
            project_entity = project_details_model.to_entity()
            project_entities[project_entity.get_id()] = json.loads(project_entity.toJSON())

        return project_entities, None
