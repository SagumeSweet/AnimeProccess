import json
import os
from copy import deepcopy
from sys import exit
from time import sleep

from Model.Config import Config, PathConfig, VideoFilterConfig, ProcessConfig, CutConfig, EpisodeConfig


def example(str_):
    example1 = ''
    q = []
    h = []
    num = []
    for i_ in range(len(str_)):
        q.append(str(i_))
        h.append(str(i_ + 1))
    for i_ in range(len(q)):
        num.append("(" + q[i_] + ")(-" + h[-(i_ + 1)] + ") | ")
    for i_ in range(len(str_)):
        if str_[i_] == ' ':
            example1 += '\n'
        example1 += str_[i_] + num[i_]
    print('\n\n' + "| " + example1 + '\n\n')


def get_cut_index(config: CutConfig) -> tuple[str, str]:
    if config.start_index != 'x' and config.end_index != 'x':
        start = config.start_index
        end = config.end_index
    elif config.start_index != 'x' and config.end_index == 'x':
        start = config.start_index
        print('如果只替换，直接回车')
        print('前：' + str(config.start_index))
        end = input('后：')
    elif config.start_index == 'x' and config.end_index != 'x':
        print('如果只替换，直接回车')
        start = input('前：')
        print('后：' + str(config.end_index))
        end = config.end_index
    else:
        print('如果只替换，直接回车')
        start = input('前：')
        end = input('后：')

    return start, end


def get_episode_index(episode_conf: EpisodeConfig) -> int | str:
    if episode_conf.value != "x":
        return episode_conf.value
    else:
        print("如果无需集数，直接回车")
        index = input("index=")
        return int(index) if index != "" else "x"


def try_rename_file(rename_dict: dict, count: int = 1) -> None:
    try:
        os.rename(rename_dict['old'], rename_dict['new'])
        return None
    except PermissionError:
        print(f"ERROR:重命名错误（疑似文件正在使用中），正在重试第{count}次")
        sleep(10)
        try_rename_file(rename_dict, count + 1)


def rename(file_list: list["Video"], process_conf_: ProcessConfig):
    # 输入处理方案
    file_list[0].example()
    start, end = get_cut_index(process_conf_.cut_conf)
    episode_index: int | str = get_episode_index(process_conf_.episode)
    # 重命名
    rename_list = []
    for i_ in file_list:
        rename_list.append(i_.rename(start, end, episode_index, process_conf_))
        for j in i_.subs:
            rename_list.append(j.rename(start, end, episode_index, process_conf_))
    if not confirm(rename_list):
        rename(file_list, process_conf_)
    else:
        for i_ in rename_list:
            try_rename_file(i_)


def process(cut_strat: str, cut_end: str, episode_index: int | str, name_, config: ProcessConfig):
    name_n = name_

    episode_num: int | str = get_episode_num(episode_index, name_) if episode_index != "x" else "x"
    episode_phrase: str = get_episode_phrase(episode_index, name_) if episode_index != "x" else ""

    if episode_phrase != "":
        name_n = name_n.replace(episode_phrase, "")

    # 裁剪
    name_n = cut_name(cut_strat, cut_end, name_n, episode_phrase, name_)

    # 处理替换字符
    if config.replace_str:
        for processing_str in config.replace_str:
            name_n = name_n.replace(processing_str[0], processing_str[1])

    # 添加开头结尾
    head: str = config.head_add
    tail: str = config.tail_add
    # 处理集数
    if episode_num != "x":
        episode_num += config.episode.add_episode
        head = f"E{num_to_str(episode_num, config.episode.length)} {head}"

    # 处理季数
    if config.season.value != "" and episode_num != "x":
        head = f"S{num_to_str(config.season.value, config.season.length)}{head}"

    name_n = head + name_n
    name_n += tail

    return name_n


def confirm(file_list):
    for i_ in range(len(file_list)):
        print(file_list[i_]['new'])
    user_confirm = input('确认名称是否无误(y/n, 退出exit)：')
    if user_confirm == 'y':
        return True
    elif user_confirm == 'exit':
        exit()
    else:
        return False


def if_sub(video, sub):
    for i_ in range(len(video)):
        if video[i_] != sub[i_]:
            return False
    return True


def foreach_video_filter_configs(configs: list, proc_fuc) -> bool:
    results_list = []
    for config in configs:
        result = True
        for option in config:
            result = proc_fuc(option)
            if not result:
                break
        results_list.append(result)
    return True in results_list


def video_filter(name: str, config: VideoFilterConfig) -> bool:
    is_in = True
    is_not_in = True
    if config.include_types:
        is_in = foreach_video_filter_configs(config.include_types, lambda x: x in name)
    if config.not_include_types:
        is_not_in = foreach_video_filter_configs(config.not_include_types, lambda x: x not in name)
    return is_in and is_not_in


def get_episode_num(episode_index: int, name: str) -> int:
    result_str: str = ""
    now_index: int = episode_index
    while (episode_index < 0 and now_index < 0 and name[now_index].isdigit()) or (episode_index > 0 and now_index < len(name) and name[now_index].isdigit()):
        result_str += name[now_index]
        now_index += 1
    return int(result_str)  # TODO:增加index错误时的处理


