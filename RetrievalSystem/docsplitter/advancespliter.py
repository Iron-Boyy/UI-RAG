#encoding: utf-8

import re

def split_text(mixed_text: str):
    # 使用正则表达式进行分块，保留空格
    pattern = re.compile(
        r'[\u4e00-\u9fff]|'         # 匹配单个汉字
        r'[a-zA-Z]+(?=[\u4e00-\u9fff])|'  # 匹配紧接在汉字前的字母串
        r'(?<=[\u4e00-\u9fff])[a-zA-Z]+|'  # 匹配紧接在汉字后的字母串
        r'[a-zA-Z]+|'                # 匹配独立的字母串
        r'\d+(\.\d+)?(?=[\u4e00-\u9fff])|'  # 匹配紧接在汉字前的数字串（包含小数）
        r'(?<=[\u4e00-\u9fff])\d+(\.\d+)?|'  # 匹配紧接在汉字后的数字串（包含小数）
        r'\d+(\.\d+)?|'              # 匹配独立的数字串（包含小数）
        r'[^\w\s]|\n|'               # 匹配标点符号或单个换行符
        r'\s+'                       # 匹配空格
    )
    
    tokens = [match.group() for match in pattern.finditer(mixed_text)]
    return tokens

def combine_tokens(tokens, max_length):
    combined = []
    current_chunk = []
    sentence_endings = {'.', '!', '?', '。', '！', '？'}

    for token in tokens:
        if token.isspace():
            current_chunk.append(token)
            continue
        
        current_chunk.append(token)
        if len([t for t in current_chunk if not t.isspace()]) > max_length:
            # 查找最后一个标点符号的位置
            last_punct_idx = max((idx for idx, t in enumerate(current_chunk) if t in sentence_endings), default=None)
            if last_punct_idx is not None:
                # 在最后一个标点符号处分割
                combined.append(''.join(current_chunk[:last_punct_idx + 1]))
                current_chunk = current_chunk[last_punct_idx + 1:]
            else:
                # 如果没有找到标点符号，强制分割
                combined.append(''.join(current_chunk[:-1]))
                current_chunk = current_chunk[-1:]

    if current_chunk:
        combined.append(''.join(current_chunk))

    return combined



def split_text_internal(text:str, max_length:int, ver:bool=False):
    
    tokens = split_text(text)
    if ver:
        print("try to split token num: {}".format(tokens.__len__()))

    combined_tokens = combine_tokens(tokens, max_length)

    return combined_tokens


if __name__ == '__main__':


    text = '''男士内裤豆腐脑斯康杜尼。是不是12.54李雷l'''

    tokens = split_text(text)
    print("Tokens:", tokens)

    max_length = 1500
    combined_tokens = combine_tokens(tokens, max_length)
    print("Combined Tokens:", combined_tokens)

    print(combined_tokens.__len__())

    print([x.__len__() for x in combined_tokens])
