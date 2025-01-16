from enum import Enum, StrEnum


class VideoSuffixes(StrEnum):
    MKV = ".mkv"
    MP4 = ".mp4"


class ExtensionSuffixes(StrEnum):
    ASS = ".ass"
    SRT = ".srt"
    MKA = ".mka"
    FLAC = ".flac"


class DefaultSettingKeys(Enum):
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
    EPISODE_INDEX = "episode_index"
    ADD_EPISODE = "add_episode"
    SEASON = "session"
    PROP = "prop"


class DefaultSettingValues(Enum):
    CUT_INDEX = "x"
    SEASON = ""
    PROP = -1
