import json
from typing import Optional

from .RenameConfig import RenameConfig
from .SettingEnum import DefaultSettingKeys


class ConfigLoader:
    @classmethod
    def load(cls, config_path: str = "conf.json") -> RenameConfig:
        print(f"Loading configuration: {config_path}")
        with open(config_path, "r", encoding='utf-8') as config_file:
            raw_data = json.load(config_file)
        raw_data[DefaultSettingKeys.PATH][DefaultSettingKeys.PATH_REPLACE] = cls._convert_replace_list_to_tuple(
            raw_data[DefaultSettingKeys.PATH][DefaultSettingKeys.PATH_REPLACE]
        )
        raw_data[DefaultSettingKeys.PROCESS_CONF][DefaultSettingKeys.REPLACE] = cls._convert_replace_list_to_tuple(
            raw_data[DefaultSettingKeys.PROCESS_CONF][DefaultSettingKeys.REPLACE]
        )
        config: RenameConfig = RenameConfig(raw_data)
        return config

    @classmethod
    def _convert_replace_list_to_tuple(cls, replace_list: list[list[str]]) -> list[tuple[str, str]]:
        """
        将替换选项从列表转换为元组
        """
        result: list[Optional[tuple[str, str]]] = []
        for item in replace_list:
            if len(item) != 2:
                raise ValueError(f"无效替换选项：{item}。每个替换选项必须完全包含两个元素")
            result.append((item[0], item[1]))
        return result
