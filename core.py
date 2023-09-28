import torch

import constants
from entity.tts_entity import TTSEntity
from entity.user_entity import UserEntity
from factory import TTSApiFactory, UsersApiFactory
from repository.repository import TTSRepository
from repository.speaker_repository import SpeakerRepository
from repository.user_repository import UserRepository
from vits import commons, utils
from vits.models import SynthesizerTrn
from vits.text.symbols import symbols
from vits.text import text_to_sequence
from logger import logger


class VitsModel:

    def __init__(self):
        self.hps_ms = utils.get_hparams_from_file("../vits/configs/vctk_base.json")
        self.model = self.get_model()

    def get_model(self):
        net_g_ms = SynthesizerTrn(
            len(symbols),
            self.hps_ms.data.filter_length // 2 + 1,
            self.hps_ms.train.segment_size // self.hps_ms.data.hop_length,
            n_speakers=self.hps_ms.data.n_speakers,
            **self.hps_ms.model)
        _ = net_g_ms.eval()

        _ = utils.load_checkpoint("../vits/pretrained_vctk.pth", net_g_ms, None)
        return net_g_ms

    def get_clean_text(self, text, hps):
        text_norm = text_to_sequence(text, hps.data.text_cleaners)
        if hps.data.add_blank:
            text_norm = commons.intersperse(text_norm, 0)
        text_norm = torch.LongTensor(text_norm)
        return text_norm

    def run_tts(self, tts_entity: TTSEntity):
        speaker_id = tts_entity.speaker_id
        text = tts_entity.text
        speech_metadata = tts_entity.speech_metadata
        sid = torch.LongTensor([speaker_id])  # speaker identity
        stn_tst = self.get_clean_text(text, self.hps_ms)
        duration = speech_metadata.get_duration()

        with torch.no_grad():
            x_tst = stn_tst.unsqueeze(0)
            x_tst_lengths = torch.LongTensor([stn_tst.size(0)])
            return \
                self.model.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=.2, noise_scale_w=0.2,
                                 length_scale=duration)[
                    0][0, 0].data.cpu().float().numpy()


class TTSCore:
    def __init__(self):
        self.tts_model = VitsModel()
        self.tts_repo = TTSRepository()
        self.user_repo = UserRepository()
        self.speaker_repo = SpeakerRepository()
        self.tts_api_factory = TTSApiFactory()
        self.user_api_factory = UsersApiFactory()

    def process_tts(self, tts_entity: TTSEntity):
        audio = self.tts_model.run_tts(tts_entity)
        tts_aggregate = self.tts_api_factory.build(tts_entity)
        self.tts_repo.create_tts_aggregate(tts_aggregate=tts_aggregate)
        logger.info("TTS task successful")
        return audio

    def add_user(self, user_entity: UserEntity):
        user_aggregate = self.user_api_factory.build(user_entity)
        user_id = self.user_repo.create_user_aggregate(user_aggregate=user_aggregate)
        logger.info("User Creation successful")
        return user_id
