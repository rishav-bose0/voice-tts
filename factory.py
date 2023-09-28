from aggregate import TTSAggregate, UserAggregate
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
