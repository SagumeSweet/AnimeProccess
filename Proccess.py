import os
import json
from sys import exit


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


def rename(file_list, process_conf_, cut_conf_):
    # 输入处理方案
    front = ''
    behind = ''
    if cut_conf_['front'] != 'x' and cut_conf_['behind'] != 'x':
        front = cut_conf_['front']
        behind = cut_conf_['behind']
    else:
        file_list[0].example()
        print('如果只替换，直接回车')
        front = input('前：')
        behind = input('后：')

    # 重命名
    rename_list = []
    for i_ in file_list:
        rename_list.append(i_.rename(front, behind, process_conf_))
        for j in i_.subs:
            rename_list.append(j.rename(front, behind, process_conf_))
    if not confirm(rename_list):
        rename(file_list, process_conf_, cut_conf_)
    else:
        for i_ in rename_list:
            os.rename(i_['old'], i_['new'])


def process(name_, process_products):
    name_n = name_

    # 处理替换字符
    if process_products['replace']:
        for process_product in process_products['replace']:
            name_n = name_n.replace(process_product[0], process_product[1])
    # 处理中括号
    name_n = name_n.replace('][', ' ')
    name_n = name_n.replace('[', '')
    name_n = name_n.replace(']', '')
    # 处理集数
    if process_products['add_episode']['value'] != 0:
        episode = int(name_n[process_products['add_episode']['episode_index']:]) + process_products['add_episode']['value']
        name_n = name_n[:process_products['add_episode']['episode_index']] + episode_to_str(episode, process_products['add_episode']['episode_index'])
    # 处理季数
    if process_products['session']['value'] != '':
        episode_index = -2
        for index in range(1, len(name_n) + 1):
            if name_n[-index] == ' ':
                episode_index = -index + 1
                break
        episode = name_n[process_products['add_episode']['episode_index']:]
        name_n = name_n[:episode_index] + 'S' + process_products['session']['value'] + 'E' + episode
    # 添加开头结尾
    name_n = process_products['fAdd'] + name_n
    name_n += process_products['bAdd']

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


def getFile(name: str, conditions: dict):
    result = True
    if conditions['in']:
        for condition in conditions['in']:
            if condition not in name:
                result = False
    if conditions['not in']:
        for condition in conditions['not in']:
            if condition in name:
                result = False
    return result


def cutName(front, behind, name):
    new_name = ''
    if front != '' and behind != '':
        new_name = name[int(front):int(behind) + 1]
    elif front == '' and behind == '':
        new_name = name
    elif front == '' and behind != '':
        new_name = name[:int(behind) + 1]
    elif front != '' and behind == '':
        new_name = name[int(front):]
    return new_name


def episode_to_str(episode, episode_index):
    episode_str = str(episode)
    format_len = -episode_index
    episode_len = len(episode_str)
    if episode_len < format_len:
        while episode_len < format_len:
            episode_str = '0' + episode_str
            episode_len += 1
    return episode_str


def process_main(core_conf):
    # 将设置放进变量
    print(core_conf)
    path = (core_conf['path'].replace('E:\\Anime\\', 'Y:\\')).replace('E:\\Anime Movie\\', 'X:\\')  # server1路径替换成本地路径
    video_conditions = core_conf['videoConditions']
    process_conf = core_conf['process_conf']
    cut_conf = core_conf['cut_conf']

    print(path)

    # 实例化文件对象
    all_file = []
    video_list = []
    for i in os.listdir(path):
        all_file.append(i)
    # 筛选视频
    for i in range(len(all_file)):
        if getFile(all_file[i], video_conditions):
            video_list.append(Video(path, all_file[i], -4))

    if len(video_list) < 1:
        print("No videos are there!")
        exit()

    for i in video_list:
        i.get_sub(all_file)

    # 改名
    rename(video_list, process_conf, cut_conf)


class File(object):
    def __init__(self, path_, name_, ex_num):
        self.path = path_
        self.oa_name = os.path.join(path_, name_)
        self.name = name_[:ex_num]
        self.extension = name_[ex_num:]

    def rename(self, front_, behind_, process_conf_):
        new = os.path.join(self.path, process(cutName(front_, behind_, self.name), process_conf_) + self.extension)
        return {'old': self.oa_name, 'new': new}


class Video(File):
    def __init__(self, path_, name_, ex_num):
        super().__init__(path_, name_, ex_num)
        self.subs = []

    def get_sub(self, file_list):
        num_ex = len(self.name)
        for i_ in file_list:
            if if_sub(self.name, i_) and '.mkv' not in i_:
                self.subs.append(File(self.path, i_, num_ex))

    def example(self):
        example(self.name)


conf = {
    'path': r'',

    # 筛选文件
    'videoConditions': {'in': ['.mkv'], 'not in': []},

    'cut_conf': {
        # 从哪里开始切片，为x时需要键入
        'front': 'x',
        'behind': 'x'
    },

    'process_conf': {
        'replace': [
            # 需要替换的字符，列表，前面是原来的后面是要改的(list, 0是旧的，1是新的)
            ["", ""]
        ],
        # 在前后添加字符
        'fAdd': '',
        'bAdd': '',
        # 增加集数（value为0即为不添加，index为集数占后几位）
        'add_episode': {'value': 0, 'episode_index': -2},
        # 季数（value为空即为不添加，index为集数占后几位）
        'session': {'value': '02', 'episode_index': -2}
    }
}

if __name__ == "__main__":
    with open("conf.json", "r", encoding="utf-8") as confFile:
        confJson = json.load(confFile)
        confFile.close()
    process_main(confJson)
