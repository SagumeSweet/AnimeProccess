import json

from .SettingEnum import DefaultSettingKeys, DefaultSettingValues


class ConfigGenerator:
    _default_config = {
        DefaultSettingKeys.PATH: {
            DefaultSettingKeys.PATH_STRING: DefaultSettingValues.PATH_STRING.value,
            DefaultSettingKeys.PATH_REPLACE: DefaultSettingValues.PATH_REPLACE.value,
        },
        DefaultSettingKeys.VIDEO_FILTER: {
            DefaultSettingKeys.INCLUDE_TYPES: DefaultSettingValues.INCLUDE_TYPES.value,
            DefaultSettingKeys.NOT_INCLUDE_TYPES: DefaultSettingValues.NOT_INCLUDE_TYPES.value,
        },
        DefaultSettingKeys.PROCESS_CONF: {
            DefaultSettingKeys.REPLACE: DefaultSettingValues.REPLACE.value,
            DefaultSettingKeys.CUT_CONF: {
                DefaultSettingKeys.START_INDEX: DefaultSettingValues.START_INDEX.value,
                DefaultSettingKeys.END_INDEX: DefaultSettingValues.END_INDEX.value,
            },
            DefaultSettingKeys.HEAD_ADD: DefaultSettingValues.HEAD_ADD.value,
            DefaultSettingKeys.TAIL_ADD: DefaultSettingValues.TAIL_ADD.value,
            DefaultSettingKeys.EPISODE: {
                DefaultSettingKeys.VALUE: DefaultSettingValues.EPISODE.value,
                DefaultSettingKeys.NUM_LENGTH: DefaultSettingValues.EPISODE_LENGTH.value,
                DefaultSettingKeys.ADD_EPISODE: DefaultSettingValues.ADD_EPISODE.value,
            },
            DefaultSettingKeys.SEASON: {
                DefaultSettingKeys.VALUE: DefaultSettingValues.SEASON.value,
                DefaultSettingKeys.NUM_LENGTH: DefaultSettingValues.SEASON_LENGTH.value,
            },
            DefaultSettingKeys.EPISODE_PHRASE_BOUNDARIES: {
                DefaultSettingKeys.LEFT_BOUNDARIES: DefaultSettingValues.LEFT_BOUNDARIES.value,
                DefaultSettingKeys.RIGHT_BOUNDARIES: DefaultSettingValues.RIGHT_BOUNDARIES.value,
            }
        }
    }
    default_config_name: str = "confTemple.json"

    @classmethod
    def generate_default_config(cls) -> None:
        """
        生成默认配置字典
        """
        with open(cls.default_config_name, "w", encoding='utf-8') as config_file:
            json.dump(cls._default_config, config_file, indent=2)
