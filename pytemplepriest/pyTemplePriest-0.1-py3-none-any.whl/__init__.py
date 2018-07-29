# -*- coding: utf-8 -*-
import requests
from templepriest import types, testmodule



######### INFORMATION ###########
# https://hackmd.io/s/Bk3FoweyX #
#################################

__version__ = "0.1"
__author__ = "@painca / painca@tutanota.com"



class ServerError(Exception):
    pass

class api:
    """ api класс
Для получения app_token и app_id обратится к @serogaq
    Методы:
        get_user_code          - запрашивает код у юзера
        get_user_token         - возвращает user_token 
        get_user               - возвращает юзер обьект
        get_user_report_code   - запрашивает код доступа к репорту у юзера
        get_user_report_access - получает доступ к репорту
        get_user_report        - возвращает репорт обьект
        get_battle_report      - возвращает строку с результатом битвы
    """
    
    def __init__(self, app_id, app_token):
        """
        :param app_id: айди приложения
        :param app_token: токен приложения
        :return: объект класса
        """
        if not(isinstance(app_id, str)):
            raise AttributeError("Invalid app_id, str only!")
        if not(isinstance(app_token, str)):
            raise AttributeError("Invalid app_token, str only!")
        self.app_id = app_id
        self.app_token = app_token

    def make_request(self, method_name, *params):
        """
        :param method_name: имя метода
        :param *params: список параметров
        :return: ответ сервера
        """
        req = "https://serogaq.xyz/ogtapi/"+method_name+"/"+self.app_id+":"+self.app_token+"/"+"/".join([str(param) for param in params])
        response = requests.get(req).json()

        if not(response["ok"]):
            raise ServerError(response["description"])

        if "result" in response:
            return response["result"]

        return True

    def get_user_code(self, user_id):
        """
        :param user_id: айди юзера
        :return: True если сообщение отправлено юзеру, иначе False
        """
        return self.make_request("get_user_code", user_id)

    def get_user_token(self, user_id, code):
        """
        :param user_id: айди юзера
        :param code: код юзера
        :return: токен юзера
        """
        return self.make_request("get_user_token", user_id, code)["user_token"]

    def get_user(self, user_token):
        """
        :param user_token: токен юзера
        :return: user объект
        """
        return types.user(self.make_request("get_user", user_token)["user"])

    def get_user_report_code(self, user_token):
        """
        :param user_token: токен юзера
        :return: True если сообщение отправлено юзеру, иначе False
        """
        return self.make_request("get_user_report_code", user_token)

    def get_user_report_access(self, user_token, access_code):
        """
        :param user_token: токен юзера
        :param access_code: код доступа
        :return: True если приложение получило доступ, иначе False
        """
        return self.make_request("get_user_report_access", user_token, access_code)

    def get_user_report(self, user_token):
        """
        :param user_token: токен юзера
        :return: обьект репорта битвы
        """
        return types.report(self.make_request("get_user_report", user_token)['report'])

    def get_battle_result(self):
        """
        :param user_token: токен юзера
        :return: строка с результатом битвы
        """
        return self.make_request("get_battle_result")['last_battle']

