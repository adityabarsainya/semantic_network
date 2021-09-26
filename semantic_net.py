import plotly
from textrazor import *
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import config

#Run creating inital data file
#import pickle

def entailment(new_response):
    l=[]
    t=[]
    word=[]
    meaning=[]
    prior=[]
    con_score=[]
    total=[]
    for e in new_response.entailments():
        if(len(e.matched_words)>0):
            l="".join(str(e.matched_words)).split(" ")
            t=l[1].split("'")
            #l[4] gives position of words
            word.append(t[1])
            meaning.append(e.entailed_word)
            con_score.append(e.context_score)
            total.append(e.score)
            prior.append(e.prior_score)
            #print(t[1],"------",e.entailed_word,"-------",e.context_score,"-------",e.score)

    trace = go.Table(
    header=dict(values=['Words', 'Contextual Entailment','Independent Score','Contextual Score','Total Score',],
                line = dict(color='#7D7F80'),
                fill = dict(color='#EED2EE'),
                align = ['left'] * 5),
    cells=dict(values=[word,meaning,prior,con_score,total],
               line = dict(color='#7D7F80'),
               fill = dict(color='#FFE1FF'),
               align = ['left'] * 5))
    #layout = dict(width=500, height=300)
    data = [trace]
    fig = dict(data=data) #layout=layout)
    plotly.offline.plot(fig, filename = 'meaning.html')



def word_info(new_response):
    rank=[]
    token=[]
    lem=[]
    pos=[]
    rtp=[]
    for w in new_response.words():
        rank.append(w.position)
        token.append(w.token)
        lem.append(w.lemma)
        pos.append(w.part_of_speech)
        rtp.append(w.relation_to_parent)

    trace = go.Table(
    header=dict(values=['Position','Token','Lemma','Part Of Speech','Relation to Parent',],
                line = dict(color='#7D7F80'),
                fill = dict(color='#a1c3d1'),
                align = ['left'] * 5),
    cells=dict(values=[rank,token,lem,pos,rtp],
               line = dict(color='#7D7F80'),
               fill = dict(color='#EDFAFF'),
               align = ['left'] * 5))
    #layout = dict(width=500, height=300)
    data = [trace]
    fig = dict(data=data) #layout=layout)
    plotly.offline.plot(fig, filename = 'word.html')





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


    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'route')
    nx.draw(G,pos,with_labels=True,node_size=1500, node_color="skyblue", node_shape="s", alpha=0.5, linewidths=40)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.savefig("Graph.png")
    plt.show()

    stop_word=["i","me","my","myself","we","our","ours","ourselves","you","your","yours","yourself","yourselves","he","him","his","himself","she","her","hers","herself","it","its",
               "itself","they","them","their","theirs","themselves","what","which","who","whom","this","that","these","those","am","is","are","was","were","be","been","being","have",
               "has","had","having","do","does","did","doing","a","an","the","and","but","if","or","because","as","until","while","of","at","by","for","with","about","against","between",
               "into","through","during","before","after","above","below","to","from","up","down","in","out","on","off","over","under","again","further","then","once","here","there",
               "when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too",
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

    #print(d)
    #output=open("data.txt","ab")
    #pickle.dump(d,output)
    #output.close()
    return d



def init(string):
    try:
        #Authentication
        client = TextRazor(config.API_KEY)
        plotly.tools.set_credentials_file(username=config.Plotly_USER_NAME, api_key=config.Plotly_API_KEY)
        
        #Setting up extracts
        client.set_extractors(["entities","topics","words","phrases","dependency-trees","relations","entailments","senses","spelling"])

        response = client.analyze(string)
        json_content = response.json
        new_response = TextRazorResponse(json_content)
        return new_response

    except TextRazorAnalysisException as ex:
        print("Failed to analyze with error: ", ex)
