import spacy
import numpy as np 
import pandas as pd 
import os
import re
import bs4
import requests
import networkx as nx
import nltk
import graphviz
import streamlit as st
import sys

from spacy import displacy
from spacy.matcher import Matcher 
from spacy.tokens import Span 
from nltk import tokenize

from EnityExtraction import getEntities
from EnityExtraction import getRelation

#######-------------------------------------#######
# Method        - showKwGraph 
# Input         - Graph text
# Returns       - Prints Knowledge graph of Entities and Relations
# Dependencies  - 
#                   1. EnityExtraction.getEntities(SentenceText) - To Obtain a List of Entities from Input Sentences
#                   2. EnityExtraction.getRelation(SentenceText) - To Obtain Asscoiation/Action of entities
#######-------------------------------------#######
def showKwGraph(gpText):
     graphText=gpText
     print("Sentences are ",tokenize.sent_tokenize(graphText))
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
     print("Graph containing \n ",kwGraph_df)
     #Visualize as graph
     graph = graphviz.Digraph()
     #using entities from DF for graph
     for index, row in kwGraph_df.iterrows():
           print("kwGraph_df values --",row['source'], row['target'], row['edge'])
           graph.edge(row['source'], row['target'], label=row['edge'], color="blue", arrowhead="none",arrowType="none") 
           
     st.graphviz_chart(graph)
          
