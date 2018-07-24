#*- coding: utf-8 -*-
'''
@author: KaueBonfim
'''
from Pyautomators.elemento import Elemento
import time
from selenium.webdriver.support.select import Select
from Pyautomators.Error import Elemento_erro

class Acoes(Elemento):
    ''' Esta classe tem o intuito de promover acoes que são comuns em testes baseados em Selenium,
    na qual os passamos um elemento chave e seu tipo e ele executa a acao descrita'''
    
     
    def escreve(self,elemento,conteudo,tipo,implicit=0,tempo=None):
        '''Este metodo escreve em um elemento, na qual temos cinco parametros
        
        elemento(obrigatorio): Qual é o elemento que iremos buscar para realizar a escrita, necessariamente oque invididualiza seu ekemento pela descricao.
        conteudo(obrigatorio): Conteudo na qual queremos inserir naquele elemento
        tipo(obrigatorio): O tipo para do elemento que iremos usar(id ,class, name, xpath ...)
        implicit: É o tempo que devemos esoerar o elemento aparecer, caso não apareça e gerado um erro
        tempo:É o tempo que leva para escrever cada tecla.
        
        Exemplos:
        
            dado um trecho de HTML:
            
                <input class="gsfi" id="lst-ib" maxlength="2048" name="q" autocomplete="off" title="Pesquisar" >
                
                 escreve("gsfi","QUALQUER TEXTO","class",10,0.1)
        '''
        
        element=self.elemento(elemento,tipo,implicit) 
        if(tempo is not None):
            for char in conteudo:
                element.send_keys(char) 
                time.sleep(tempo)
        else:
            element.send_keys(conteudo)
            
        return element
        
    def escreve_por_texto(self,elemento_base,tipo,conteudo,texto_referencia):
        '''Este metodo escreve em um elemento, na qual temos cinco parametros
        
        elemento(obrigatorio): Qual é o elemento que iremos buscar para realizar a escrita, necessariamente oque invididualiza seu ekemento pela descricao.
        conteudo(obrigatorio): Conteudo na qual queremos inserir naquele elemento
        tipo(obrigatorio): O tipo para do elemento que iremos usar(id ,class, name, xpath ...)
        
        tempo:É o tempo que leva para escrever cada tecla.
        
        Exemplos:
        
            dado um trecho de HTML:
            
                <a href='http://algumacoisa.com.br'>texto valor</a>
                
                 escreve("gsfi","QUALQUER TEXTO","class",10,0.1)
        '''
        elements=self.elementos_list(elemento_base, tipo)
        for element in elements:
            if(element.text==texto_referencia):
                element.send_keys(conteudo)
                break
            
    def clica_por_text(self,elemento_base,tipo,texto_referencia):
        '''Este metodo escreve em um elemento, na qual temos cinco parametros
        
        elemento_base(obrigatorio): Qual é o elemento que iremos buscar para realizar a escrita, necessariamente oque invididualiza seu elemento pela descricao.
        conteudo(obrigatorio): Conteudo na qual queremos inserir naquele elemento
        tipo(obrigatorio): O tipo para do elemento que iremos usar(id ,class, name, xpath ...)
        tempo:É o tempo que leva para escrever cada tecla.
        
        Exemplos:
        
            dado um trecho de HTML:
            
                <a href='http://algumacoisa.com.br'>texto valor</a>
                
                 clica_por_text("gsfi","QUALQUER TEXTO","class",10,0.1)
        '''
        elements=self.elementos_list(elemento_base, tipo)
        for element in elements:
            if(element.text==texto_referencia):
                element.click()
                break
            
    def clica(self,elemento,tipo=None,implicit=0):
        '''Este metodo clica em um elemento, na qual temos tres parametros
        
        elemento(obrigatorio): Qual é o elemento que iremos buscar para realizar a escrita, necessariamente oque invididualiza seu ekemento pela descricao.
        tipo(obrigatorio): O tipo para do elemento que iremos usar(id ,class, name, xpath ...)
        implicit: É o tempo que devemos esoerar o elemento aparecer, caso não apareça e gerado um erro
        
        Exemplos:
        
            dado um trecho de HTML:
            
                <input class="gsfi" id="lst-ib" maxlength="2048" name="q" autocomplete="off" title="Pesquisar" >
                
                clica("gsfi","class",10)
        '''
        
        element=self.elemento(elemento,tipo,implicit) 
        element.click()
        return element
             
    
    def pegar_texto(self,elemento,tipo,implicit=0):
        '''Este metodo retorna o texto de um elemento, na qual temos tres parametros
        
        retornara o texto que estiver no elemento
        
        elemento(obrigatorio): Qual é o elemento que iremos buscar para realizar a escrita, necessariamente oque invididualiza seu ekemento pela descricao.
        tipo(obrigatorio): O tipo para do elemento que iremos usar(id ,class, name, xpath ...)
        implicit: É o tempo que devemos esoerar o elemento aparecer, caso não apareça e gerado um erro
        Exemplos:
        
            dado um trecho de HTML:
            
                <input class="gsfi" id="lst-ib" maxlength="2048" name="q" autocomplete="off" title="Pesquisar" >Textooo</input>
                
                valor=pegar_textto("lst-ib","id",10)
                print(valor)
                >>>Textooo
        '''
        element=self.elemento(elemento,tipo,implicit) 
        return element.text
                
    def escrever_elemento_lista(self,elemento,conteudo,tipo,indice_lista:int,implicit=0,tempo:int=None):
        '''Este metodo escreve em um elemento de uma lista de elementos com o mesmo tipo e elemento, na qual temos seis parametros
        
        elemento(obrigatorio): Qual é o elemento que iremos buscar para realizar a busca na lista de elementos com a mesma descricao
        conteudo(obrigatorio): Conteudo na qual queremos inserir naquele elemento
        tipo(obrigatorio): O tipo para do elemento que iremos usar(id ,class, name, xpath ...)
        indice_lista(obrigatorio): Qual dos itens que achamos queremos usar, este sempre retorna uma lista na ordem que foi achado 
        implicit: É o tempo que devemos esoerar o elemento aparecer, caso não apareça e gerado um erro
        tempo:É o tempo que leva para escrever cada tecla.
        
        Exemplos:
        
            dado um trecho de HTML:
            
                <input name="btn" type="submit" jsaction="sf.lck">
                <input name="btn" type="submit" jsaction="sf.chk">
                
                escrever_elemento_lista("input","QUAL QUER TEXTO","tag",2,10,0.1)
        '''
        element=self.elementos_list(elemento,tipo,indice_lista,implicit)
        if(tempo is not None):
            for char in conteudo:
                element.send_keys(char) 
                time.sleep(tempo)
        else:
            element.send_keys(conteudo)
        return element      
            
    def clica_elemento_lista(self,elemento,tipo,indice_lista:int,implicit=0):
        '''Este metodo clica em um elemento de uma lista de elementos com o mesmo tipo e elemento. na qual temos quatro parametros
        
        elemento(obrigatorio): Qual é o elemento que iremos buscar para realizar a busca na lista de elementos com a mesma descricao
        indice_lista(obrigatorio): Qual dos itens que achamos queremos usar, este sempre retorna uma lista na ordem que foi achado
        tipo(obrigatorio): O tipo para do elemento que iremos usar(id ,class, name, xpath ...)
        implicit: É o tempo que devemos esoerar o elemento aparecer, caso não apareça e gerado um erro
        
        Exemplos:
        
            dado um trecho de HTML:
            
                <input name="btn" type="submit" jsaction="sf.lck">
                <input name="btn" type="submit" jsaction="sf.chk">
                
                clica_elemento_lista("input","tag",1,10)
        '''
        element=self.elementos_list(elemento,tipo,indice_lista,implicit)
        element.click()
        return element 
    
    def pegar_texto_list(self,elemento,tipo,indice_lista:int,implicit=0):
        '''Este metodo retorna o texto de um elemento de uma lista de elementos com o mesmo tipo e elemento. na qual temos quatro parametros
        
        retornara o texto que estiver no elemento
        
        elemento(obrigatorio): Qual é o elemento que iremos buscar para realizar a escrita, necessariamente oque invididualiza seu ekemento pela descricao.
        indice_lista(obrigatorio): Qual dos itens que achamos queremos usar, este sempre retorna uma lista na ordem que foi achado
        tipo(obrigatorio): O tipo para do elemento que iremos usar(id ,class, name, xpath ...)
        implicit: É o tempo que devemos esoerar o elemento aparecer, caso não apareça e gerado um erro
        
        Exemplos:
        
            dado um trecho de HTML:
            
                <input name="btn" type="submit" jsaction="sf.lck">
                <input name="btn" type="submit" jsaction="sf.chk">
                
                pegar_texto_list("input","tag",1,10)
        '''
        element=self.elementos_list(elemento,tipo,indice_lista,implicit)
        return element.text
    
    def select(self,elemento,valores_de_manipulacao=None,tipo_selecao=None,deselect=False):
        '''Este metodo trabalha com listas <Select> para preenchimento 
        parametros:
        elemento(obrigatorio): elemento do select
        valores_manipulacao: lista de elementos a ser selecionados ou deselecionados, se ele nao for passado ele seleciona todos
        tipo_selecao: tipos de selecao para ser usado que pode ser:valor,index e texto, ele nao selecionada todos 
        deselect:se True ele retira ao invez de selecionar
        
        Exemplo:
        
        select(app.elemento('user.select.list','id'),['masculino','São Paulo'],'texto')
        select(app.elemento('user.select.list','id'),['masculino','São Paulo'],'texto',True)
        '''
        Erro="""
                            Não é um tipo de seleção valido
                            Digite um tipo valido:
                            
                            index
                            valor
                            texto    
                                
                                """
        select=Select(elemento)
        if(deselect):
            if(tipo_selecao is None):
                select.deselect_all()
            else:
                for valor in valores_de_manipulacao:
                    if(tipo_selecao=='index'):
                        select.deselect_by_index(valor)
                    elif(tipo_selecao=='valor'):
                        select.deselect_by_value(valor)
                    elif(tipo_selecao=='texto'):
                        select.deselect_by_visible_text(valor)
                    else:                        
                        raise Elemento_erro(Erro)  
        else:
            if(tipo_selecao is None):
                select.select_all()
            else:
                for valor in valores_de_manipulacao:
                    if(tipo_selecao=='index'):
                        select.select_by_index(valor)
                    elif(tipo_selecao=='valor'):
                        select.select_by_value(valor)
                    elif(tipo_selecao=='texto'):
                        select.select_by_visible_text(valor)
                    
                    else:
                        raise Elemento_erro(Erro)  