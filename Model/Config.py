from StringEnum.SettingEnum import DefaultSettingKeys


class BaseConfig(object):
    def __init__(self, source: dict):
        self._source = source

    def __str__(self):
        return str(self._source)


class PathConfig(BaseConfig):
    @property
    def path_str(self) -> str:
        return self._source[DefaultSettingKeys.PATH_STRING.value]

    @property
    def path_replace(self) -> list[list[str, str]]:
        return self._source[DefaultSettingKeys.PATH_REPLACE.value]


class VideoFilterConfig(BaseConfig):
    @property
    def include_types(self) -> list[list[str]]:
        return self._source[DefaultSettingKeys.INCLUDE_TYPES.value]

    @property
    def not_include_types(self) -> list[list[str]]:
        return self._source[DefaultSettingKeys.NOT_INCLUDE_TYPES.value]


class CutConfig(BaseConfig):
    @property
    def start_index(self) -> int:
        return self._source[DefaultSettingKeys.START_INDEX.value]

    @property
    def end_index(self) -> int:
        return self._source[DefaultSettingKeys.END_INDEX.value]


class NumConfig(BaseConfig):
    @property
    def value(self) -> int | str:
        return self._source[DefaultSettingKeys.VALUE.value]

    @property
    def length(self) -> int:
        return self._source[DefaultSettingKeys.NUM_LENGTH.value]


class EpisodeConfig(NumConfig):
    @property
    def add_episode(self) -> int:
        return self._source[DefaultSettingKeys.ADD_EPISODE.value]

class ProcessConfig(BaseConfig):
    @property
    def replace_str(self) -> list[list[str, str]]:
        return self._source[DefaultSettingKeys.REPLACE.value]

    @property
    def head_add(self) -> str:
        return self._source[DefaultSettingKeys.HEAD_ADD.value]

    @property
    def tail_add(self) -> str:
        return self._source[DefaultSettingKeys.TAIL_ADD.value]

    @property
    def season(self) -> NumConfig:
        return NumConfig(self._source[DefaultSettingKeys.SEASON.value])

    @property
    def episode(self) -> EpisodeConfig:
        return EpisodeConfig(self._source[DefaultSettingKeys.EPISODE_INDEX.value])

    @property
    def cut_conf(self) -> CutConfig:
        return CutConfig(self._source[DefaultSettingKeys.CUT_CONF.value])



class Config(BaseConfig):
    @property
    def video_filter(self) -> VideoFilterConfig:
        return VideoFilterConfig(self._source[DefaultSettingKeys.VIDEO_FILTER.value])

    @property
    def path(self) -> PathConfig:
        return PathConfig(self._source[DefaultSettingKeys.PATH.value])

    @property
    def process_config(self) -> ProcessConfig:
        return ProcessConfig(self._source[DefaultSettingKeys.PROCESS_CONF.value])
