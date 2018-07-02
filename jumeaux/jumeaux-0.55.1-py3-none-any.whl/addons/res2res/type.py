# -*- coding:utf-8 -*-
from owlmixin import OwlMixin, TOption, TList

from jumeaux.addons.res2res import Res2ResExecutor
from jumeaux.addons.utils import when_filter
from jumeaux.logger import Logger
from jumeaux.models import Res2ResAddOnPayload, Response, Request

logger: Logger = Logger(__name__)
LOG_PREFIX = "[res2res/type]"


class Condition(OwlMixin):
    type: str
    when: TOption[str]


class Config(OwlMixin):
    conditions: TList[Condition]


def apply_first_condition(res: Response, req: Request, conditions: TList[Condition]) -> Response:
    # TODO: remove TOption (owlmixin... find)
    condition: TOption[Condition] = TOption(
        conditions.find(
            lambda c: c.when.map(lambda x: when_filter(x, {'req': req, 'res': res})).get_or(True)
        )
    )
    if condition.is_none():
        return res

    return Response.from_dict(
        {
            "body": res.body,
            "type": condition.get().type,
            "encoding": res.encoding.get(),
            "headers": res.headers,
            "url": res.url,
            "status_code": res.status_code,
            "elapsed": res.elapsed,
            "elapsed_sec": res.elapsed_sec,
        },
    )


class Executor(Res2ResExecutor):
    def __init__(self, config: dict) -> None:
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: Res2ResAddOnPayload) -> Res2ResAddOnPayload:
        return Res2ResAddOnPayload.from_dict({
            "req": payload.req,
            "response": apply_first_condition(payload.response, payload.req, self.config.conditions),
        })
