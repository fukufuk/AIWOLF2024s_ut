import re

from cls import ProtocolMean
from lib.aiwolf_share.main_classes import Comment, Sentence


def convert_to_protocol(nl: str, talker: str, me: str) -> list[ProtocolMean]:
    """自然言語をプロトコルに変換

    Args:
        nl (str): 自然言語の他人の発話

    Returns:
        str: プロトコル
    """
    # ここに処理を追加
    if nl == "SKIP":
        return [ProtocolMean(False, "SKIP", None, None)]
    elif nl == "Over":
        return [ProtocolMean(False, "Over", None, None)]
    else:
        print("### sentence", nl)
        comment = Comment(nl, talker=f"Agent[0{talker}]", me=f"Agent[0{me}]")
        protocol_list: list[Sentence] = comment.remark_to_protocol(ruizido_check=False, check_gpt=False)
        print("### protocol_list", len(protocol_list))
        [print(sentence) for sentence in protocol_list]
        protocol_list = [ProtocolMean(
            not_flag="NOT" in protocol.verb,
            action=protocol.verb.split(' ')[-1],
            talk_subject=me,
            talk_object=protocol.agent,
            role=protocol.role,
            team=protocol.team,
            mention_flag=comment.flag,
            original_text=nl
        ) for protocol in protocol_list]
        return protocol_list


# プロトコルのみでやり取りするようの関数
def get_protocol_meaning(protocol: str, index: str) -> ProtocolMean:
    single_actions = ["SUSPECT", "VOTE", "DIVINATION", "AGREE"]
    double_actions = ["ESTIMATE", "CO", "DIVINED"]

    if protocol == "SKIP":
        return ProtocolMean(False, "SKIP", None, None)
    elif protocol == "Over":
        return ProtocolMean(False, "Over", None, None)

    protocol_parts = protocol.split(' ')
    if protocol_parts[0] == 'NOT':
        not_flag = True
        protocol_parts.pop(0)
    else:
        not_flag = False

    print(protocol_parts)
    if protocol_parts[0] in single_actions or protocol_parts[0] in double_actions:
        protocol_parts.insert(0, f"Agent[0{index}]")
    if protocol_parts[1] in single_actions:
        talk_subject = _judge_agent_name(protocol_parts[0])
        talk_object = _judge_agent_name(protocol_parts[2])
        protocol_meaning = ProtocolMean(not_flag, protocol_parts[1],
                                        talk_subject, talk_object)
    elif protocol_parts[1] in double_actions:
        if protocol_parts == ['ANY', 'CO', 'ANY']:
            protocol_meaning = ProtocolMean(not_flag, protocol_parts[1], "ANY",
                                            "ANY", None, protocol_parts[0])
        elif protocol_parts[1] == ["DIVINED"]:
            talk_subject = _judge_agent_name(protocol_parts[0])
            talk_object = _judge_agent_name(protocol_parts[2])
            protocol_meaning = ProtocolMean(not_flag, protocol_parts[1], talk_subject,
                                            talk_object, None, protocol_parts[3])
        else:
            talk_subject = _judge_agent_name(protocol_parts[0])
            talk_object = _judge_agent_name(protocol_parts[2])
            protocol_meaning = ProtocolMean(not_flag, protocol_parts[1], talk_subject,
                                            talk_object, protocol_parts[3])
    else:
        print("存在しないActionです。", protocol_parts)
        return ProtocolMean(False, "SKIP", None, None)
    return protocol_meaning


def _judge_agent_name(name: str):
    """Agent[01]~Agent[05]の名前かどうか判定し、そうなら1~5の数字を返す。そうでないならそのまま返す。"""
    if re.match(r"Agent\[0[1-5]\]", name):
        return name[-2]
    else:
        return name
