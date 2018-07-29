# -*- coding: utf-8 -*-

######### INFORMATION #########
# Описание применяемых тайпов #
###############################

class user:
    """ Юзер класс """
    def __init__(self, jjson):
        self.original = jjson                          # Оригинал json(a)
        self.destruction = jjson["skill_destruction"]  # Разрушение
        self.durability  = jjson["skill_durability"]   # Стойкость
        self.blessing    = jjson["skill_blessing"]     # Лагословение
        self.count_pray   = jjson["count_pray"]        # Молитвы
        self.count_confes = jjson["count_confes"]      # Исповедь
        self.cookies = jjson["cookies"]                # Печеньки
        self.lvl = jjson["lvl"]                        # Уровень
        self.xp  = jjson["xp"]                         # Текущий опыт
        self.next_lvl_xp = jjson["next_lvl_xp"]        # Необходимо опты до след. уровня
        self.god_id   = jjson["god_id"]                # id(Уникальный идентификатор) бога
        self.god_name = jjson["god_name"]              # Имя бога

class report:
    """ Класс репорта """
    def __init__(self, jjson):
        self.xp = jjson['xp']         # Опыт
        self.attack = jjson['atk']    # Аттака
        self.defend = jjson['def']    # Защита
        self.target = jjson['target'] # Цель

