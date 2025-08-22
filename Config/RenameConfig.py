from typing import Callable, Any

from .SettingEnum import DefaultSettingKeys, NullSettingValues


class BaseConfig(object):
    def __init__(self, source: dict):
        self._source: dict = source
        self._cache: dict = {}

    def __str__(self):
        return str(self._source)

    def _lazy_load(self, key: str, loader: Callable) -> Any:
        if key not in self._cache:
            self._cache[key] = loader(self._source[key])
        return self._cache[key]


class PathConfig(BaseConfig):
    @property
    def path_str(self) -> str:
        return self._source[DefaultSettingKeys.PATH_STRING]

    @property
    def path_replace(self) -> list[tuple[str, str]]:
        return self._source[DefaultSettingKeys.PATH_REPLACE]


class VideoFilterConfig(BaseConfig):
    @property
    def include_types(self) -> list[list[str]]:
        return self._source[DefaultSettingKeys.INCLUDE_TYPES]

    @property
    def not_include_types(self) -> list[list[str]]:
        return self._source[DefaultSettingKeys.NOT_INCLUDE_TYPES]


class CutConfig(BaseConfig):
    @property
    def start_index(self) -> Any:
        result = self._source[DefaultSettingKeys.START_INDEX]
        if type(result) is not int and type(result) is not type(NullSettingValues.CUT_INDEX.value):
            raise ValueError(f"Invalid value type: {type(result)}. Expected int or {type(NullSettingValues.CUT_INDEX.value)}.")
        return result

    @property
    def end_index(self) -> Any:
        result = self._source[DefaultSettingKeys.END_INDEX]
        if type(result) is not int and type(result) is not type(NullSettingValues.CUT_INDEX.value):
            raise ValueError(f"Invalid value type: {type(result)}. Expected int or {type(NullSettingValues.CUT_INDEX.value)}.")
        return result


class NumConfig(BaseConfig):
    @property
    def value(self) -> Any:
        result = self._source[DefaultSettingKeys.VALUE]
        if type(result) is not int and type(result) is not type(NullSettingValues.NUM.value):
            raise ValueError(f"Invalid value type: {type(result)}. Expected int or {type(NullSettingValues.NUM.value)}.")
        return result

    @property
    def length(self) -> int:
        return self._source[DefaultSettingKeys.NUM_LENGTH]


class EpisodeConfig(NumConfig):
    @property
    def add_episode(self) -> int:
        return self._source[DefaultSettingKeys.ADD_EPISODE]

class EpisodePhraseBoundariesConfig(BaseConfig):
    @property
    def left_boundaries(self) -> list[str]:
        return self._source[DefaultSettingKeys.LEFT_BOUNDARIES]

    @property
    def right_boundaries(self) -> list[str]:
        return self._source[DefaultSettingKeys.RIGHT_BOUNDARIES]


class ProcessConfig(BaseConfig):
    @property
    def replace_str(self) -> list[tuple[str, str]]:
        return self._source[DefaultSettingKeys.REPLACE]

    @property
    def head_add(self) -> str:
        return self._source[DefaultSettingKeys.HEAD_ADD]

    @property
    def tail_add(self) -> str:
        return self._source[DefaultSettingKeys.TAIL_ADD]

    @property
    def season(self) -> NumConfig:
        return self._lazy_load(DefaultSettingKeys.SEASON, NumConfig)

    @property
    def episode(self) -> EpisodeConfig:
        return self._lazy_load(DefaultSettingKeys.EPISODE, EpisodeConfig)

    @property
    def cut_conf(self) -> CutConfig:
        return self._lazy_load(DefaultSettingKeys.CUT_CONF, CutConfig)

    @property
    def episode_phrase_boundaries(self) -> EpisodePhraseBoundariesConfig:
        return self._lazy_load(DefaultSettingKeys.EPISODE_PHRASE_BOUNDARIES, EpisodePhraseBoundariesConfig)


class RenameConfig(BaseConfig):
    @property
    def video_filter(self) -> VideoFilterConfig:
        return self._lazy_load(DefaultSettingKeys.VIDEO_FILTER, VideoFilterConfig)

    @property
    def path(self) -> PathConfig:
        return self._lazy_load(DefaultSettingKeys.PATH, PathConfig)

    @property
    def process_config(self) -> ProcessConfig:
        return self._lazy_load(DefaultSettingKeys.PROCESS_CONF, ProcessConfig)

