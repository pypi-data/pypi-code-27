'''
Created on 23 de jul de 2018

@author: koliveirab
'''

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from Pyautomators.Error import Dado_erro 
'''Este Modulo trabalha com as esperas feitas pelo WebDriverWait'''
class Aguarde_elemento():
    ''' Esta classe tem o intuito de prover conexao com o WevDriverWait'''
    def __condition(self,condicao,elemento,tipo):
        ''' Este metodo trabalha com as especificacao das esperas'''
        if(condicao is 'visivel'):
            return expected_conditions.visibility_of_element_located((tipo,elemento))
        elif(condicao is 'clicavel'):
            return expected_conditions.element_to_be_clickable((tipo,elemento))
        else:
            Erro='''Coloque uma condição valida:
                    
                    visivel:elemento visivel na tela
                    clicavel:é possivel clicar neste elemento
            '''
            raise Dado_erro(Erro)
    def aguarde_condicao(self,elemento,tipo,condicao,tempo=10,intervalo=0.5,menssagem_exception=''):
        ''' Este metodo trabalha com o aguarde trazendo uma condicao para o aguarde explicito
        retorna o elemento
        parametros:
            elemento(obrigatorio):Valor do elemento que sera esperado
            tipo(obrigatorio):Tipo de elemento que sera gerado
            condicao(obrigatorio):Condicao de espera
            tempo: valor de tentativas
            intervalo:intervalo em cada tentativa
            menssagem_exception:mensagem que sera gerada caso de erro
        Exemplo:
            aguarde_condicao('user.login','id','visivel',15,2)
            aguarde_condicao('user.login','id','clicavel')'''
        wait=WebDriverWait(self.driver,tempo,intervalo)
        
        return wait.until(self.__condition(condicao,self.__definir_by(tipo),elemento),menssagem_exception)