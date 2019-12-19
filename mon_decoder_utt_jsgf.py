#!/usr/bin/python

from os import environ, path
from sys import stdout

from pocketsphinx import *
from sphinxbase import *

def wer(hypothesis, reference):
    substitutionCost = 0
    insertionCost = 1
    supressionCost = 1
    m = len(hypothesis)
    n = len(reference)
    d = [x[:] for x in [[0] * 10] * 10]
    for i in range(0, m):
        for j in range(0, n):
            d[i][j] = 0
    for i in range(0, m):
        d[i][0] = i
    for j in range(0, n):
        d[0][j] = j
    for j in range(1, n):
        for i in range(1, m):
            if (hypothesis[i] == reference[j]):
                substitutionCost = 0
            else:
                substitutionCost = 1
            d[i][j] = min(d[i-1][j] + supressionCost, min(d[i]  [j-1] + insertionCost, d[i-1][j-1] + substitutionCost))
    return d[m-1][n-1] / max(m, n)


# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-logfn','nul')
config.set_string('-hmm',  'ps_data/model/en-us')
config.set_string('-lm',   'ps_data/lm/turtle.lm.bin')
config.set_string('-dict', 'numbers.dic')
decoder = Decoder(config)

# Switch to JSGF grammar
jsgf = Jsgf('numbers.gram')
rule = jsgf.get_rule('numbers.move')
fsg = jsgf.build_fsg(rule, decoder.get_logmath(), 7.5)
fsg.writefile('numbers.fsg')

decoder.set_fsg("numbers", fsg)
decoder.set_search("numbers")

# Set path 

mon_path = 'td_corpus_digits'
mon_bruit = ['SNR05dB','SNR15dB','SNR25dB','SNR35dB']
mon_locuteur = ['man','woman','boy','girl']
mon_nbdigit = [200,100,100]
mon_nbdigit_file = ['seq1digit_','seq3digits_','seq5digits_']
wertot = 0
nbgood = 0
nbtot = 0

for le_bruit in mon_bruit:
    print(le_bruit)
    if le_bruit == 'SNR35dB':
        for le_locuteur in mon_locuteur:
            print(le_locuteur)
            for nbdigit in range(0,3):
                wertot = 0
                nbgood = 0
                nbtot = 0   
                for indice in range(1,mon_nbdigit[nbdigit]+1):
                    decoder.start_utt()
                    the_ultimate_path = mon_path + '/' + le_bruit + '/' + le_locuteur + '/' + mon_nbdigit_file[nbdigit] + str(mon_nbdigit[nbdigit]) + '_files' + '/' + le_bruit + '_' + le_locuteur + '_' + mon_nbdigit_file[nbdigit]
                    if indice < 10:
                        the_ultimate_path += '00'
                    elif indice < 100:
                        the_ultimate_path += '0'
                    else :
                        the_ultimate_path += ''
                    the_ultimate_path += '' + str(indice)
                    stream = open(the_ultimate_path + '.raw', 'rb')
                    uttbuf = stream.read(-1)
                    if uttbuf:
                        decoder.process_raw(uttbuf, False, True)
                    else:
                        print ("Error reading speech data")
                        exit ()
                    decoder.end_utt()
                    stream = open(the_ultimate_path + '.ref', 'r')
                    uttbuf = stream.read(-1)
                    if decoder.hyp() != None:
                        """print ('Decoding with "numbers" grammar:', decoder.hyp().hypstr , 
                        '\tReal numbers :' , uttbuf.split('\n')[0] , 
                        '\tThe prediction is' , decoder.hyp().hypstr == uttbuf.split('\n')[0])"""
                        if decoder.hyp().hypstr == uttbuf.split('\n')[0]:
                            #print(wer(decoder.hyp().hypstr.split(' '), uttbuf.split('\n')[0].split(' ')))
                            nbgood += 1
                        wertot += wer(decoder.hyp().hypstr.split(' '), uttbuf.split('\n')[0].split(' '))
                    nbtot += 1
                print('Nb ggod : ', nbgood , ' Nb tot : ' , nbtot , ' Error : ' , 1-(nbgood / nbtot), " WER : %1.2f" % (wertot/nbtot))
    else: 
    # Traitement man only 
        print(mon_locuteur[0])
        for nbdigit in range(0,3):
            nbgood = 0
            wertot = 0
            nbtot = 0   
            for indice in range(1,mon_nbdigit[nbdigit]+1):
                decoder.start_utt()
                the_ultimate_path = mon_path + '/' + le_bruit + '/' + mon_locuteur[0] + '/' + mon_nbdigit_file[nbdigit] + str(mon_nbdigit[nbdigit]) + '_files' + '/' + le_bruit + '_' + mon_locuteur[0] + '_' + mon_nbdigit_file[nbdigit]
                if indice < 10:
                    the_ultimate_path += '00'
                elif indice < 100:
                    the_ultimate_path += '0'
                else :
                    the_ultimate_path += ''
                the_ultimate_path += '' + str(indice)
                stream = open(the_ultimate_path + '.raw', 'rb')
                uttbuf = stream.read(-1)
                if uttbuf:
                    decoder.process_raw(uttbuf, False, True)
                else:
                    print ("Error reading speech data")
                    exit ()
                decoder.end_utt()
                stream = open(the_ultimate_path + '.ref', 'r')
                uttbuf = stream.read(-1)
                if decoder.hyp() != None:
                    """print ('Decoding with "numbers" grammar:', decoder.hyp().hypstr , 
                    '\tReal numbers :' , uttbuf.split('\n')[0] , 
                    '\tThe prediction is' , decoder.hyp().hypstr == uttbuf.split('\n')[0])"""
                    if decoder.hyp().hypstr == uttbuf.split('\n')[0]:
                        nbgood += 1
                    wertot += wer(decoder.hyp().hypstr.split(' '), uttbuf.split('\n')[0].split(' ')) 
                    #print(wer(decoder.hyp().hypstr.split(' '), uttbuf.split('\n')[0].split(' ')))
                nbtot += 1
            print('Nb ggod : ', nbgood , ' Nb tot : ' , nbtot , ' Error : ' , 1-(nbgood / nbtot), " WER : %1.2f" % (wertot/nbtot))