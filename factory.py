from aggregate import TTSAggregate, UserAggregate, ProjectAggregate, ExtensionsUserAggregate
from entity.extensions_user_entity import ExtensionsUserEntity
from entity.project_entity import ProjectEntity
from entity.tts_entity import TTSEntity
from entity.user_entity import UserEntity


class TTSApiFactory:
    def __init__(self):
        pass

    def build(self, entity: TTSEntity) -> TTSAggregate:
        tts_aggregate = TTSAggregate(entity)
        tts_aggregate.get_tts_entity().initialize()
        return tts_aggregate


class UsersApiFactory:
    def __init__(self):
        pass

    def build(self, entity: UserEntity) -> UserAggregate:
        user_aggregate = UserAggregate(entity)
        user_aggregate.get_user_entity().initialize()
        return user_aggregate


class ProjectApiFactory:
    def __init__(self):
        pass

    def build(self, entity: ProjectEntity) -> ProjectAggregate:
        project_aggregate = ProjectAggregate(entity)
        project_aggregate.get_project_entity().initialize()
        return project_aggregate


class ExtensionsUsersApiFactory:
    def __init__(self):
        pass

    def build(self, entity: ExtensionsUserEntity) -> ExtensionsUserAggregate:
        extensions_user_aggregate = ExtensionsUserAggregate(entity)
        extensions_user_aggregate.get_extensions_user_entity().initialize()
        return extensions_user_aggregate
