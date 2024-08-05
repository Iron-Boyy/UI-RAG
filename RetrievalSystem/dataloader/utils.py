def utf8_next_char(s, start=0):
    # Encode the string to UTF-8 bytes if not already in byte form
    if isinstance(s, str):
        data = s.encode('utf-8')
    elif isinstance(s, bytes):
        data = s
    else:
        raise ValueError("Input must be a string or bytes")

    if start >= len(data):
        raise ValueError("Start position is out of the string length")

    first_byte = data[start]
    if (first_byte & 0x80) == 0:
        # Single byte character (ASCII)
        return first_byte, 1

    elif (first_byte & 0xE0) == 0xC0:
        # Two byte character
        if start + 1 >= len(data):
            raise ValueError("Incomplete 2-byte character at the end of data")
        return ((first_byte & 0x1F) << 6) | (data[start + 1] & 0x3F), 2

    elif (first_byte & 0xF0) == 0xE0:
        # Three byte character
        if start + 2 >= len(data):
            raise ValueError("Incomplete 3-byte character at the end of data")
        return ((first_byte & 0x0F) << 12) | ((data[start + 1] & 0x3F) << 6) | (data[start + 2] & 0x3F), 3

    elif (first_byte & 0xF8) == 0xF0:
        # Four byte character, but treated as space (' ')
        if start + 3 >= len(data):
            raise ValueError("Incomplete 4-byte character at the end of data")
        return ord(' '), 4

    else:
        # Invalid UTF-8 start byte
        raise ValueError(f"Cannot decode UTF-8 character: 0x{first_byte:X}")


def is_blanks(ch):
    return chr(ch) in ('\n', ' ', '\t', '\v')

def is_number(ch):
    return '0' <= chr(ch) <= '9'

# 假设有一个函数 IsSpecificChars 和一个列表 chinese_numbers 来处理中文数字
# 这里需要先定义这个列表和检查函数
chinese_numbers = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十']

def is_specific_chars(ch, chars):
    return chr(ch) in chars

def is_number_ch(ch):
    return is_number(ch) or is_specific_chars(ch, chinese_numbers)

def is_lower_case(ch):
    print(ch)
    return 'a' <= chr(ch) <= 'z'

def is_upper_case(ch):
    return 'A' <= chr(ch) <= 'Z'

def is_alpha(ch):
    print("alpha: ", ch)
    return is_lower_case(ch) or is_upper_case(ch)

def is_alpha_number(ch):
    print("alpha number: ", ch)
    return is_alpha(ch) or is_number(ch)

# # 使用这些函数的示例：
# char = ord('5')
# print(chr(char))
# print("Is blank:", is_blanks(char))
# print("Is number:", is_number(char))
# print("Is number including Chinese:", is_number_ch(char))
# print("Is lower case:", is_lower_case(char))
# print("Is upper case:", is_upper_case(char))
# print("Is alpha:", is_alpha(char))
# print("Is alpha or number:", is_alpha_number(char))


def emit_line_buffer(out, line_buffer):
    """ Append the contents of line_buffer to out and clear line_buffer """
    out += line_buffer
    line_buffer = ""  # Clear line_buffer by reassigning it to an empty string
    return out, line_buffer

from enum import Enum

class LineType(Enum):
    kNormalLine = 0
    kStartsWithNumber = 1
    kOnlyNumbers = 2
    kStartsWithSpecificChar = 3
    kPrabableInTable = 4
    kPrabableTitleLine = 5
    kPrabableInReference = 6

# Example usage:
example_str = "Abstract\n [15]dfnodlv,bdsknvbkn25，45613.\n555摘要二零05五年"
index = 0
example_str_byte = example_str.encode('utf-8')




chinese_comma = '，'
chinese_period = '。'
chinese_exclamation = '！'
chinese_pause = '、'


trim_flag = False
line_start_flag = True
this_line_start_pos = 0

line_content = ""
line_type = LineType.kNormalLine

line_buffer = ""
is_first_line = True
emit_line_buffer_flag = False

clear_line_content_flag = True

last_char = 0

title_level = 1
last_token_is_number = True

char_starts_with_spacified_char = 0
out =""

def append_char(line_buffer:str, line_content, ch:int, len):
    if len <= 3:
        # 直接追加字符，这里假设 ch 已经是字符串格式
        line_buffer  += chr(ch)
        if ch != ord(' '):
            line_content += chr(ch)
    else:
        # 处理更长的字符，假设这些是四字节字符
        # 在 Python 中，即使是长字符，也可以直接追加
        line_buffer += chr(ch)
        if ch != ord(' '):
            line_content += ord(ch)

    # 返还更新后的值，因为字符串和列表在函数外部不会自动更新
    return line_buffer, line_content


def next_char(ch, i, len, emit_line_buffer_flag, is_first_line, line_buffer, out):
    last_ch = ch
    i += len

    if emit_line_buffer_flag:
        out, line_buffer = emit_line_buffer(out, line_buffer)
        emit_line_buffer_flag = False
        is_first_line = True

    return last_ch, i, emit_line_buffer_flag, is_first_line, line_buffer, out


