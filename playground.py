# import subprocess
# def get_current_app_package():
#     adb_command = "adb shell dumpsys window windows | findstr mCurrentFocus"
#     result = subprocess.run(adb_command, capture_output=True, text=True, shell=True)
#     print(result)
#     current_app = result.stdout.split()[-1].split('/')[0]
#     return current_app

# current_app = get_current_app_package()
# print(current_app)

import openai_proxy
import os
import base64
from mimetypes import guess_type

openai_proxy.generate.default_url = "http://api.schedule.mtc.sensetime.com:80"
my_key = "7846f1a233727507bda3aeef7cc19685"
client = openai_proxy.GptProxy(api_key=my_key)


def local_image_to_data_url(image_path):
    # Guess the MIME type of the image based on the file extension
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'  # Default MIME type if none is found

    # Read and encode the image file
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(
            image_file.read()).decode('utf-8')

    # Construct the data URL
    return f"data:{mime_type};base64,{base64_encoded_data}"

image_path = '/home/SENSETIME/luozhihao/code/AppAgent/apps/AudioRecorder/demos/demo_AudioRecorder_2024-07-29_16-48-35/raw_screenshots/demo_AudioRecorder_2024-07-29_16-48-35_1.png'
data_url = local_image_to_data_url(image_path)

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant."
    },
    {
        "role": "user",
        "content": [
                {
                    "type": "text",
                    "text": "Describe this picture:"
                },
            {
                    "type": "image_url",
                    "image_url": {
                        "url": data_url
                    }
                }
        ]
    }
]

rsp = client.generate(
    messages=messages,
    model="gpt-4o-2024-05-13-ptu",
    transaction_id="lsch_test_0001", # 同样transaction_id将被归类到同一个任务，一起统计
)   
if rsp.ok:
    print(rsp.json())
else:
    print(rsp.text)