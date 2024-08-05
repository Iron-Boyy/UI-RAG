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


    text = '''⽤AI 写研报哪家强？沙利⽂《2023\n中国⼤模型⾏研能⼒评测报告》商\n汤⽇⽇新·商量获评第⼀ \n⼤模型展现出强⼤的通⽤性和跨领域能⼒，正在助⼒千⾏百业发展，“⼈⼯智能+”\n（AI+）在2024 年⾸次被写⼊政府⼯作报告。 \n \n⽇前，权威研究机构弗若斯特沙利⽂（Frost & Sullivan, 简称“沙利⽂”）联合头豹研究\n院发布《2023 年中国⼤模型⾏研能⼒评测报告》\n。评测结果显示，商汤语⾔⼤模型“⽇\n⽇新·商量”（简称：商汤商量）以总分7.73（满分\
    10 分）斩获总榜第⼀，并在报告撰\n写能⼒（⼋⼤模块）\n、模型基础能⼒（⾏研基础能⼒）两个⼦榜位居第⼀。报告也给出\n结论：商汤⽇⽇新·商量（SenseChat）超越国际⼤模型均线，位列中国⼤模型第⼀梯\n队。 \n \n图：中国\
    ⼤模型⾏研能⼒综合评测榜单（来源：沙利⽂） \n \n \n为全⾯了解中国⼤模型在⾏业研究领域的应⽤表现，沙利⽂调动了百⼈规模的分析师，\n从研究报告撰写能⼒、模型基础能⼒、⾏业综合理解能⼒三⼤核⼼板块对⼤模型进⾏\n了\
    多维度的综合评估。 \n \n报告选定了中外19 个具有代表性的⼤模型进⾏评测，其中覆盖15 家国内主流模型，\n与此同时，国际⽅⾯选择了OpenAI 的GPT3.5 和GPT4、⾕歌的Gemini1.0 以及\nAnthropic 的Claude 2，并将这四⼤模型 \
    的平均⽔平设为国际⼤模型均线。 \n \n图：⼤模型⾏业能⼒评测⽅法：报告撰写、模型基础能⼒、⾏业理解 \n（来源：沙利⽂） \n \n经过模型能⼒评测，沙利⽂报告指出，商汤商量作为中国最早推向市场的千亿参数⼤\n语⾔模型之\
    ⼀，在报告撰写能⼒、模型基础能⼒等⽅⾯均领先其他⼤模型，不但可以\n处理各类⽂本和信息，在协助⾏业分析师⼯作时，还可胜任随⾝综合知识库、⾼效⽂\n本编辑器、数理计算器和简单易⽤的编程助⼿等多个⻆⾊。 \n  \n⾏研领\
    域内容创作“⾼⻔槛”，商汤商量三项“第⼀”解放⾏业⽣产⼒ \n  \n内容⽣成和创作能⼒是⽬前⼤模型最⽕热的应⽤场景，并且也是能够直接体现⼤模型\n⽣产⼒⽔平的能⼒。从⼤模型应⽤场景来看，⽆论是知识管理、市场营销、客户服\
    务，\n \n \n还是员⼯⾃⾝⽇常⼯作，都需要⼤模型具有优秀的内容⽣成和创作能⼒。Gartner 预测，\n到2025 年，企业30%的营销信息将会由⼤模型协助⽣成。 \n \n⾏业研究是通过分析特定⾏业的定义、竞争格局、市场规模等关键 \
    ⽅⾯，产出深刻洞\n察和观点，涵盖从宏观的产业层到微观的产品层，各层级决定着相应的研究⽅法，研\n究⽅法论囊括外部宏观因素和内部微观细节的全⾯分析。其⾏业特殊性、复杂性、严\n谨性对⼤模型的内容⽣成和创作能⼒提出 \
    了多维度的⾼要求。 \n \n同时，⽬前⾏业研究⼯作依然存在诸多痛点。从基础数据收集到深度分析输出，传统\n⾏业研究的流程⾯临着⼯具⾰新滞后、团队知识难以传承、信息溯源复杂性以及研报\n质量控制的重⼤挑战。 \n \n结合 \
    ⼤模型技术，可以协助分析师克服传统⾏业研究的核⼼制约因素，通过AI 专家访\n谈、AI 内容⽣成、AI ⽂字校对、AI 资料检索等多⽅⾯赋能⾏研⾏业，显著提升研究的\n精度和效率，同时加速分析师的专业成⻓，进⼀步推动⾏研数 \
    字化进程。 \n \n图：⼤模型赋能⾏业研究（来源：沙利⽂） \n \n商汤商量除了在总榜第⼀，在报告撰写能⼒的⼦榜单同样位居第⼀。此前，沙利⽂及\n头豹⾏企研究的8-D ⽅法论，是⼀种全⾯系统的研究⽅法，包含了⼋⼤关键模块 \
    ，⽤\n于对⾏业进⾏深⼊分析。 \n \n \n \n \n \n在这⼀框架下，百名分析师研磨提炼⼀套⾼效的8D 模块提问⽅法', '以对模型能⼒进⾏\n评测，商汤商量正是经过了这套⽅法的检验。沙利⽂认为，根据⼤模型报告撰写能⼒\n综合热\
    ⼒矩阵图可以看出商汤商量是综合能⼒最强的模型， 且在各个板块的表现稳定\n处在前列位置，体现出均衡的能⼒。 \n  \n \n \n \n图：⼤模型的撰写能⼒评测结果 - 热⼒矩阵图（来源：沙利⽂） \n  \n另外，在模型基础能⼒（⾏\
    研基础能⼒）⼦榜中，商汤商量再次夺魁，并在语境转换、\n⽂字⽣成、知识储备等模块排名第⼀，能够为⾏业研究提供深度分析和有价值的⻅解。\n分析师认为，商汤商量的产出内容能够避免使⽤⾮专业词汇，同时确保⽣成内容的完\n整性和专业性，从⽽为⽤户提供符合要求且令⼈阅读体验感满意的研究产出物。 \n图：⼤模型的模型基础能⼒（⾏研基础能⼒）评测结果 - 热⼒矩阵图 \n（来源：沙利⽂） \n  \n \n \n \n基于AI“三要素”全⾯深耕模型能⼒，商汤 \
    科技提速⽣成式AI 应⽤落地 \n \n商汤商量取得优秀的评测结果，离不开对基模型能⼒的⻓期耕耘和提升。⾸先，依托\n丰沛AI 算⼒的SenseCore 商汤AI ⼤装置，通过软件、硬件、⼯程化系统以服务⼤模\n型迭代为⽬标的研发配合，\
    保障了⼤模型的⾼频迭代，以及不断精炼的训练配⽅。 \n \n其次，商汤在积累巨⼤的原始语料数据的基础上，通过⾼精度的分类器和⼈⼯精细化\n清洗的⽅式，提炼出⾼质量的数据，进⽽训练性能强⼤、价值观对⻬的⼤模型。现在，\n商汤的⾼质量训练数据的每个⽉产出量，已经达到2 万亿Tokens。 \n \n在此之前，新华社研究院发布《⼈⼯智能⼤模型体验报告3.0》\n，报告显示，商汤“商量\nSenseChat”在定量实测的情商维度上，位居全部10 款⼤模型第⼀，并 \
    在定性评估中\n⼊选⼤模型市场未来领袖象限。借助丰厚、领先的算⼒和数据资源，商汤不断优化迭\n代⼤模型能⼒，提升⽣产⼒⽔平，未来将进⼀步引领⾏业研究进⼊⼀个效率更⾼和质\n量更优的新产出范式，以促进数字⾏业研究的 \
    创新和变⾰。 \n \n放眼未来，商汤科技将持续创造领先的⼤模型落地和⽣成式AI 应⽤⽣态，向通⽤⼈⼯\n智能（AGI）持续迭代，⽤我们的创新⼒为AGI 时代的到来做出努⼒。'''

    tokens = split_text(text)
    print("Tokens:", tokens)

    max_length = 1500
    combined_tokens = combine_tokens(tokens, max_length)
    print("Combined Tokens:", combined_tokens)

    print(combined_tokens.__len__())

    print([x.__len__() for x in combined_tokens])
