from enum import Enum, StrEnum


class VideoSuffixes(StrEnum):
    MKV = ".mkv"
    MP4 = ".mp4"


class ExtensionSuffixes(StrEnum):
    ASS = ".ass"
    SRT = ".srt"
    MKA = ".mka"
    FLAC = ".flac"


class DefaultSettingKeys(StrEnum):
    PATH = "path"
    PATH_STRING = "path_str"
    PATH_REPLACE = "path_replace"
    VIDEO_FILTER = "videoConditions"
    INCLUDE_TYPES = "in"
    NOT_INCLUDE_TYPES = "not in"
    CUT_CONF = "cut_conf"
    START_INDEX = "front"
    END_INDEX = "behind"
    PROCESS_CONF = "process_conf"
    REPLACE = "replace"
    HEAD_ADD = "fAdd"
    TAIL_ADD = "bAdd"
    VALUE = "value"
    NUM_LENGTH = "num_length"
    EPISODE = "episode"
    ADD_EPISODE = "add_episode"
    SEASON = "season"
    PROP = "prop"
    EPISODE_PHRASE_BOUNDARIES = "episode_phrase_boundaries"
    LEFT_BOUNDARIES = "left_boundaries"
    RIGHT_BOUNDARIES = "right_boundaries"


class NullSettingValues(Enum):
    CUT_INDEX = None
    NUM = None


class DefaultSettingValues(Enum):
    PATH_STRING = ""
    PATH_REPLACE = []
    INCLUDE_TYPES = [
        [VideoSuffixes.MKV],
        [VideoSuffixes.MP4]
    ]
    NOT_INCLUDE_TYPES = []
    REPLACE = [
        ["][", " "],
        ["]", ""],
        ["[", ""],
        ["  ", " "]
    ]
    START_INDEX = NullSettingValues.CUT_INDEX.value
    END_INDEX = NullSettingValues.CUT_INDEX.value
    HEAD_ADD = ""
    TAIL_ADD = ""
    EPISODE = NullSettingValues.NUM.value
    EPISODE_LENGTH = 2
    ADD_EPISODE = 0
    SEASON = NullSettingValues.NUM.value
    SEASON_LENGTH = 2
    LEFT_BOUNDARIES = [" ", "[", "-"]
    RIGHT_BOUNDARIES = [" ", "]", "-"]
