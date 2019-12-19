#!/usr/bin/python

from os import environ, path
from sys import stdout

from pocketsphinx import *
from sphinxbase import *

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm',  'ps_data/model/en-us')
config.set_string('-lm',   'ps_data/lm/turtle.lm.bin')
config.set_string('-dict', 'ps_data/lex/turtle.dic')
decoder = Decoder(config)

# Decode with lm
decoder.start_utt()
stream = open('ps_data/exemple/goforward.raw', 'rb')
uttbuf = stream.read(-1)
if uttbuf:
    decoder.process_raw(uttbuf, False, True)
else:
    print ("Error reading speech data")
    exit ()
decoder.end_utt()
print ('Decoding with "turtle" language:', decoder.hyp().hypstr)

print ('')
print ('--------------')
print ('')

# Switch to JSGF grammar
jsgf = Jsgf('ps_data/jsgf/goforward.gram')
rule = jsgf.get_rule('goforward.move2')
fsg = jsgf.build_fsg(rule, decoder.get_logmath(), 7.5)
fsg.writefile('goforward.fsg')

decoder.set_fsg("goforward", fsg)
decoder.set_search("goforward")

decoder.start_utt()
stream = open('ps_data/exemple/goforward.raw', 'rb')
uttbuf = stream.read(-1)
if uttbuf:
    decoder.process_raw(uttbuf, False, True)
else:
    print ("Error reading speech data")
    exit ()
decoder.end_utt()
print ('Decoding with "goforward" grammar:', decoder.hyp().hypstr)
