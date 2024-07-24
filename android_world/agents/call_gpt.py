import openai
from openai import AzureOpenAI
import os
import copy
import pkg_resources
from packaging import version
import random
import requests
import json


last_openai_request_cost = 0.0


def get_last_openai_request_cost():
    return last_openai_request_cost


USE_AZURE = True

if USE_AZURE:
    API_VERSION = "2023-12-01-preview"
    API_VERSION = "2024-02-15-preview"
    if not (
        os.environ.get("AZURE_OPENAI_ENDPOINT")
        and os.environ.get("AZURE_OPENAI_KEY")
        and os.environ.get("AZURE_API_VERSION")
    ):
        model_to_region_and_tpm = {
            "gpt-4-vision-preview": [("us-w", 10), ("se-c", 10)],
            "gpt-4-1106-preview": [
                ("us-w", 80),
                ("in-s", 150),
                ("no-e", 150),
                ("se-c", 150),
                ("au-e", 80),
                ("ca-e", 80),
                ("us-e2", 80),
                ("fr-c", 80),
                ("uk-s", 80),
            ],
            "gpt-35-turbo-1106": [("us-w", 100), ("in-s", 100)],
            "gpt-35-turbo-1106": [("us-w", 100), ("in-s", 100)],
            "gpt-4o":[("us-w",10)]
            # https://agent-us-w.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview
        }
        region_to_api_key = {
            "us-w": "c0a247839a2e40809c2c8724432c3a91",
            "in-s": "ac5342dba8bf451e903ba938b51fb13f",
            "se-c": "11dd2fc8bec5423f856671503705e6aa",
            "no-e": "34a52444d4914db2b2dc117bd0b64bc5",
            "au-e": "bf8f0a85eee34c4d8dda3e20b18e3c96",
            "ca-e": "2e8b797a8b3b4a729c1f606c502ad964",
            "us-e2": "d58dc9db5f92428daf74e783bdb01682",
            "fr-c": "cc43e0c8ae4742a6a68df2a2ab3c5a64",
            "uk-s": "8692fcaf0cb04f6b8e3e79fc6b8f1f41",
        }
        # example: {model: [(client1, weight1), (client2, weight2), ...)]}
        model_to_client_and_tpm = {
            model: [
                (
                    AzureOpenAI(
                        azure_endpoint=f"https://agent-{region}.openai.azure.com/openai/deployments/{model}/chat/completions?api-version={API_VERSION}",
                        api_key=region_to_api_key[region],
                        api_version=API_VERSION,
                    ),
                    tpm,
                )
                for region, tpm in model_to_region_and_tpm[model]
            ]
            for model in model_to_region_and_tpm.keys()
        }
    else:
        # TODO
        client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version=os.environ.get("AZURE_API_VERSION"),
        )
else:
    # TODO 待验证
    if not os.environ.get("OPENAI_API_KEY"):
        openai.api_key = "fk221315-UIp73CUkRiNI7dzlBS9OEdxrTjkgNsaX"
        # openai.api_base = "https://openai.api2d.net/v1"
        try:
            if version.parse(pkg_resources.get_distribution("openai").version) < version.parse("1"):
                openai.api_base = "https://oa.ai01.org/v1"
            else:
                openai.base_url = "https://oa.ai01.org/v1/"
        except pkg_resources.DistributionNotFound:
            print("openai is not installed.")



if not os.environ.get("OPENAI_API_KEY"):
    openai.api_key = "fk221315-UIp73CUkRiNI7dzlBS9OEdxrTjkgNsaX"
    # openai.api_base = "https://openai.api2d.net/v1"
    try:
        if version.parse(pkg_resources.get_distribution("openai").version) < version.parse("1"):
            openai.api_base = "https://oa.ai01.org/v1"
        else:
            openai.base_url = "https://oa.ai01.org/v1/"
    except pkg_resources.DistributionNotFound:
        print("openai is not installed.")



def api(model):
    if USE_AZURE:
        client = random.choices(
            population=[client for client, _ in model_to_client_and_tpm[model]],
            weights=[tpm for _, tpm in model_to_client_and_tpm[model]],
            k=1,
        )[0]
    return client.api_key
    

def call_openai_completion_api(messages, model="gpt-4", **kwargs):
    messages_for_log = copy.deepcopy(messages)
    for msg in messages_for_log:
        for content in msg:
            if isinstance(content, dict) and content.get("image_url"):
                content["image_url"] = "data:image/jpeg;base64, ..."
    # print(messages_for_log)

    if version.parse(pkg_resources.get_distribution("openai").version) < version.parse("1"):
        # 暂不维护openai<1.0
        response = openai.ChatCompletion.create(model=model, messages=messages, **kwargs)
    else:
        if USE_AZURE:
            client = random.choices(
                population=[client for client, _ in model_to_client_and_tpm[model]],
                weights=[tpm for _, tpm in model_to_client_and_tpm[model]],
                k=1,
            )[0]
            # print(client.chat.completions.create(model="gpt-4o", messages=messages, **kwargs))
            try:
                response = client.chat.completions.create(model=model, messages=messages, **kwargs)
            except:
                response = ""
                return response
        else:
            # TODO 待验证
            response = openai.chat.completions.create(model=model, messages=messages, **kwargs)
    # return response.json()['choices'][0]['message']['content'].strip()
    if kwargs.get("stream") == True:
        collected_messages = []
        for chunk in response:
            chunk_message = chunk["choices"][0]["delta"]  # extract the message
            collected_messages.append(chunk_message)  # save the message
            # print(chunk_message.get('content', ''))
        full_reply_content = "".join([m.get("content", "") for m in collected_messages])
        print(full_reply_content)
        return full_reply_content
    # print(response)
    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens
    # gpt4-turbo cost
    global last_openai_request_cost
    last_openai_request_cost = (0.01 * prompt_tokens + 0.03 * completion_tokens) / 1000


    return {"role": "assistant", "content": response.choices[0].message},0,completion_tokens



openai_model_list = [
    "gpt-4",
    "gpt-4-32k",
    "gpt-4-1106-preview",
    "gpt-4-vision-preview",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k",
    "gpt-3.5-turbo-1106",
    "text-embedding-ada-002",
]

