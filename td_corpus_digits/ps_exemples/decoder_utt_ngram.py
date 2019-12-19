#!/usr/bin/python

from os import environ, path


from pocketsphinx import *
from sphinxbase import *


# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm',  'ps_data/model/en-us')
config.set_string('-lm',   'ps_data/lm/en-us.lm.bin')
config.set_string('-dict', 'ps_data/lex/cmudict-en-us.dict')

# Decode streaming data.
decoder = Decoder(config)

## print ("Pronunciation for word 'hello' is ", decoder.lookup_word("hello"))
## print ("Pronunciation for word 'abcdf' is ", decoder.lookup_word("abcdf"))

decoder.start_utt()
stream = open('ps_data/exemple/goforward.raw', 'rb')
uttbuf = stream.read(-1)
if uttbuf:
    decoder.process_raw(uttbuf, False, True)
else:
    print ("Error reading speech data")
    exit ()
decoder.end_utt()

hypothesis = decoder.hyp()
logmath = decoder.get_logmath()
print ('Best hypothesis: ', hypothesis.hypstr, " model score: ", hypothesis.best_score, " confidence: ", logmath.exp(hypothesis.prob))

print ('Best hypothesis segments: ', [seg.word for seg in decoder.seg()])

# Access N best decodings.
print ('Best 10 hypothesis: ')
for best, i in zip(decoder.nbest(), range(10)):
    print (best.hypstr, best.score)

