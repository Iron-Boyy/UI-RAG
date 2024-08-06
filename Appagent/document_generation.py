import argparse
import ast
import json
import os
import re
import sys
import time

import prompts
from app_config import load_config
from model import OpenAIModel, QwenModel
from app_utils import print_with_color, encode_image
from call_gpt import call_openai_completion_api
import openai_proxy
import os
import base64



openai_proxy.generate.default_url = "http://api.schedule.mtc.sensetime.com:80"
my_key = "7846f1a233727507bda3aeef7cc19685"
client = openai_proxy.GptProxy(api_key=my_key)

arg_desc = "AppAgent - Human Demonstration"
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=arg_desc)
parser.add_argument("--app", required=True)
parser.add_argument("--demo", required=True)
parser.add_argument("--root_dir", default="./")
args = vars(parser.parse_args())

configs = load_config()

if configs["MODEL"] == "OpenAI":
    mllm = OpenAIModel(base_url=configs["OPENAI_API_BASE"],
                       api_key=configs["OPENAI_API_KEY"],
                       model=configs["OPENAI_API_MODEL"],
                       temperature=configs["TEMPERATURE"],
                       max_tokens=configs["MAX_TOKENS"])
elif configs["MODEL"] == "Qwen":
    mllm = QwenModel(api_key=configs["DASHSCOPE_API_KEY"],
                     model=configs["QWEN_MODEL"])
else:
    print_with_color(f"ERROR: Unsupported model type {configs['MODEL']}!", "red")
    sys.exit()

root_dir = args["root_dir"]
work_dir = os.path.join(root_dir, "apps")
if not os.path.exists(work_dir):
    os.mkdir(work_dir)
sys_doc_dir = os.path.join(work_dir, "sys_doc")
if not os.path.exists(sys_doc_dir):
    os.mkdir(sys_doc_dir)
app = args["app"]
work_dir = os.path.join(work_dir, app)
demo_dir = os.path.join(work_dir, "demos")
demo_name = args["demo"]
task_dir = os.path.join(demo_dir, demo_name)
xml_dir = os.path.join(task_dir, "xml")
raw_ss_dir = os.path.join(task_dir, "raw_screenshots")
record_path = os.path.join(task_dir, "record.txt")
task_desc_path = os.path.join(task_dir, "task_desc.txt")
if not os.path.exists(task_dir) or not os.path.exists(xml_dir) or not os.path.exists(raw_ss_dir) \
        or not os.path.exists(record_path) or not os.path.exists(task_desc_path):
    sys.exit()
log_path = os.path.join(task_dir, f"log_{app}_{demo_name}.txt")

docs_dir = os.path.join(work_dir, "demo_docs")
if not os.path.exists(docs_dir):
    os.mkdir(docs_dir)

