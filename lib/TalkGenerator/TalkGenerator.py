import os

import openai
from cls import ProtocolMean
from lib.aiwolf_share.output_tests.output_module import first_translate
from openai import OpenAI

openai.api_key = os.environ["OPENAI_API_KEY"]


class TalkGenerator:
    def __init__(self, agent_name):
        self.agent_name = agent_name

    def generate_talk(self, protocol: ProtocolMean, request=False, request_target=""):
        if request:
            protocol_text = f"REQUEST {request_target} ({str(protocol)})"
        else:
            protocol_text = str(protocol)
        first = first_translate(protocol_text)
        if first is None:
            first = "SKIP"

        # 出力
        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": "あなたは、人狼ゲームの参加者です。人狼ゲーム中で、発言したい内容が英語の一文で与えられるので、その趣旨を保ったまま、流ちょうな関西弁で話を膨らませながら発言してください。"
                    + "ただし、例外が存在するのでその場合は以下のように出力すること。"
                    + "contentが「SKIP」または「OVER」の場合、出力はそのまま、SKIPおよびOVERを返してください。"
                },
                {
                    "role": "user",
                    "content": first
                }
            ]
        )

        return completion.choices[0].message.content
