import spacy
import numpy as np 
import pandas as pd 
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
from nltk import tokenize

nlp = spacy.load('en_core_web_sm')
nltk.download('punkt')

#######-------------------------------------#######
# Method    - getEntities 
# Input     - One Sentence text
# Returns   - 2 entities as FirstEntity and SecondEntity extracted from the input sentence
#######-------------------------------------#######
def getEntities(txtSentence):
     ## Firstchunk 
     FirstEntity = ""
     SecondEntity = ""

     PrevTokenDependency = "" 
     PrevTokenText = ""  

     prefix = ""
     modifier = ""
                                    
     for txtToken in nlp(txtSentence):
           # Skip punctutaion tokens
           if txtToken.dep_ != "punct":
           # is this token a compound word?
               if txtToken.dep_ == "compound":
                    prefix = txtToken.text
                    #based on previous word being a 'compound' then add the current word to it
                    if PrevTokenDependency == "compound":
                          prefix = PrevTokenText + " " + txtToken.text

           # check: token is a modifier or not
           if txtToken.dep_.endswith("mod") == True:
                   modifier = txtToken.text
                   #based on previous word being a 'compound' then add the current word to it
                   if PrevTokenDependency == "compound":
                        modifier = PrevTokenText + " " + txtToken.text
           
           if txtToken.dep_.find("subj") == True:
                FirstEntity = modifier + " " + prefix + " " + txtToken.text
                prefix = ""
                modifier = ""
                PrevTokenDependency = ""
                PrevTokenText = ""

           if txtToken.dep_.find("obj") == True:
                SecondEntity = modifier + " " + prefix + " " + txtToken.text
           
           # update variables
           PrevTokenDependency = txtToken.dep_
           PrevTokenText = txtToken.text
           ############################################################
     return [FirstEntity.strip(), SecondEntity.strip()]

#######-------------------------------------#######
# Method    - getRelation 
# Input     - One Sentence text
# Returns   - returns relation label of 2 entities from the input sentence
#######-------------------------------------#######
def getRelation(txtSentence):
     print("getRelation sentence ->>", txtSentence)
     objDocument = nlp(txtSentence)
     matcher = Matcher(nlp.vocab)

     #pattern definition for graph
     pattern = [[{'DEP':'ROOT'},
          {'DEP':'prep','OP':"?"},
          {'DEP':'agent','OP':"?"},  
          {'POS':'ADJ','OP':"?"}] ]

     matcher.add("matching_1",pattern) 
     matches = matcher(objDocument)
     k = len(matches) - 1

     span = objDocument[matches[k][1]:matches[k][2]] 
     print("getRelation returning ->>", span.text)
     return(span.text)

#######-------------------------------------#######
# Method    - showKwGraph 
# Input     - Graph text
# Returns   - Prints Knowledge graph of Entities and Relations
#######-------------------------------------#######
def showKwGraph(gpText):
     graphText=gpText
     #print("Sentences are ",tokenize.sent_tokenize(graphText))
     pd.set_option('display.max_colwidth', 150)

     #A text may have many sentences, extract each sentence & add to data frame
     AllSentences = pd.DataFrame({'sentence': tokenize.sent_tokenize(graphText)})
     AllSentences.shape
     
     #For each sentence extract entity pairs
     arrEntityPairs = []
     for i in AllSentences["sentence"]:
          arrEntityPairs.append(getEntities(i))
     
     #Extract relation with entities
     arrRelations = [getRelation(i) for i in AllSentences['sentence']]
        
     # extract Source entity from entity pairs
     arrSrcEntities = [i[0] for i in arrEntityPairs]
     # extract target entity from entity pairs
     arrTargetEntities = [i[1] for i in arrEntityPairs]
     kwGraph_df = pd.DataFrame({'source':arrSrcEntities, 'target':arrTargetEntities, 'edge':arrRelations})
     
     #Visualize as graph
     graph = graphviz.Digraph()
     #using entities from DF for graph
     for index, row in kwGraph_df.iterrows():
           print("kwGraph_df values --",row['source'], row['target'], row['edge'])
           graph.edge(row['source'], row['target'], label=row['edge'], color="blue", arrowhead="none",arrowType="none") 
           
     st.graphviz_chart(graph)
    
    #Works in commandline , but not interactive have commented
    # create a directed-graph from a dataframe
    # G=nx.from_pandas_edgelist(kwGraph_df, "source", "target", 
    #                      edge_attr=True, create_using=nx.MultiDiGraph())

    #print("mltb interactive?",mlt.is_interactive())
     #plt.figure(figsize=(8,8))
     #pos = nx.spring_layout(G)
     #nx.draw(G, with_labels=True, node_color='red', edge_cmap=plt.cm.Blues, pos = pos)
     #plt.show() 
     #save image to view during debugging
     #plt.savefig("myKwGraph.png")
          
