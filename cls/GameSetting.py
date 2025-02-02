from dataclasses import dataclass

from .Role import Role


@dataclass
class GameSetting:
    enableNoAttack: bool
    enableNoExecution: bool
    enableRoleRequest: bool
    maxAttackRevote: int
    maxRevote: int
    maxSkip: int
    maxTalk: int
    maxTalkTurn: int
    maxWhisper: int
    maxWhisperTurn: int
    playerNum: int
    randomSeed: int
    roleNumMap: dict[Role: int]
    talkOnFirstDay: bool
    timeLimit: int
    validateUtterance: bool
    votableInFirstDay: bool
    voteVisible: bool
    whisperBeforeRevote: bool
