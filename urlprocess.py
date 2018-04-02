from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from pyteaser import SummarizeUrl
import os
import operator

#import nltk
#nltk.download('punkt')

LANGUAGE = "English"
SENTENCES_COUNT = 3

def delete_file_contents(spath):
    open(spath, 'w').close()

#write to path
def append_file(spath,summaries,retrimChk):
    with open(spath, 'a') as s:
        try:
            if(retrimChk==0):
                for summary in summaries:
                    s.write(summary)
            else:
                s.write(summaries)
        except:
            pass
        s.close()

#condense 3 news stories into 1
def retrimmer(spath):
    parser = PlaintextParser.from_file(spath, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    i = 0
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        if i == 0:
            i = 1
            delete_file_contents(spath)
        append_file(spath,str(sentence) + '\n',1)
    print(spath + ' completed.')

def process(links):
    for s in range(1,6):
        spath = "story" + str(s) + ".txt"
        delete_file_contents(spath)
    s=1
    i=0

    for link in links:
        try:
            i+=1
            spath="story"+str(s)+".txt"
            summaries = SummarizeUrl(link)
            append_file(spath,summaries,0)
            if i == 3:
                i=0
                s+=1
                retrimmer(spath)
        except:
            pass