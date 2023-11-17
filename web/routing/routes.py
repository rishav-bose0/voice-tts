from flask_restx import Api

from web.controllers.ping_controller import Ping
from web.controllers.tts_controller import ProcessTTS, SignUpUser, LoginUser, VoicePreview, ListVoices, \
    ListSampleVoices, GetUserDetails, GetProjectDetails, CreateProject, CreateSpeakers, ListAllProjectsForUser, \
    UpdateUserDetails

default_routes = {
    '/ping': Ping,
}

api_routes = {
    '/process_tts': ProcessTTS,
    '/signup_user': SignUpUser,
    '/login_user': LoginUser,
    '/voice_preview/<int:speaker_id>/<string:name>': VoicePreview,
    '/list_all_voices': ListVoices,
    '/list_sample_voices': ListSampleVoices,
    '/get_user_details/<string:user_id>': GetUserDetails,
    '/create_project': CreateProject,
    '/get_project_details/<string:project_id>': GetProjectDetails,
    '/create_speakers': CreateSpeakers,
    '/list_all_projects_for_user/<string:user_id>': ListAllProjectsForUser,
    '/update_user_details': UpdateUserDetails
}


def add_default_routes(api: Api) -> Api:
    for url, controller in default_routes.items():
        api.add_resource(controller, url)
    return api


def add_tts_api_routes(api: Api) -> Api:
    for url, controller in api_routes.items():
        api.add_resource(controller, url)
    return api
