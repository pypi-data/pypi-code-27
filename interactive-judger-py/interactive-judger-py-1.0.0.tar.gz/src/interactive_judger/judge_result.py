from enum import Enum


class Result(Enum):
    AC = 'Accepted'
    WA = 'Wrong Answer'
    TLE = 'Time Limit Exceeded'
    RE = 'Runtime Error'
    PE = 'Presentation Error'
    JE = 'Judgement Error'
