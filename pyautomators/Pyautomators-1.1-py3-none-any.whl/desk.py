#*- coding: utf-8 -*-
'''
@author: KaueBonfim
'''
import os 
from selenium import webdriver 
from Pyautomators.acoes_no_elemento import Acoes
from Pyautomators.mouse_teclado import Teclado
from Pyautomators.mouse_teclado import Mouse
from Pyautomators.elemento import Elemento
from Pyautomators.Verifica import Valida
''' Este arquivo tem o intuito dos metodos em selenium para Desktop,
    na qual os passamos um elemento chave e seu tipo e ele executa a acao descrita'''

class Desk(Acoes,Teclado,Mouse,Elemento,Valida):
    ''' Esta classe tem o intuito de prover conexão com selenium em Desktop'''
    def __init__(self,Driver_Winium,aplicacao:str):
        '''No construtor temos dois parametros sendo um obrigatorio
        
        Driver_Winium(obrigatorio):Local Aonde esta o Driver do Winium
        aplicacao(obrigatorio): Qual Aplicação será Testada
        '''
        os.startfile(Driver_Winium)
        self.driver= webdriver.Remote(command_executor="http://localhost:9999",desired_capabilities={"app": aplicacao})
        
    def fechar_programa(self):
        '''Este metodo fecha conexão com o driver. Exemplo: fechar()'''
        self.driver.close()
        os.system("TASKKILL /IM Winium.Desktop.Driver.exe")
        
    @staticmethod
    def Open_comandLine(Comand):
        '''Este metodo abre a aplicação apartir de uma linha de comando
        Exemplo:
        Open_comandLine("C:/APP/main_interface.exe")'''
        os.system(Comand)
        