print_with_color(f"Starting to generate documentations for the app {app} based on the demo {demo_name}", "yellow")
doc_count = 0
with open(record_path, "r") as infile:
    step = len(infile.readlines()) - 1
    infile.seek(0)
    for i in range(1, step + 1):
        img_before = os.path.join(raw_ss_dir, f"{demo_name}_{i}.png")
        img_after = os.path.join(raw_ss_dir, f"{demo_name}_{i + 1}.png")
        rec = infile.readline().strip()
        action, element_list_path = rec.split(":::")
        action_type = action.split("(")[0]
        if action_type == "click":
            action_param = re.findall(r"\((.*?)\)", action)[0]#获取括号中的内容
            with open(element_list_path, "r") as w:
                element_list = w.read()
            prompt_template = prompts.click_doc_template
            prompt = re.sub(r"<ui_element>", action_param, prompt_template)
            prompt = re.sub(r"<element_list>", element_list, prompt)
        elif action_type == "double_tap":
            action_param = re.findall(r"\((.*?)\)", action)[0]#获取括号中的内容
            with open(element_list_path, "r") as w:
                element_list = w.read()
            prompt_template = prompts.double_tap_doc_template
            prompt = re.sub(r"<ui_element>", action_param, prompt_template)
            prompt = re.sub(r"<element_list>", element_list, prompt)
        elif action_type == "long_press":
            action_param = re.findall(r"\((.*?)\)", action)[0]#获取括号中的内容
            with open(element_list_path, "r") as w:
                element_list = w.read()
            prompt_template = prompts.long_press_doc_template
            prompt = re.sub(r"<ui_element>", action_param, prompt_template)
            prompt = re.sub(r"<element_list>", element_list, prompt)
        elif action_type == "input_text":
            action_param = re.findall(r"\((.*?)\)", action)[0]#获取括号中的内容
            action_param, input_text = action_param.split(":sep:")
            with open(element_list_path, "r") as w:
                element_list = w.read()
            prompt_template = prompts.input_text_doc_template
            prompt = re.sub(r"<ui_element>", action_param, prompt_template)
            prompt = re.sub(r"<element_list>", element_list, prompt)
        elif action_type == "keyboard_enter":
            action_param = action_type
            prompt_template = prompts.sys_doc_template
            prompt = re.sub(r"<ui_element>", action_param, prompt_template)
        elif action_type == "navigate_home":
            action_param = action_type
            prompt_template = prompts.sys_doc_template
            prompt = re.sub(r"<ui_element>", action_param, prompt_template)
        elif action_type == "navigate_back":
            action_param = action_type
            prompt_template = prompts.sys_doc_template
            prompt = re.sub(r"<ui_element>", action_param, prompt_template)
        elif action_type == "open_app":
            action_param = action_type
            prompt_template = prompts.sys_doc_template
            prompt = re.sub(r"<ui_element>", action_param, prompt_template)
        elif action_type == "wait":
            action_param = action_type
            prompt_template = prompts.sys_doc_template
            prompt = re.sub(r"<ui_element>", action_param, prompt_template)
        elif action_type == "scroll":
            action_param = re.findall(r"\((.*?)\)", action)[0]#获取括号中的内容
            with open(element_list_path, "r") as w:
                element_list = w.read()
            action_param, scroll_dir = action_param.split(":sep:")
            if scroll_dir == "up" or scroll_dir == "down":
                action_type = "v_scroll"
            elif scroll_dir == "left" or scroll_dir == "right":
                action_type = "h_scroll"
            prompt_template = prompts.scroll_doc_template
            prompt = re.sub(r"<scroll_dir>", scroll_dir, prompt_template)
            prompt = re.sub(r"<ui_element>", action_param, prompt)




        
        # if action_type == "tap":
        #     prompt_template = prompts.tap_doc_template
        #     prompt = re.sub(r"<ui_element>", action_param, prompt_template)
        # elif action_type == "text":
        #     input_area, input_text = action_param.split(":sep:")
        #     prompt_template = prompts.text_doc_template
        #     prompt = re.sub(r"<ui_element>", input_area, prompt_template)
        # elif action_type == "long_press":
        #     prompt_template = prompts.long_press_doc_template
        #     prompt = re.sub(r"<ui_element>", action_param, prompt_template)
        # elif action_type == "swipe":
        #     swipe_area, swipe_dir = action_param.split(":sep:")
        #     if swipe_dir == "up" or swipe_dir == "down":
        #         action_type = "v_swipe"
        #     elif swipe_dir == "left" or swipe_dir == "right":
        #         action_type = "h_swipe"
        #     prompt_template = prompts.swipe_doc_template
        #     prompt = re.sub(r"<swipe_dir>", swipe_dir, prompt_template)
        #     prompt = re.sub(r"<ui_element>", swipe_area, prompt)
        # else:
        #     break

        task_desc = open(task_desc_path, "r").read()
        prompt = re.sub(r"<task_desc>", task_desc, prompt)

        doc_name = action_param + ".txt"
        doc_path = os.path.join(docs_dir, doc_name)
        doc_sys_path = os.path.join(sys_doc_dir,doc_name)

        if action_type == "keyboard_enter" or action_type == "navigate_home" or action_type == "navigate_back" or action_type == "open_app" or action_type == "wait":
            if os.path.exists(doc_sys_path):
                doc_content = ast.literal_eval(open(doc_sys_path).read())
                if doc_content["function"]:
                    if configs["DOC_REFINE"]:
                        suffix = re.sub(r"<old_doc>", doc_content["function"], prompts.refine_doc_suffix)
                        prompt += suffix
                        print_with_color(f"Documentation for the element {action_param} already exists. The doc will be "
                                        f"refined based on the latest demo.", "yellow")
                    else:
                        print_with_color(f"Documentation for the element {action_param} already exists. Turn on DOC_REFINE "
                                        f"in the config file if needed.", "yellow")
                        continue
            else:
                doc_content = {
                    "function": ""
                }
        else:
            if os.path.exists(doc_path):
                doc_content = ast.literal_eval(open(doc_path).read())
                if doc_content[action_type]:
                    if configs["DOC_REFINE"]:
                        suffix = re.sub(r"<old_doc>", doc_content[action_type], prompts.refine_doc_suffix)
                        prompt += suffix
                        print_with_color(f"Documentation for the element {action_param} already exists. The doc will be "
                                        f"refined based on the latest demo.", "yellow")
                    else:
                        print_with_color(f"Documentation for the element {action_param} already exists. Turn on DOC_REFINE "
                                        f"in the config file if needed.", "yellow")
                        continue
            else:
                doc_content = {
                    "click": "",
                    "double_tap": "",
                    "v_scroll": "",
                    "h_scroll": "",
                    "long_press": "",
                    "input_text": ""
                }
            

        print_with_color(f"Waiting for GPT-4o to generate documentation for the element {action_param}", "yellow")
        messages = [{
            'role': 'user',
            'content': [
                {'type': 'text', 'text': prompt},
            ],
        }]
        messages[0]['content'].append({
            'type': 'image_url',
            'image_url': {
                'url': f'data:image/jpeg;base64,{encode_image(img_before)}'
            },
        })
        messages[0]['content'].append({
            'type': 'image_url',
            'image_url': {
                'url': f'data:image/jpeg;base64,{encode_image(img_after)}'
            },
        })
        kwargs = {
        'temperature': 0.0,
        'max_tokens': 300,

        }
        # rsp = client.generate(
        #     messages=messages,
        #     model="gpt-4o-2024-05-13-ptu",
        #     transaction_id="lsch_test_0001", # 同样transaction_id将被归类到同一个任务，一起统计
        # )
        # # print(rsp.json()['data']['response_content'])
        # rsp = rsp.json()['data']['response_content']['choices'][0]['message']['content']
        rsp = call_openai_completion_api(messages, "gpt-4o", **kwargs)
        rsp = rsp[0]['content'].content
        # print(response)
        # time.sleep(5)
        # rsp = response[0]['content'].content
        # status, rsp = mllm.get_model_response(prompt, [img_before, img_after])
        if action_type == "keyboard_enter" or action_type == "navigate_home" or action_type == "navigate_back" or action_type == "open_app" or action_type == "wait":
            doc_content["function"] = rsp
            with open(log_path, "a") as logfile:
                log_item = {"step": i, "prompt": prompt, "image_before": f"{demo_name}_{i}.png",
                            "image_after": f"{demo_name}_{i + 1}.png", "response": rsp}
                logfile.write(json.dumps(log_item) + "\n")
            with open(doc_sys_path, "w") as outfile:
                outfile.write(str(doc_content))
        else:
            doc_content[action_type] = rsp
            with open(log_path, "a") as logfile:
                log_item = {"step": i, "prompt": prompt, "image_before": f"{demo_name}_{i}.png",
                            "image_after": f"{demo_name}_{i + 1}.png", "response": rsp}
                logfile.write(json.dumps(log_item) + "\n")
            with open(doc_path, "w") as outfile:
                outfile.write(str(doc_content))
        doc_count += 1
        print_with_color(f"Documentation generated and saved to {doc_path}", "yellow")
        time.sleep(configs["REQUEST_INTERVAL"])

 
