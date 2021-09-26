import networkx as nx
import matplotlib.pyplot as plt
import pickle


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


    pos = nx.spring_layout(G) 
    edge_labels = nx.get_edge_attributes(G, 'route')
    nx.draw(G,pos,with_labels=True,node_size=500, node_color="pink", node_shape="s", alpha=0.5, linewidths=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.savefig("Graph.png")
    plt.show()



