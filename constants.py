DEFAULT_ENV_MODE = "dev"
app_context = "app_context"

REQUEST_ID_CONSTANT = 'request_id'
FLASK_REQUEST_ID = 'FLASK_REQUEST_ID'
regex_alpha_numeric = '^[a-zA-Z0-9]+$'
rzp_id_length = 14

# TTS request constants
PITCH = "pitch"
EMOTION = "emotion"
DURATION = "duration"
SPEAKER_ID = "speaker_id"
TEXT = "text"
PROJECT_ID = "project_id"
BLOCK_NUMBER = "block_number"
LANGUAGE = "language"
IS_TTS_GENERATED = "is_tts_generated"

# User request constants
EMAIL = "email"
FIRST_NAME = "first_name"
LAST_NAME = "last_name"
PASSWORD = "password"
TOKEN = "token"
PRIVILEGE_TYPE = "privilege_type"

AUDIO_FORMAT = "audio/wav"
PRETRAINED_VCTK_PATH = "../vits/pretrained_vctk_tts.pth"

JWT_EXPIRY_TIME = "jwt_expiry_time"
JWT_SECRET = "jwt_secret"

GOOGLE_OAUTH_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

ERROR_DESCRIPTION = "error_description"

# Project Details
BLOCK_DETAILS = "block_details"
TTS_DETAILS = "tts_details"
SPEAKER_DETAILS = "speaker_details"
NAME = "name"

# Model Names
VCTK_VIT_MODEL = "VCTK"
VCTK_TORTOISE_MODEL = "TORTOISE_VCTK"

sample_voice_preview = {
    "130": "https://voaux.s3.ap-south-1.amazonaws.com/promo_audio/Ethan.wav",
    "126": "https://voaux.s3.ap-south-1.amazonaws.com/promo_audio/Peter.wav",
    "116": "https://voaux.s3.ap-south-1.amazonaws.com/promo_audio/Emery.wav",
    "121": "https://voaux.s3.ap-south-1.amazonaws.com/promo_audio/Rachel.wav",
}
