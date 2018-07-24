'''
@author: KaueBonfim
'''
import http.server
import socketserver
''' Esta modulo tem o intuito de trabalhar em conjunto comunicação entre sistemas e geração de Threads, 
trabalhando com cloud, processos e sistemas provedores de serviços de nuvem e docker'''
def servidor_http(endereco:str,porta:int):
    '''Esta função tem como principio gerar um servidor http'''
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer((endereco, porta), Handler)
    httpd.serve_forever()