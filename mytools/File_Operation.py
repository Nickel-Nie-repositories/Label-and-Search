import re

# 用文件行头部，查找文件的行，输出行数和行。
from rapidfuzz.distance import Levenshtein


def get_line_by_filename(File, filename):
    with open(File, "r") as f:
        for index, line in enumerate(f.readlines()):
            # if line.split("\t")[0] == keyword:
            if line.split("\t")[0] in filename:
                return line, index
        return "", -1


def get_line_by_index(File, index):
    with open(File, "rU") as f:
        if index < 0:
            return ""
        for cur_line_number, line in enumerate(f):
            if cur_line_number == index:
                return line
        return ""


# 向文件指定行写入内容。（暂时这样）
def write_line_by_index(File, index: int, content: str):
    with open(File, 'r') as f:
        lines = f.readlines()

    lines[index] = content + "\n"

    with open(File, 'w') as f:
        f.writelines(lines)


# 文本退格一个label。
def backspace_label(text: str, separator: str):
    # 先拆分文件行头和labels：
    sep = text.split("\t", 1)
    # 然后将后面的部分按分隔符拆开重组，移除最后一个。
    # 如果本来就是空label ，返回。
    if sep[1] == "":
        return sep[0] + "\t", ""

    temp = sep[1].split(separator)
    pop_label = temp[-2]
    # 如果本来只剩一个label，返回。
    if len(temp) < 3:
        return sep[0] + "\t", pop_label

    # 如果本来有一个以上，剩下的label要在最后加个分隔符。
    sep1 = separator.join(temp[:-2]) + separator

    ret = sep[0] + "\t" + sep1
    return ret, pop_label


# 判断一个label是不是坐标：
def is_coordinate(text: str):
    if text == "":
        return False
    if text[0] != "(" or text[-1] != ")":
        return False
    float_list = text[1:-1].split(",")
    for each_float in float_list:
        if not is_number(each_float):
            return False
    return True


# 判断一个字符串是否表达一个数字：
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


# 判断keywords （str的list）中是否所有关键词都在这一行。
def all_keywords_in_line(keywords, line):
    for keyword in keywords:
        if keyword not in line:
            return False
    return True


# 用文件行内容，查找lines的行，输出找到匹配的行的列表。
def get_lines_by_keyword(lines, keyword):
    line_list = []
    for line in lines:
        if keyword in line:
            line_list.append(line)
    return line_list


# 输入一个keyword的列表，在文件中查找同时包含这些keyword的行，然后从这些行的行头中获得文件名。
def get_files_by_keywords(File, keywords):
    with open(File, "r") as f:
        line_list = f.readlines()
        for k in keywords:
            line_list = get_lines_by_keyword(line_list, k)
    file_list = [line.split("\t")[0] for line in line_list]
    return file_list


# 判断字符串相似性（引入模糊搜索备用）越小越相似
def str_similarity(str1, str2):
    return Levenshtein.normalized_distance(str1, str2)
    # 暂时不知道考虑中文 形近/音近 的模糊搜索的距离计算。


# 判断keywords （str的list）中是否所有关键词都在这一行。（模糊搜索版）
def all_keywords_in_line_fuzzy(keywords, line):
    linesWords = line.split()
    for keyword in keywords:
        found_flag = False
        for word in linesWords:
            if str_similarity(keyword, word) <= 0.5:
                found_flag = True
                break
        if not found_flag:
            return False
    return True
