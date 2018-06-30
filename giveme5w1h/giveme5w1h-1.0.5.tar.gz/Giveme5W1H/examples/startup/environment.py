from Giveme5W1H.examples.startup.util import StartupHelper


def start():
    h = StartupHelper()
    h.do_command('CoreNLP',
                 'java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000 -props edu/stanford/nlp/coref/properties/neural-english.properties',
                 'stanford-corenlp-full-2017-06-09')
    h.forever()


start()

#