print(example_str_byte)

while index < len(example_str_byte):

    if clear_line_content_flag:
        line_content = ""
        clear_line_content_flag = False

    char, char_len = utf8_next_char(example_str_byte, index)
    # print(f"Character: {chr(char)} (size: {char_len})")


    if (char_len == 3) and (char & 0xffff == 0x80e2) and ((char >> 16) & 0xff) >= 0x80 and ((char >> 16) & 0xff) <= 0x8f:
        #goto next char
        last_char, index, emit_line_buffer_flag, is_first_line, line_buffer, out = next_char(char, index, char_len, emit_line_buffer_flag, is_first_line, line_buffer, out)
        continue

    
    if line_start_flag and char == ord(' '):
        #goto next char
        last_char, index, emit_line_buffer_flag, is_first_line, line_buffer, out = next_char(char, index, char_len, emit_line_buffer_flag, is_first_line, line_buffer, out)
        continue
    

    last_token_is_number = (char >= ord('0') and char <= ord('9'))

    if char == ord('\n'):
        if line_content == "Abstract" or line_content == "摘要":
            line_type = LineType.kPrabableTitleLine
        
        clear_line_content_flag = True

        old_line_type = line_type
        line_start_flag = True
        line_type = LineType.kNormalLine
        this_line_start_pos = line_buffer.__len__()

        if not trim_flag:
            if is_alpha_number(last_char):
                line_buffer += " "
            if is_number(last_char):
                line_type = old_line_type
                #goto next char
                last_char, index, emit_line_buffer_flag, is_first_line, line_buffer, out = next_char(char, index, char_len, emit_line_buffer_flag, is_first_line, line_buffer, out)
                continue
        
        if old_line_type == LineType.kPrabableTitleLine:
            line_buffer = ' ' + line_buffer
            old_title_level = title_level

            title_level = 1

            for j in range(old_title_level):
                line_buffer = '#' + line_buffer
            
            line_buffer = '\n' + line_buffer

            emit_line_buffer_flag = True

            #goto append char
            line_buffer,line_content = append_char(line_buffer, line_content, char, char_len)
            last_char, index, emit_line_buffer_flag, is_first_line, line_buffer, out = next_char(char, index, char_len, emit_line_buffer_flag, is_first_line, line_buffer, out)

            continue

        
        if last_char == ord('\n'):
            #goto next char
            last_char, index, emit_line_buffer_flag, is_first_line, line_buffer, out = next_char(char, index, char_len, emit_line_buffer_flag, is_first_line, line_buffer, out)
            continue

        if not trim_flag:
            is_first_line = False
            #goto next char
            last_char, index, emit_line_buffer_flag, is_first_line, line_buffer, out = next_char(char, index, char_len, emit_line_buffer_flag, is_first_line, line_buffer, out)
            continue
        emit_line_buffer_flag = True

        #goto append char
        line_buffer,line_content = append_char(line_buffer, line_content, char, char_len)
        last_char, index, emit_line_buffer_flag, is_first_line, line_buffer, out = next_char(char, index, char_len, emit_line_buffer_flag, is_first_line, line_buffer, out)

        continue



    if line_type == LineType.kStartsWithNumber:
        if char == ord('.') or char == ord(' ') or char == ord(chinese_pause):
            line_type = LineType.kPrabableTitleLine
    
    if char == ord('.') and line_type == LineType.kPrabableTitleLine:
        title_level = min(title_level + 1, 3)
    
    if char == ord(chinese_period) or char == ord(chinese_exclamation) or char == ord('.') or char == ord('!'):

        if char == ord('.') and (line_type == LineType.kPrabableInReference or last_token_is_number):
            pass
        else:
            trim_flag = True
        #goto append char
        line_buffer,line_content = append_char(line_buffer, line_content, char, char_len)
        last_char, index, emit_line_buffer_flag, is_first_line, line_buffer, out = next_char(char, index, char_len, emit_line_buffer_flag, is_first_line, line_buffer, out)
        continue

    if char == ord(' '):
        #goto append char
        line_buffer,line_content = append_char(line_buffer, line_content, char, char_len)
        last_char, index, emit_line_buffer_flag, is_first_line, line_buffer, out = next_char(char, index, char_len, emit_line_buffer_flag, is_first_line, line_buffer, out)

        continue

    if line_start_flag and is_first_line and is_number_ch(char):
        line_type = LineType.kStartsWithNumber
        out, line_buffer = emit_line_buffer(out, line_buffer)

    elif line_start_flag and char == ord('['):
        line_type = LineType.kStartsWithSpecificChar
        char_starts_with_spacified_char = ord('[')
    elif line_type == LineType.kStartsWithSpecificChar and ord('[') == char_starts_with_spacified_char:
        line_type = LineType.kPrabableInReference
    
    trim_flag = False
    line_start_flag = False

    line_buffer,line_content = append_char(line_buffer, line_content, char, char_len)
    last_char, index, emit_line_buffer_flag, is_first_line, line_buffer, out = next_char(char, index, char_len, emit_line_buffer_flag, is_first_line, line_buffer, out)


out += line_buffer


print(out)







    
