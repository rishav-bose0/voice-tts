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
VCTK_VIT_MODEL = "VITS_VCTK"
VCTK_TORTOISE_MODEL = "TORTOISE_VCTK"
TORTOISE_CLONE_MODEL = "TORTOISE_CLONE"

sample_voice_preview = {
    282: "https://voaux.s3.ap-south-1.amazonaws.com/promo_audio/Ethan.wav",
    286: "https://voaux.s3.ap-south-1.amazonaws.com/promo_audio/Peter.wav",
    296: "https://voaux.s3.ap-south-1.amazonaws.com/promo_audio/Emery.wav",
    226: "https://voaux.s3.ap-south-1.amazonaws.com/promo_audio/Rachel.wav",
}

avatar_pics = {
    "M": [
        "https://vaux-contents.s3.us-east-2.amazonaws.com/profile_images/avatar_68.png",
        "https://vaux-contents.s3.us-east-2.amazonaws.com/profile_images/avatar_2.png",
        "https://vaux-contents.s3.us-east-2.amazonaws.com/profile_images/avatar_4.png",
        "https://vaux-contents.s3.us-east-2.amazonaws.com/profile_images/avatar_5.png",
        "https://vaux-contents.s3.us-east-2.amazonaws.com/profile_images/avatar_6.png",
        "https://vaux-contents.s3.us-east-2.amazonaws.com/profile_images/avatar_7.png",
        "https://vaux-contents.s3.us-east-2.amazonaws.com/profile_images/avatar_8.png",
        "https://vaux-contents.s3.us-east-2.amazonaws.com/profile_images/avatar_9.png",
        "https://vaux-contents.s3.us-east-2.amazonaws.com/profile_images/avatar_10.png",
        "https://vaux-contents.s3.us-east-2.amazonaws.com/profile_images/avatar_11.png",
        "https://vaux-contents.s3.us-east-2.amazonaws.com/profile_images/avatar_13.png"
    ],
    "F": [
        "https://vaux-contents.s3.us-east-2.amazonaws.com/profile_images/avatar_34.png",
        "https://vaux-contents.s3.us-east-2.amazonaws.com/profile_images/avatar_64.png",
        "https://vaux-contents.s3.us-east-2.amazonaws.com/profile_images/avatar_65.png",
        "https://vaux-contents.s3.us-east-2.amazonaws.com/profile_images/avatar_66.png",
        "https://vaux-contents.s3.us-east-2.amazonaws.com/profile_images/avatar_67.png",
        "https://vaux-contents.s3.us-east-2.amazonaws.com/profile_images/avatar_0.png",
        "https://vaux-contents.s3.us-east-2.amazonaws.com/profile_images/avatar_35.png",
        "https://vaux-contents.s3.us-east-2.amazonaws.com/profile_images/avatar_70.png",
        "https://vaux-contents.s3.us-east-2.amazonaws.com/profile_images/avatar_21.png",
        "https://vaux-contents.s3.us-east-2.amazonaws.com/profile_images/avatar_37.png",
        "https://vaux-contents.s3.us-east-2.amazonaws.com/profile_images/avatar_73.png",
        "https://vaux-contents.s3.us-east-2.amazonaws.com/profile_images/avatar_74.png",
        "https://vaux-contents.s3.us-east-2.amazonaws.com/profile_images/avatar_75.png",
        "https://vaux-contents.s3.us-east-2.amazonaws.com/profile_images/avatar_76.png"
    ]
}
