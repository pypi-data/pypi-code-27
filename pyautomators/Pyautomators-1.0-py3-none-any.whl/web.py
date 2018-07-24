#*- coding: utf-8 -*-
'''

@author: KaueBonfim
'''

from pytractor import webdriver as protactor
from selenium import webdriver
from Pyautomators.acoes_no_elemento import Acoes
from Pyautomators.elemento import Elemento
from Pyautomators.mouse_teclado import Teclado
from Pyautomators.mouse_teclado import Mouse
from Pyautomators.Verifica import Valida
from Pyautomators.aguarde import Aguarde_elemento
from selenium.webdriver import ActionChains,common
from Pyautomators.Error import Driver_erro
''' Este arquivo prove os metodos em selenium para web,
    na qual os passamos um elemento chave e seu tipo e ele executa a acao descrita'''


class Web(Acoes,Elemento,Teclado,Mouse,Valida,Aguarde_elemento):
    ''' Esta classe tem o intuito de prover conexão com selenium em web'''
    def __init__(self,driver,path_driver=None,options=None,Angular=False):
        '''No construtor temos um parametros sendo um obrigatorio
        driver(obrigatorio):Qual dos drivers a serem usados
        path_driver:Local Aonde esta o Driver web usado
        options:as configurações passadas pelo options do driver
        Angular:Vai ser caso o site for feito inteiramente em angular
        '''
        if(Angular):
            if(driver == 'Chrome'):
                if(path_driver==None):
                    path_driver="chromedriver"
                self.driver=protactor.Chrome(executable_path=path_driver,chrome_options=options)
                
                    
            elif(driver == 'Firefox'):  
                if(path_driver==None):
                    path_driver="geckodriver"          
                self.driver=protactor.Firefox(str(path_driver),firefox_options=options)
                
                
            elif(driver == 'Ie'):    
                if(path_driver==None):
                    path_driver="IEDriverServer.exe"          
                self.driver=protactor.Ie(str(path_driver),ie_options=options)
            else:
                Erro="""
                    Não é um driver de servidor valido!
                    Digite um driver valido:
                    
                    Ie
                    Firefox
                    Chrome    
                        
                        """
                raise Driver_erro(Erro)  
        else:  
            if(driver == 'Chrome'):
                if(path_driver==None):
                    path_driver="chromedriver"
                self.driver=webdriver.Chrome(executable_path=path_driver,chrome_options=options)    
                
            elif(driver == 'Firefox'):  
                if(path_driver==None):
                    path_driver="geckodriver"          
                self.driver=webdriver.Firefox(executable_path=path_driver,firefox_options=options)
                
                
            elif(driver == 'Ie'):    
                if(path_driver==None):
                    path_driver="IEDriverServer.exe"          
                self.driver=webdriver.Ie(executable_path=path_driver,ie_options=options)
            else:
                Erro="""
                    Não é um driver de servidor valido!
                    Digite um driver valido:
                    
                    Ie
                    Firefox
                    Chrome    
                        
                        """
                raise Driver_erro(Erro)   
        self.ActionChains=ActionChains(self.driver)
        self.Alert=common.alert.Alert(self.driver)
        
    def fechar_programa(self):
        '''Este metodo fecha o driver web
        Exemplo:
        fechar_programa()''' 
        self.driver.quit()  
          
    def get_url(self):
        '''Este metodo retorna a Url atual
           Exemplo:
        get_url()''' 
        return self.driver.current_url
        
    def pagina(self,url):
        '''Este metodo vai a pagina passada para a url
           Exemplo:
        pagina('http://google.com.br')''' 
        self.driver.get(url)
        
    def maximiza(self):
        '''Este metodo maximiza a janela do driver utilizado
           Exemplo:
        maximiza()''' 
        self.driver.maximize_window()
    
    def preencher_tela(self):
        '''Este metodo preenche a tela inteira com a pagina
           Exemplo:
        preencher_tela()'''
        self.driver.fullscreen_window()
            
    def atualizar(self):
        '''Este metodo atualiza a pagina atual
           Exemplo:
        atualizar()'''
        self.driver.refresh()
        
    def voltar(self):
        '''Este metodo retorna a pagina anterior
           Exemplo:
        voltar()'''
        self.driver.back()
    
    def frente(self):
        '''Este metodo segue para a proxima pagina em sequencia
           Exemplo:
        frente()'''
        self.driver.forward()
    
    def limpar(self):
        '''Este metodo limpa o campo de um input de texto
           Exemplo:
        limpar()'''
        self.driver.clear()
        
    def get_titulo(self):
        '''Este metodo retorna o titulo atual da pagina
           Exemplo:
        get_titulo()'''
        return self.driver.title
    
    def get_navegador(self):
        '''Este metodo retorna o navegador que esta sendo usado no driver
           Exemplo:
        get_navegador()'''
        return self.driver.name
    
    def print_janela(self,path_imagem):
        '''Este metodo tira um print do conteudo atual da janela sendo usada
        
            parametros:
            path_imagem(obrigatorio):nome a imagem mais o caminho dela caso seja em outro diretorio
           Exemplo:
        print_janela('c:/teste.png')
        print_janela('teste.png')'''
        
        self.driver.get_screenshot_as_file(path_imagem)
        
    def execute_script(self,script):
        '''Este metodo executa comando javascript no console do navegador
        
            parametros:
            script(obrigatorio):o script a ser executado
           Exemplo:
        ("window.scrollTo(0, document.body.scrollHeight);")'''
        self.driver.execute_script(script)   
        