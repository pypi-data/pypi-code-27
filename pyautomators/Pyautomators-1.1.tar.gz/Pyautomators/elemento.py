#*- coding: utf-8 -*-
'''
@author: KaueBonfim
'''
'''Este Arquivo trabalha com a procura de elementos apartir acessiveis no Selenium'''
from Pyautomators.Error import Elemento_erro
from selenium.webdriver.common.by import By

class Elemento():
    
    '''Esta classe trabalha com a procura de elementos'''
    def __definir_by(self,elemento):
            if(elemento=='id'):
                return By.ID
            elif(elemento=='class'):
                return By.CLASS_NAME
            elif(elemento=='xpath'):
                return By.XPATH
            elif(elemento=='name'):
                return By.NAME
            elif(elemento=='tag'):
                return By.TAG_NAME
            elif(elemento=='partial_link'):
                return By.PARTIAL_LINK_TEXT
            elif(elemento=='link'):
                return By.LINK_TEXT
            elif(elemento=='css'):
                return By.CSS_SELECTOR
            else:
                Erro="""
                Escolha um valor de elemento Valido
                lista de elementos:
                id:    Desk,Web,Mobile
                name:    Desk,Web,Mobile
                class:    Desk,Web,Mobile
                xpath:    Desk,Web,Mobile
                link:    Web
                tag:    Web,Mobile
                css:    Web,Mobile
                partial_link:    Web
                
                
                """
                raise Elemento_erro(Erro)
    def elemento(self,elemento,tipo,implicit=0):
        r'''Esta procura um elemento e retorna o objeto do elemento
        parametros:
        elemento(obrigatorio):elemento que deve ser procurado
        tipo(obrigatorio): tipo do elemento que sera procurado
        implicit: É o tempo que devemos esoerar o elemento aparecer, caso não apareça e gerado um erro
        
        Exemplos:
        elemento("id.user","id",10)
        elemento("class_user_login","class",1)
        elemento("login","name")
        
       lista de elementos:
        
        id:    Desk,Web,Mobile    <form id="loginForm"> = 'loginForm'
        
        name:    Desk,Web,Mobile    <input name="username" type="text" /> = 'username'
        
        class:    Desk,Web,Mobile     <p class="content">Site content goes here.</p> = 'content'
        
        xpath:    Desk,Web,Mobile <html>                    =    '/html/body/form[1]' ou '//form[1]' ou '//form[@id='loginForm']'
                                     <body>
                                      <form id="loginForm">
                                      
        link:    Web        <a href="continue.html">Continue</a> = 'Continue'
        
        tag:    Web,Mobile    <h1>Welcome</h1> = 'h1'
        
        css:    Web,Mobile    <p class="content">Site content goes here.</p> = 'p.content'
        
        partial_link:    Web    <a href="continue.html">Continue</a> = 'Conti'
        
        android:    Mobile 
        
        ios:    Mobile
        
        binding:    Web(Angular) <span>{{person.name}}</span> = 'person.name' ou <span ng-bind="person.email"></span> = 'person.email'
        
        model:    Web(Angular) <input type="text" ng-model="person.name"/> = 'person.name'       
        '''    
        self.driver.implicitly_wait(implicit)
        if(tipo == 'id'):
            element=self.driver.find_element_by_id(elemento)
        elif(tipo == 'name'):
            element=self.driver.find_element_by_name(elemento) 
        elif(tipo == 'class'):            
            element=self.driver.find_element_by_class_name(elemento) 
        elif(tipo == 'xpath'):            
            element=self.driver.find_element_by_xpath(elemento) 
        elif(tipo == 'link'):            
            element=self.driver.find_element_by_link_text(elemento) 
        elif(tipo == 'tag'):            
            element=self.driver.find_element_by_tag_name(elemento) 
        elif(tipo == 'css'):            
            element=self.driver.find_element_by_css_selector(elemento) 
        elif(tipo == 'partial_link'):            
            element=self.driver.find_element_by_partial_link_text(elemento) 
        elif(tipo=='android'):
            element=self.driver.find_element_by_android_uiautomator(elemento) 
        elif(elemento=='ios'):
            element=self.driver.find_element_by_ios_uiautomation(elemento)
        elif(tipo=='binding'):
            element=self.driver.find_element_by_binding(elemento)
        elif(tipo=='model'):
            element=self.driver.find_element_by_model(elemento)
        elif(tipo=='accessibility_id'):
            element=self.driver.find_element_by_accessibility_id(elemento)
        else:
            Erro="""
                Escolha um valor de elemento Valido
                lista de elementos:
                id:    Desk,Web,Mobile
                name:    Desk,Web,Mobile
                class:    Desk,Web,Mobile
                xpath:    Desk,Web,Mobile
                link:    Web
                tag:    Web,Mobile
                css:    Web,Mobile
                partial_link:    Web
                andorid:    Mobile
                ios:    Mobile
                binding:    Web(Angular)
                model:    Web(Angular)
                
                """
            raise Elemento_erro(Erro)
        return element
      
    def elemento_list(self,elemento,tipo,indice_lista,implicit=0):
        '''Esta procura um elemento  dentro de uma lista de elementos com o mesmo parametro
        parametros:
        elemento(obrigatorio):elemento que deve ser procurado
        tipo(obrigatorio): tipo do elemento que sera procurado
        indice_lista(obrigatorio):Indice de ordem do elemento na lista
        implicit: É o tempo que devemos esoerar o elemento aparecer, caso não apareça e gerado um erro
        
        Exemplos:
        elemento_list("id.user","id",0,10)
        elemento_list("class_user_login","class",3,1)
        elemento_list("login","name",2)
        
        lista de elementos:
        
        id:    Desk,Web,Mobile    <form id="loginForm"> = 'loginForm'
        
        name:    Desk,Web,Mobile    <input name="username" type="text" /> = 'username'
        
        class:    Desk,Web,Mobile     <p class="content">Site content goes here.</p> = 'content'
        
        xpath:    Desk,Web,Mobile <html>                    =    '/html/body/form[1]' ou '//form[1]' ou '//form[@id='loginForm']'
                                     <body>
                                      <form id="loginForm">
                                      
        link:    Web        <a href="continue.html">Continue</a> = 'Continue'
        
        tag:    Web,Mobile    <h1>Welcome</h1> = 'h1'
        
        css:    Web,Mobile    <p class="content">Site content goes here.</p> = 'p.content'
        
        partial_link:    Web    <a href="continue.html">Continue</a> = 'Conti'
        
        android:    Mobile 
        
        ios:    Mobile
        
        binding:    Web(Angular) <span>{{person.name}}</span> = 'person.name' ou <span ng-bind="person.email"></span> = 'person.email'
        
        model:    Web(Angular) <input type="text" ng-model="person.name"/> = 'person.name'
         
        '''
        self.driver.implicitly_wait(implicit)
        elements=self.elementos_list(elemento, tipo, implicit)
        element=elements[indice_lista]
        return element
    
    def elementos_list(self,elemento,tipo,implicit=0):
        '''Esta procura todos os elementos de elementos com o mesmo parametro
        parametros:
        elemento(obrigatorio):elemento que deve ser procurado
        tipo(obrigatorio): tipo do elemento que sera procurado
        implicit: É o tempo que devemos esoerar o elemento aparecer, caso não apareça e gerado um erro
        
        Exemplos:
        elementos_list("id.user","id",10)
        elementos_list("class_user_login","class",1)
        elementos_list("login","name")
        
        lista de elementos:
        
        id:    Desk,Web,Mobile    <form id="loginForm"> = 'loginForm'
        
        name:    Desk,Web,Mobile    <input name="username" type="text" /> = 'username'
        
        class:    Desk,Web,Mobile     <p class="content">Site content goes here.</p> = 'content'
        
        xpath:    Desk,Web,Mobile <html>                    =    '/html/body/form[1]' ou '//form[1]' ou '//form[@id='loginForm']'
                                     <body>
                                      <form id="loginForm">
                                      
        link:    Web        <a href="continue.html">Continue</a> = 'Continue'
        
        tag:    Web,Mobile    <h1>Welcome</h1> = 'h1'
        
        css:    Web,Mobile    <p class="content">Site content goes here.</p> = 'p.content'
        
        partial_link:    Web    <a href="continue.html">Continue</a> = 'Conti'
        
        android:    Mobile 
        
        ios:    Mobile
        
        binding:    Web(Angular) <span>{{person.name}}</span> = 'person.name' ou <span ng-bind="person.email"></span> = 'person.email'
        
        model:    Web(Angular) <input type="text" ng-model="person.name"/> = 'person.name'
         
        '''
        self.driver.implicitly_wait(implicit)
        if(tipo == 'id'):           
            elements=self.driver.find_elements_by_id(elemento)  
        elif(tipo == 'name'):
            elements=self.driver.find_elements_by_name(elemento)
        elif(tipo == 'class'):            
            elements=self.driver.find_elements_by_class_name(elemento)
        elif(tipo == 'xpath'):            
            elements=self.driver.find_elements_by_xpath(elemento)
        elif(tipo == 'link'):            
            elements=self.driver.find_elements_by_link_text(elemento)
        elif(tipo == 'tag'):            
            elements=self.driver.find_elements_by_tag_name(elemento)
        elif(tipo == 'text'):            
            elements=self.driver.find_elements_by_partial_link_text(elemento)
        elif(tipo == 'css'):            
            elements=self.driver.find_elements_by_css_selector(elemento)
        elif(tipo=='android'):
            elements=self.driver.find_elements_by_android_uiautomator(elemento) 
        elif(elemento=='ios'):
            elements=self.driver.find_elements_by_ios_uiautomation(elemento)
        elif(tipo=='binding'):
            elements=self.driver.find_elements_by_binding(elemento)
        elif(tipo=='model'):
            elements=self.driver.find_elements_by_model(elemento)
        elif(tipo=='accessibility_id'):
            elements=self.driver.find_elements_by_accessibility_id(elemento)
        else:
            Erro="""
                Escolha um valor de elemento Valido
                lista de elementos:
                id:    Desk,Web,Mobile
                name:    Desk,Web,Mobile
                class:    Desk,Web,Mobile
                xpath:    Desk,Web,Mobile
                link:    Web
                tag:    Web,Mobile
                css:    Web,Mobile
                partial_link:    Web
                andorid:    Mobile
                ios:    Mobile
                binding:    Web(Angular)
                model:    Web(Angular)
                
                """
            raise Elemento_erro(Erro)
        return elements