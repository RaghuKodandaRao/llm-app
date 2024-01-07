import spacy
import nltk
import sys
from spacy import displacy
from spacy.matcher import Matcher 
from spacy.tokens import Span 
from nltk import tokenize

nlp = spacy.load('en_core_web_sm')
nltk.download('punkt')

#######
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
                          prefix = PrevTokenText+" "+txtToken.text

           # Is this token a modifier
           if txtToken.dep_.endswith("mod") == True:
                   modifier = txtToken.text
                   #based on previous word being a 'compound' then add the current word to it
                   if PrevTokenDependency == "compound":
                        modifier = PrevTokenText+" "+txtToken.text
           
           if txtToken.dep_.find("subj") == True:
                FirstEntity = modifier+" "+prefix+" "+txtToken.text
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
     #print("getRelation sentence ->>", txtSentence)
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
     #print("getRelation returning ->>", span.text)
     return(span.text)