def get_episode_phrase(episode_index: int, name: str) -> str:
    result_str: str = ""
    now_index: int = episode_index
    now_char: str = name[episode_index]
    while ((episode_index < 0 and now_index < 0 and (now_char != ' ' and now_char != '[' and now_char != '-'))
           or (episode_index > 0 and now_index < len(name) and (now_char != ' ' and now_char != '[' and now_char != '-'))):
        result_str += now_char
        now_index += 1
        now_char = name[now_index]
    now_index = episode_index - 1
    now_char = name[now_index]
    while ((episode_index < 0 and now_index >= -len(name) and (now_char != ' ' and now_char != ']' and now_char != '-'))
           or (episode_index > 0 and now_index >= 0 and (now_char != ' ' and now_char != ']' and now_char != '-'))):
        result_str = now_char + result_str
        now_index -= 1
        now_char = name[now_index]
    result_str = now_char + result_str
    return result_str


def get_new_cut_index(index: int, episode_str: str, episode_index: int | str, old_name_length: int, new_name_length: int) -> int:
    if episode_str == "":
        return index
    del_length: int = len(episode_str)
    if index >= 0:
        # 正索引处理
        del_end = episode_index + del_length - 1
        if index > del_end:
            index -= del_length
        elif index >= episode_index:
            index = episode_index
    elif index < 0:
        # 负索引处理
        index = old_name_length + index  # 转为正索引
        del_end = episode_index + del_length - 1
        if index > del_end:
            index -= del_length
        elif index >= episode_index:
            index = episode_index
        index -= new_name_length  # 转回负索引
    return index


def cut_name(start: str, end: str, name: str, episode_str: str, old_name: str) -> str:
    new_name = ''
    episode_index: int = old_name.index(episode_str) if episode_str != "" else -1
    old_name_length: int = len(old_name)
    new_name_length: int = len(name)
    if start != '' and end != '':
        start_index = get_new_cut_index(int(start), episode_str, episode_index, old_name_length, new_name_length)
        end_index = get_new_cut_index(int(end), episode_str, episode_index, old_name_length, new_name_length)
        new_name = name[start_index:end_index]
    elif start == '' and end == '':
        new_name = name
    elif start == '' and end != '':
        end_index = get_new_cut_index(int(end), episode_str, episode_index, old_name_length, new_name_length)
        new_name = name[:end_index]
    elif start != '' and end == '':
        start_index = get_new_cut_index(int(start), episode_str, episode_index, old_name_length, new_name_length)
        new_name = name[start_index:]
    return new_name


def num_to_str(num: int, format_length: int) -> str:
    num_str = str(num)
    num_now_len = len(num_str)
    if num_now_len < format_length:
        while num_now_len < format_length:
            num_str = '0' + num_str
            num_now_len += 1
    return num_str


def get_real_path(config: PathConfig) -> str:
    result: str = config.path_str
    path_replace_list: list[list[str, str]] = config.path_replace
    for i in range(len(path_replace_list)):
        result = result.replace(path_replace_list[i][0], path_replace_list[i][1])
    return result


def process_main(config: Config):
    print(config)
    path = get_real_path(config.path)  # server1路径替换成本地路径

    process_conf: ProcessConfig = config.process_config

    print(path)

    # 实例化文件对象
    all_file = []
    video_list = []
    for i in os.listdir(path):
        all_file.append(i)
    other_list = deepcopy(all_file)

    # 筛选视频
    for i in range(len(all_file)):
        if video_filter(all_file[i], config.video_filter):
            video_list.append(Video(path, all_file[i]))
            other_list.remove(all_file[i])

    if len(video_list) < 1:
        print("No videos are there!")
        exit()

    # 获取字幕
    for i in video_list:
        i.get_sub(other_list)

    # 改名
    rename(video_list, process_conf)


def get_ext(name: str) -> str:
    ext: str = ""
    index: int = -1
    while name[index] != ".":
        ext = f"{name[index]}{ext}"
        index -= 1
    return f".{ext}"


class File(object):
    def __init__(self, path_, name_):
        self.path = path_
        self.extension = get_ext(name_)
        self.name = name_.replace(self.extension, "")

    @property
    def oa_name(self):
        return os.path.join(self.path, f"{self.name}{self.extension}")

    def rename(self, front_: int | str, behind_: int | str, episode_index: str | int, process_conf_: ProcessConfig):
        if episode_index != "x":
            episode_index = int(episode_index)
        new = os.path.join(self.path, process(front_, behind_, episode_index, self.name, process_conf_) + self.extension)
        return {'old': self.oa_name, 'new': new}


class Video(File):
    def __init__(self, path_, name_):
        super().__init__(path_, name_)
        self.subs: list[File] = []

    def get_sub(self, file_list):
        for i_ in file_list:
            if if_sub(self.name, i_) and (self.extension not in i_):
                sub: File = File(self.path, i_)
                sub.extension = sub.name.replace(self.name, "") + sub.extension
                sub.name = self.name
                self.subs.append(sub)

    def example(self):
        example(self.name)


conf = {
    "path": {
        "path_str": "",
        "path_replace": [
        ]
    },
    "videoConditions": {
        "in": [
            [".mkv"],
            [".mp4"]
        ],
        "not in": [
        ]
    },

    "process_conf": {
        "replace": [
            ["][", " "],
            ["]", ""],
            ["[", ""],
            ["- ", ""],
            ["  ", " "]
        ],
        "cut_conf": {
          "front": "x",
          "behind": "x"
        },
        "fAdd": "",
        "bAdd": "",
        "episode_index": {
            "value": "x",
            "num_length": 2,
            "add_episode": 0
        },
        "session": {
            "value": "",
            "num_length": 2
        }
    }
}

if __name__ == "__main__":
    with open("conf.json", "r", encoding="utf-8") as confFile:
        confJson = json.load(confFile)
    process_main(Config(confJson))
