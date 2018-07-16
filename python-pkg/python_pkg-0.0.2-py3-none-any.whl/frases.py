# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 09:48:53 2018

@author: ORD-PORTATIL-ASUS
"""
import nltk, csv, itertools, requests
from nltk import word_tokenize
from bs4 import BeautifulSoup
from nltk.corpus.reader.plaintext import PlaintextCorpusReader

"""Incluir el corpus para usar"""
#Directorio del corpus
corpusdir = 'LTcorpus/'
#Crear un objeto "Reader" para leer el corpus
ltcorpus = PlaintextCorpusReader(corpusdir, '.*')

#desempacar el argumento "lamba" así que NLTK puede leer las palabras en el texto
def lambda_unpack(f):
    return lambda args: f(*args)

"""La forma del URL que el código necesita"""
#Lee el html usando BeautifulSoup
url = "https://www.logitravel.co.uk/"
#Evitar el error prohibido 403
hdr = {'User-Agent': 'Mozilla/5.0'}

#Obtener la pagina web
pagina = requests.get(url, headers=hdr)
soup = BeautifulSoup(pagina.content, 'html.parser')

"""Una funcion para quitar las etiquetas html en un string usando Regular Expression"""
def remove_html_tags(text):
    import re
    limpia = re.compile('<.*?>')
    return re.sub(limpia, '', text)

"""Una funcion para crear "tokens" desde el texto "raw" """
def tokenize(raw):
    #separar el texto para crear "tokens" de las palabras
    tokens = word_tokenize(raw)
    #quitar las palabras que no existen en el corpus
    tokens = [thing for thing in tokens if thing in ltcorpus.words("all.txt")]
    return tokens

"""Buscar las palabras que tienen p dentro de otra etiqueta o la etiqueta dentro de p
    Quitar las palabras desde el texto"""
def p(string):
    #Buscar todos las palabras dentro de la etiqueta "p"
    texts = soup.find_all("p")
    #Una lista para todas las palabras en las etiquetas dentro de otras
    nested = []
    for element in texts:
        #Buscar las palabras en la etiqueta "p" que también existe en las etiquetas que tiene mas valor
        if (element.find("span") or element.find("strong") or element.find("h1")
            or element.find("h2") or element.find("h3") or element.find("h4")
            or element.find("h5") or element.find("h6") or element.find("li"))is not None:
            element = str(element)
            element = remove_html_tags(element)
            nested.append(element)
    #Buscar todas las palabras 
    outer = (soup.find_all("li") + soup.find_all("h1") + soup.find_all("h2") + 
        soup.find_all("h3") + soup.find_all("h4") + soup.find_all("h5") + 
        soup.find_all("h6") + soup.find_all("span") + soup.find_all("strong"))
    for element in outer:
        if element.find("p") is not None:
            element = str(element)
            element = remove_html_tags(element)
            nested.append(element)
    for text in string:
            for element in nested:
                if text.find(element) is not None:
                    string.remove(text)
                    break
    #Crear una string que tiene todos las frases en la lista
    return string

"""Buscar las palabras que tienen strong dentro de otra etiqueta o la etiqueta dentro de strong
    Quitar las palabras desde el texto"""
def strong(string):
    texts = soup.find_all("strong")
    nested = []
    for element in texts:
        if (element.find("span") or element.find("h1")
            or element.find("h2") or element.find("h3") or element.find("h4")
            or element.find("h5") or element.find("h6") or element.find("li"))is not None:
            element = str(element)
            element = remove_html_tags(element)
            nested.append(element)
    outer = (soup.find_all("li") + soup.find_all("h1") + soup.find_all("h2") + 
        soup.find_all("h3") + soup.find_all("h4") + soup.find_all("h5") + 
        soup.find_all("h6") + soup.find_all("span"))
    for element in outer:
        if element.find("strong") is not None:
            element = str(element)
            element = remove_html_tags(element)
            nested.append(element)
    for text in string:
            for element in nested:
                if text.find(element) is not None:
                    string.remove(text)
                    break
    #Crear una lista que tiene las frases
    return string


def span(string):
    texts = soup.find_all("span")
    nested = []
    for element in texts:
        if (element.find("h1")
            or element.find("h2") or element.find("h3") or element.find("h4")
            or element.find("h5") or element.find("h6") or element.find("li"))is not None:
            element = str(element)
            element = remove_html_tags(element)
            nested.append(element)
    outer = (soup.find_all("li") + soup.find_all("h1") + soup.find_all("h2") + 
        soup.find_all("h3") + soup.find_all("h4") + soup.find_all("h5") + 
        soup.find_all("h6"))
    for element in outer:
        if element.find("span") is not None:
            element = str(element)
            element = remove_html_tags(element)
            nested.append(element)
    for text in string:
            for element in nested:
                if text.find(element) is not None:
                    string.remove(text)
                    break
    #Crear una string que tiene todos las frases en la lista
    return string

def li(string):
    texts = soup.find_all("li")
    nested = []
    for element in texts:
        if (element.find("h1")
            or element.find("h2") or element.find("h3") or element.find("h4")
            or element.find("h5") or element.find("h6"))is not None:
            element = str(element)
            element = remove_html_tags(element)
            nested.append(element)
    outer = (soup.find_all("h1") + soup.find_all("h2") + 
        soup.find_all("h3") + soup.find_all("h4") + soup.find_all("h5") + 
        soup.find_all("h6"))
    for element in outer:
        if element.find("li") is not None:
            element = str(element)
            element = remove_html_tags(element)
            nested.append(element)
    for text in string:
            for element in nested:
                if text.find(element) is not None:
                    string.remove(text)
                    break
    #Crear una string que tiene todos las frases en la lista
    return string

def h3(string): 
    texts = soup.find_all("h3")
    nested = []
    for element in texts:
        if (element.find("h1") or element.find("h2"))is not None:
            element = str(element)
            element = remove_html_tags(element)
            nested.append(element)
    outer = soup.find_all("h1") + soup.find_all("h2")
    for element in outer:
        if element.find("h3") is not None:
            element = str(element)
            element = remove_html_tags(element)
            nested.append(element)
    for text in string:
            for element in nested:
                if text.find(element) is not None:
                    string.remove(text)
                    break
    #Crear una string que tiene todos las frases en la lista
    return string

def h2(string): 
    texts = soup.find_all("h2")
    nested = []
    for element in texts:
        if (element.find("h1")) is not None:
            element = str(element)
            element = remove_html_tags(element)
            nested.append(element)
    outer = soup.find_all("h1")
    for element in outer:
        if element.find("h2") is not None:
            element = str(element)
            element = remove_html_tags(element)
            nested.append(element)
    for text in string:
            for element in nested:
                if text.find(element) is not None:
                    string.remove(text)
                    break
    #Crear una string que tiene todos las frases en la lista
    return string

"""Una funcion para volver las textos que esta dentro de una etiqueta"""
def text_from(body, tag):
    string = []
    if tag == "img":
        texts = soup.find_all('img', alt=True)
        #Crear una lista para contener las frases
        string = []
        #Por cada texto en texts, convertir el texto a un "string" y quitar los etiquetas y ponerlo en la lista "string"
        for tag in texts: 
            item = tag["alt"]
            string.append(item) 
    else:
        #Buscar todas las frases en la etiqueta y ponerlos en una lista "texts"
        texts = soup.find_all(tag)
        #Crear una lista para contener las frases
        #Por cada texto en texts, convertir el texto a un "string", quitar las etiquetas y ponerlo en la lista "string"
        if tag == "meta":
            for tag in texts: 
                item = tag.get("content", None)
                item = str(item)
                string.append(item) 
        else:
            for t in texts:
                t = t.contents
                for thing in t:
                    thing = str(thing)
                    cleaned = remove_html_tags(thing)
                    string.append(cleaned)
            if tag == "h2":
                string = h2(string)
            if tag == "h3":
                string = h3(string)
            if tag == ("li"):
                string = li(string)
            if tag == "p":
                string = p(string)
            if tag == "strong":
                string = strong(string)
            if tag == "span":
                string = span(string)
    #Crear una string que tiene todos las frases en la lista
    words = " ".join(string)
    return words   

"""Guardar el texto que tiene la etiqueta y convertir las letras a minúscula
    y crear "tokens" desde el texto"""
rawtitle = text_from(pagina, "title").lower()
tokenstitle = tokenize(rawtitle)

rawp = text_from(pagina, "p").lower()
tokensp = tokenize(rawp)

rawli = text_from(pagina, "li").lower()
tokensli = tokenize(rawli)

rawspan = text_from(pagina, "span").lower()
tokensspan = tokenize(rawspan)

rawh1 = text_from(pagina, "h1").lower()
tokensh1 = tokenize(rawh1)

rawh2 = text_from(pagina, "h2").lower()
tokensh2 = tokenize(rawh2)

rawh3 = text_from(pagina, "h3").lower()
tokensh3 = tokenize(rawh3)

rawstrong = text_from(pagina, "strong").lower()
tokensstrong = tokenize(rawstrong)

rawmeta = text_from(pagina, "meta").lower()
tokensmeta = tokenize(rawmeta)

rawalt = text_from(pagina, "img").lower()
tokensalt = tokenize(rawalt)

"""Leer el texto y volver un "string" que incluye todas las palabras en el texto que tienen las etiqueta hx
Es diferente del "text_from(body, tag)" por que necesita incluir diferentes etiquetas
""" 
def text_from_h(body):
    #Incluir todos los tipos de "hx"
    texts =  soup.find_all("h4") + soup.find_all("h5") + soup.find_all("h6") 
    string = []
    for t in texts:
        t = t.contents
        for thing in t:
            thing = str(thing)
            cleaned = remove_html_tags(thing)
            string.append(cleaned)
    nested = []
    for element in texts:
        if (element.find("h1") or element.find("h2") or element.find("h3")) is not None:
            element = str(element)
            element = remove_html_tags(element)
            nested.append(element)
    outer = soup.find_all("h1") + soup.find_all("h2") + soup.find_all("h3")
    for element in outer:
        if (element.find("h4") or element.find("h5") or element.find("h6")) is not None:
            element = str(element)
            element = remove_html_tags(element)
            nested.append(element)
    for text in string:
        for element in nested:
            if text.find(element) is not None:
                string.remove(text)
                break
    words = " ".join(string)
    return words

rawh = text_from_h(pagina).lower()
tokensh = tokenize(rawh)

#Crear y volver la lista de los candidatos de los palabras claves
def candidates(tokens):
    #Una lista por los sustantivos
    words = []
    #una lista de las palabras que necesita quitar
    delete = []
    #Buscar todos los sustantivos y añadirlos en la lista
    for word, pos in nltk.pos_tag(tokens):
        if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS' or pos == 'VB' or pos == 'VBD'
            or pos == 'VBG' or pos == 'VBN' or pos == 'VBP' or pos == 'VBZ'):
            words.append(word)
    #Para asegurar los elemenots en la serie son únicos
    words = list(set(words))
    #Buscar los errores en "nltk.pos_tag" (hay letras solas en la lista de palabras)
    for palabra in words:
        if len(palabra) < 3:
            delete.append(palabra)
    #Quitar los errores
    l3 = [x for x in words if x not in delete]
    return l3

def phrases(tokens):
    chunker = nltk.chunk.regexp.RegexpParser(r'KT: {<JJ>* <NN.*>+ <IN>?}')
    #añadir las etiquetas parte del discuro a las palabras
    tagged_sents = nltk.pos_tag_sents(tokens for sent in tokens)
    #Crear una lista de todas las frases posibles
    all_chunks = list(itertools.chain.from_iterable(nltk.chunk.tree2conlltags(chunker.parse(tagged_sent))
                                                    for tagged_sent in tagged_sents))
    #junta los palabras "chunks" para crear una frase "chunked"
    candidates = [' '.join(word for word, pos, chunk in group).lower()
    for key, group in
    itertools.groupby(all_chunks, lambda_unpack(lambda word, pos, chunk: chunk != 'O')) if key]
    #Crear una serie por las frases
    phrases = []
    #Buscar todos las frases con mas de un palabra en la serie de las frases "chunked"  y añadirlos en una serie
    for cand in candidates:
        if " " in cand:
            phrases.append(cand)
    step = list(set(phrases))
    return step

phrasesmeta = phrases(tokensmeta)
phrasesalt = phrases(tokensalt)
phrasesh1 = phrases(tokensh1)
phrasesh2 = phrases(tokensh2)
phrasesh3 = phrases(tokensh3)
phraseshx = phrases(tokensh)
phrasesli = phrases(tokensli)
phrasesp = phrases(tokensp)
phrasesspan = phrases(tokensspan)
phrasesstrong = phrases(tokensstrong)

#Crear un archivo CSV que puede escribir en
myFile = open('frasesypalabras.csv', 'w')
"""Para escribir en el archivo CSV"""
with myFile:
    #los columnos por el archivo
    myFields = ['#', 'palabra', "etiqueta"]
    #Crear un "DictWriter", una escritor por un archivo CSV que tiene columnos
    writer = csv.DictWriter(myFile, lineterminator='\n', delimiter=';', quoting = csv.QUOTE_ALL, fieldnames=myFields)
    writer.writeheader()

    """Un funcion para escribir la informacion entre el archivo"""
    def write(tokens, raw, tag):
        for cand in candidates(tokens):
             #escribe el contento en el archivo
             n= raw.count(cand)
             #si existe en el texto, añadir al archivo CSV
             if n > 0:
                 n = str(raw.count(cand))
                 n.encode('utf-8')
                 myString = ",".join(cand)
                 myString.encode('utf-8')
                 writer.writerow({'#' : n, 'palabra': cand, "etiqueta" : tag})
                 if (tag == "h2" or tag == "h3"):
                    print(str(raw.count(cand)) + " "+ cand)
    
    """Un funcion para escribir la informacion entre el archivo"""
    def todo(tokens, step, raw, tag):
        for cand in step:
            print(str(raw.count(cand)) + " "+ cand)
            n= raw.count(cand)
            if n > 0:
                #escribe el contento entre el archivo
                n= str(raw.count(cand))
                n.encode('utf-8')
                myString = ",".join(cand)
                myString.encode('utf-8')
                writer.writerow({'#' : n, 'palabra': cand, "etiqueta" : tag})
                #quitar la frase en el texto "raw"
                raw = raw.replace(cand, " ")
        for cand in candidates(tokens):
             #escribe el contento en el archivo
             n= raw.count(cand)
             #si existe en el texto, añadir al archivo CSV
             if n > 0:
                 n = str(raw.count(cand))
                 n.encode('utf-8')
                 myString = ",".join(cand)
                 myString.encode('utf-8')
                 writer.writerow({'#' : n, 'palabra': cand, "etiqueta" : tag})
                 print(str(raw.count(cand)) + " "+ cand)
                 
    #Escribir la información de todas las etiquetas en el archivo
    write(tokenstitle, rawtitle, "title")
    todo(tokensmeta, phrasesmeta, rawmeta, "meta")
    todo(tokensalt, phrasesalt, rawalt, "img-alt")
    todo(tokensh1, phrasesh1, rawh1, "h1")
    todo(tokensh2, phrasesh2, rawh2, "h2")
    todo(tokensh3, phrasesh3, rawh3, "h3")
    todo(tokensh, phraseshx, rawh, "hx")
    todo(tokensli, phrasesli, rawli, "li")
    todo(tokensspan, phrasesspan, rawspan, "span")
    todo(tokensstrong, phrasesstrong, rawstrong, "strong")
    todo(tokensp, phrasesp, rawp, "p")