flie_dir = os.listdir(docs_dir)
flie_sys_dir = os.listdir(sys_doc_dir)
flag=0
for file in flie_dir:
    with open(os.path.join(docs_dir, file), "r") as w:
        doc_content = w.read()
    doc_item = file[:-4]+":"+doc_content+"\n"
    if flag==0:
        f = open(os.path.join(work_dir, app.replace("*"," ")+".txt"),'w')
        flag=1
    else:
        f = open(os.path.join(work_dir, app.replace("*"," ")+".txt"),'a')
    f.write(doc_item)
for file in flie_sys_dir:
    with open(os.path.join(sys_doc_dir, file), "r") as w:
        doc_content = w.read()
    doc_item = file[:-4]+":"+doc_content+"\n"
    f.write(doc_item)
f.close()
with open(os.path.join(work_dir, app.replace("*"," ")+".txt"), "r") as w:
    doc_content = w.read()
INTRODUCTION_PROMPT = '''
I will provide the APP's name and it's ui elements' function description. You need to generate a detailed description for the APP. Guidelines: 1. Write a general overview of the API's purpose and functionality. 2. Use clear, concise language and avoid jargon, keeping the description under 300 tokens in length.
'''

messages=[{
        "role": "system",
        "content": INTRODUCTION_PROMPT
    },
    {
    "role": "user",
    "content": "{\"name\":"+app.replace("*"," ")+", \"ui elements description\":"+doc_content+"}"
    }]
model = "gpt-4o"
kwargs = {
    #"top_k":0.7,
    "temperature": 0.1,
    #"stream": False,
    # "max_new_tokens": 10
}

# rsp = client.generate(
#     messages=messages,
#     model="gpt-4o-2024-05-13-ptu",
#     transaction_id="lsch_test_0001", # 同样transaction_id将被归类到同一个任务，一起统计
# )
# # print(rsp.json()['data']['response_content']['choices'][0]['message']['content'])
# # response = rsp.json()['data']['response_content']['choices'][0]['message']['content']
# introduction = rsp.json()['data']['response_content']['choices'][0]['message']['content']
introduction  = call_openai_completion_api(messages, "gpt-4o", **kwargs)
introduction  = introduction[0]['content'].content
print(introduction)
f = open(os.path.join(os.path.join(root_dir, "apps/introduction"), app.replace("*"," ")+"_introduction.txt"),'w')
f.write(introduction)
print_with_color(f"Documentation generation phase completed. {doc_count} docs generated.", "yellow")
