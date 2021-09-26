import pandas as pd
import config
from pandas import ExcelWriter
from pandas import ExcelFile
import re
import plotly
from textrazor import *
import networkx as nx
import matplotlib.pyplot as plt
import pickle


def sentence_parse(new_response):
    G=nx.Graph()
    d={} # Will conatain parent as key and children as value
    d_temp={}
    d_temp1={}
    for x in new_response.sentences():
        for y in x.words:
            child_list=[]
            l=()
            if(len(y.children)>0):
                t="".join(str(y.children)).split(',')
                for i in t:
                    i=i.strip()
                    t1=i.split(" ")
                    t2=t1[1].split("'")
                    child_list.append(t2[1])
                    l=(y.token,t2[1])
                    d_temp[l]=y.relation_to_parent
                    #print(y.token,t2[1],y.relation_to_parent)
                    d[y.token]=child_list
            else:
                i=y.parent
                l=(i.token,y.token)
                d_temp1[l]=y.relation_to_parent
                #print(i.token,y.token,y.relation_to_parent)
                d[y.token]=child_list

    #Graph ploting
    for i in d_temp.keys():
        l=list(i)
        x=l[0]
        y=l[1]
        if i in d_temp1:
            G.add_edge(x,y,route=d_temp1[i])
        else:
            G.add_edge(x,y,route=d_temp[i])


    stop_word=["i","me","my","myself","we","our","ours","ourselves","you","your","yours","yourself","yourselves","he","him","his","himself","she","her","hers","herself","it","its",
               "itself","they","them","their","theirs","themselves","what","which","who","whom","this","that","these","those","am","is","are","was","were",
               "be","been","being","have","has","had","having","do","does","did","doing","a","an","the","and","but","if","or","because","as","until","while","of","at","by","for","with",
               "about","against","between","into","through","during","before","after","above","below","to","from","up","down","in","out","on","off","over","under","again","further","then",
               "once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too",
               "very","s","t","can","will","just","don","should","now"]

    temp=list(d.keys())
    for i in temp:
        if(i in stop_word):
            del d[i]


    for i in d.keys():
        if(len(d[i])>0):
            temp=d[i]
            for j in temp:
                if(j in stop_word):
                    temp.remove(j)

            if(temp==None):
                d[i]=[]
            else:
                d[i]=temp

    return d


def knowledge_graph(d):

    base={}
    G=nx.Graph()

    input_1=open("data.txt","rb")
    base=pickle.load(input_1)
    input_1.close()
    #print(base)
    for i in d.keys():
        if(i in base.keys()):
            base[i]=list(set(base[i]+d[i]))
        else:
            base[i]=d[i]

    output=open("data.txt","wb")
    pickle.dump(base,output)
    #print(base)
    output.close()
    d=base
    G.add_nodes_from(list(d.keys()))
    #print(d)
    for i in d.keys():
        if(len(d[i])>0):
            for j in d[i]:
                G.add_edge(i,j)


    #pos = nx.spring_layout(G)
    #edge_labels = nx.get_edge_attributes(G, 'route')
    #nx.draw(G,pos,with_labels=True,node_size=500, node_color="pink", node_shape="s", alpha=0.5, linewidths=20)
    #nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    #plt.savefig("Graph.png")
    #plt.show()




try:
    #Authentication
    client = TextRazor(config.API_KEY)
    
    #Setting up extracts
    client.set_extractors(["entities","topics","words","phrases","dependency-trees","relations","entailments","senses","spelling"])


except TextRazorAnalysisException as ex:
    print("Failed to analyze with error: ", ex)




file = 'random_sentences.xlsx'

xl = pd.ExcelFile(file)

df1 = xl.parse('Sheet1')

k=0
for i in df1['SENTENCES']:
    k=k+1
    s=re.sub('[^ a-zA-Z0-9\'\.]', ' ', i)
    #text to analyze
    #string="""what is the national sport of japan"""
    string=s
    #print(string)
    string=string.lower()
    relation={}
    response = client.analyze(string)
    json_content = response.json
    new_response = TextRazorResponse(json_content)
    relation=sentence_parse(new_response)
    knowledge_graph(relation)
    if(k>100):
        break
