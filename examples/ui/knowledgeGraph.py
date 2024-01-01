import spacy
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import re
import bs4
import requests
import networkx as nx
import matplotlib.pyplot as plt
import nltk
import graphviz
import streamlit as st

from spacy import displacy
from spacy.matcher import Matcher 
from spacy.tokens import Span 
from tqdm import tqdm
from nltk import tokenize

nlp = spacy.load('en_core_web_sm')
nltk.download('punkt')

import matplotlib as mlt
plt.ion()

def get_entities(sent):
     ## chunk 1
     ent1 = ""
     ent2 = ""

     prv_tok_dep = ""  # dependency tag of previous token in the sentence
     prv_tok_text = ""  # previous token in the sentence

     prefix = ""
     modifier = ""
                                    
     for tok in nlp(sent):
           ## chunk 2
           # if token is a punctuation mark then move on to the next token
           if tok.dep_ != "punct":
           # check: token is a compound word or not
               if tok.dep_ == "compound":
                    prefix = tok.text
                    # if the previous word was also a 'compound' then add the current word to it
                    if prv_tok_dep == "compound":
                          prefix = prv_tok_text + " " + tok.text

           # check: token is a modifier or not
           if tok.dep_.endswith("mod") == True:
                   modifier = tok.text
                   # if the previous word was also a 'compound' then add the current word to it
                   if prv_tok_dep == "compound":
                        modifier = prv_tok_text + " " + tok.text
           
           ## chunk 3
           if tok.dep_.find("subj") == True:
                ent1 = modifier + " " + prefix + " " + tok.text
                prefix = ""
                modifier = ""
                prv_tok_dep = ""
                prv_tok_text = ""

                ## chunk 4
           if tok.dep_.find("obj") == True:
                ent2 = modifier + " " + prefix + " " + tok.text
                                                                                                                               # chunk 5  
                                                                                                                               # update variables
           prv_tok_dep = tok.dep_
           prv_tok_text = tok.text
           ############################################################

     return [ent1.strip(), ent2.strip()]

def get_relation(sent):

     doc = nlp(sent)
     # Matcher class object 
     matcher = Matcher(nlp.vocab)

     #define the pattern 
     pattern = [[{'DEP':'ROOT'},
          {'DEP':'prep','OP':"?"},
          {'DEP':'agent','OP':"?"},  
          {'POS':'ADJ','OP':"?"}] ]

     #matcher.add("matching_1", None, pattern) 
     matcher.add("matching_1",pattern) 

     matches = matcher(doc)
     k = len(matches) - 1

     span = doc[matches[k][1]:matches[k][2]] 

     return(span.text)

def showKwGraph(gpText):
     graphText=gpText
     #graphText = "Sumedh is elder son of Raghu and Parimala. Sumedh's youger brother is Suchith. Sumedh and Suchith live together with Ramachandra, Shakunthala grandparents along with Raghu and Parimala. SUchith plays with Shakunthala. while Sumedh reads books these days"

     print("Sentences are ",tokenize.sent_tokenize(graphText))

     doc = nlp(graphText)

     for tok in doc:
          print(tok.text, "...", tok.dep_)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
     pd.set_option('display.max_colwidth', 200)

     candidate_sentences = pd.DataFrame({'sentence': tokenize.sent_tokenize(graphText)})

     candidate_sentences.shape
     candidate_sentences

     entity_pairs = []
     for i in tqdm(candidate_sentences["sentence"]):
          entity_pairs.append(get_entities(i))
     entity_pairs[10:20]

     relations = [get_relation(i) for i in tqdm(candidate_sentences['sentence'])]
     pd.Series(relations).value_counts()[:50]


# extract subject
     source = [i[0] for i in entity_pairs]
# extract object
     target = [i[1] for i in entity_pairs]
     kg_df = pd.DataFrame({'source':source, 'target':target, 'edge':relations})
     kg_df

     graph = graphviz.Digraph()
     for j in entity_pairs:
           graph.edge(j[0],j[1],arrowhead="none",arrowType="none")
     st.graphviz_chart(graph)

# create a directed-graph from a dataframe
     G=nx.from_pandas_edgelist(kg_df, "source", "target", 
                          edge_attr=True, create_using=nx.MultiDiGraph())

     print("mltb interactive?",mlt.is_interactive())
     plt.figure(figsize=(8,8))
     pos = nx.spring_layout(G)
     nx.draw(G, with_labels=True, node_color='red', edge_cmap=plt.cm.Blues, pos = pos)
     #plt.show() 
     plt.savefig("myKwGraph.png")
     #return(graph)     
