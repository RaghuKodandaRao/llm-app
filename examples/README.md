<b><h1>Visualize Pathway LLM Generative AI responses as a Knowlegde Graph</h1></b>

A Knowlegde Graph is a visual representation in the form of Graph consisting of Entities like Names, organizations etc formulated as nodes. These nodes are connected with edges having labels, that often depict information or ralation between nodes like Action or association words.  

In this exercise I have extended the Pathway LLM application to post the response text recived from the LLM to generate the Knwoedge graph. I promted the LLM app to "tell me something", "tell me a story", etc to generate some text, the output of the same are captured as below 

Two modules named <b><i>KnowledgeGraph</b></i> and <b><i>EnityExtraction</b></i> are newly intorduced towards Knowedge Graph extension
1. <i>EnityExtraction</i> - This has two Methods <br>
    a. <i>getEntities(SentenceText)</i> to extract Entities from a sentence.<br>
    b. <i>getRelation(SentenceText)</i> to extract Action/Association between the entities of a sentence.<br>
2. <i>KnowledgeGraph</i> has method <i>showKwGraph(SentencesText)</i> . It utilizes <i>EnityExtraction.getEntities(SentenceText)</i> to extract Entities &  <i>EnityExtraction.getRelation(SentenceText)</i> to extract entities & Labels from all the Sentences of input text. It then Displays the Knowedge Graph using this information. 

Further server.py is extended to invoke KnowledgeGraph.showKwGraph by passing the LLM response text. A "Hide Graph" enables user to hide the Graph as needed.

<h3>Demo Video :    
▶️ [Demo video](https://youtu.be/ZDSu2OsVqF0)
</h3>

<h3> Application of Knowlegde Graph generation on Pathway API</h3>

As an usecase, the enhancement of using Knowledge Graph has been applied on Pathway APIs. The approach taken, challengea faced and resolution have been documented in
https://github.com/RaghuKodandaRao/llm-app/blob/main/.github/assets/Realtime%20LLM%20JSON%20Documents%20Embedding%20with%20Pathway%20API%20Information.docx


<h3>Image: Sample Screenshot 1 </h3>

![Sample Screenshot 1](https://github.com/RaghuKodandaRao/llm-app/blob/main/.github/assets/KnowledgeGraphDemo1.PNG)

<h3>Image: Sample Screenshot 2</h3>

![Sample Screenshot 2](https://github.com/RaghuKodandaRao/llm-app/blob/main/.github/assets/KnowledgeGraphDemo2.PNG)

<h3>Image: Sample Screenshot =3</h3>

![Sample Screenshot 3](https://github.com/RaghuKodandaRao/llm-app/blob/main/.github/assets/KnowledgeGraphDemo3.PNG)

The UI as well is extended to show a "Hide Graph" button to hide the graph, the below sample shows the LLM Output ext while the graph is hidden as the user has clicked the"Hide Graph" button.
<h3>Image: Sample Screenshot 2 with "Hide Graph" clicked</h3>

![Hide Button in action](https://github.com/RaghuKodandaRao/llm-app/blob/main/.github/assets/KnowledgeGraphDemo2_Onclick_HideGraphButton.PNG)


