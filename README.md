## EAA Scientific Program Topics Visual Navigator

I have implemented a topic navigator of the Scientific programmes' topics from the EAA Congress 2025 and 2026.
The link to the Congress in Prague - https://eaa-online.org/congress-2026/scientific-programme/.  

It's very frustrating to scroll through 111 pages of the pdf file so I've utilized Qwen3-14B llm to extract text from pdf, 
clean, preprocess it, embedded it into 2D space with UMAP library and visualized it in Altair. The plot is interactive - 
you can see the topic and the authors hovering mouse to the dot. Topics semantically similar to each other are closer in the plot. 

Apparently, the tool can be improved if the conference provided also abstracts of the paper, so the embedding could be more precise and semantically rich. Also, using more advanced embedding model could improve the results.

Small disclosure: the tool is a small pet project and may contain some significant flaws: not all topics or categories 
are extracted from the pdf, the embedding didn't work quite well, or there is a mix of authors etc.