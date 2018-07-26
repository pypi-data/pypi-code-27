# -*- coding: utf-8 -*-
'''
@author: KaueBonfim
'''
import http.server
import socketserver

''' Esta modulo tem o intuito de trabalhar em conjunto comunica��o entre sistemas e gera��o de Threads, 
trabalhando com cloud, processos e sistemas provedores de servi�os de nuvem e docker'''
def servidor_http(endereco:str,porta:int):
    '''Esta fun��o tem como principio gerar um servidor http'''
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer((endereco, porta), Handler)
    httpd.serve_forever()
import threading 
import thread
class Grid_Test():
    
    def __init__(self):
        self