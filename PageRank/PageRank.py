import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random
import time

def create_graph(filename):
    
##    This function accepts a filename string as a parameter.
##    This filename contains edgelist in the format of "node1 node2"
##    which indicates the former node points to the latter. Using
##    read_esgelist function of the networkx library , we can easily
##    make a drected graph from the given information. The function
##    returns a directed graph.
    
    g=nx.read_edgelist(filename,create_using=nx.DiGraph())
    n=nx.number_of_nodes(g)
    g=nx.stochastic_graph(g)
    return g,n

def create_adjacency_matrix(G,N):

##    Accepts the created DiGraph object as a parameter and constructs an
##    adjacency matrix from that DiGraph object. Also this adjacency
##    matrix is converted to the transition matrix needed for the
##    Markov chain multiplication later. This function also returns a list
##    of dead_ends in the graph.
    
    a=np.zeros(N*N).reshape(N,N)
    no_ones_per_row=dict.fromkeys(range(N),0)
    for i in G.edges():
        r=int(i[0])-1
        c=int(i[1])-1
        a[r,c]=1
        no_ones_per_row[r]+=1
    for i in range(N):
        if no_ones_per_row[i]!=0 :
            for j in range(N):
                a[i,j]=float(a[i,j])/float(no_ones_per_row[i])
    dead_ends=[]
    for i in no_ones_per_row :
        if no_ones_per_row[i]==0 :
            dead_ends.append(i)

    return a,dead_ends

def fix_dead_ends(A,N,dead_ends):

##    The created transition matrix has a lot of dead ends which need to be
##    fixed. Thus this function accepts the transition matrix to be
##    modified and a list of the dead end nodes. Invisible links are added from
##    the dead ends to every other page in the graph. In the transition matrix
##    probability of following random invisible link from dead ends is uniformly
##    deistributed.
    
    d=np.zeros(N).reshape(N,1) 
    for i in dead_ends :
        d[i]=1.0
    w=np.ones(N)/N  ####
    w=w.reshape(1,6012)
    s=A+np.dot(d,w)
    return s

def create_google_matrix(S,N,beta,p):

##    Accepts the transition matrix made so far , taxation parameter and personalization
##    vector and finally creates the google transition matrix.
    
    ones=np.ones(N).reshape(N,1)
    temp=np.dot(ones,p)
    GM=beta*S + (1-beta)*temp
    return GM

def return_answer(GM,sv,number_of_iter):

##    performs the matrix multiplication for a specified number of iterations
##    and then returns the answer vector.
    
    data_history=[]
    data_history.append(sv)
    for i in range(number_of_iter):
        sv=np.dot(sv,GM)
        data_history.append(sv)
    return sv,data_history

def plot_graph(G,ans):

##    constructs the required graph by selecting some randomly connected nodes.
    
    nl=[]
    for i in range(20):
        nl.append(str(random.randint(1,100)))
    H=G.subgraph(nl)
    ns=[]
    for i in H.nodes():
        ns.append(answer[0][int(i)-1]*100000)
    nx.draw_networkx(H,pos=nx.spring_layout(H),node_size=ns)
    plt.show()

def plot_graph_max(data_histry,max_ind):
    
    x=[i for i in range(1,11)]
    y=[]
    for i in range(11):
        y.append(data_history[i][0][max_ind])
    plt.plot(x,y)
    plt.show()

G,N=create_graph("hollins.txt")
A,dead_ends=create_adjacency_matrix(G,N)
S=fix_dead_ends(A,N,dead_ends)
personalization_vector=np.full((1,N),1.0/N).reshape(1,N)
beta=0.85
GM=create_google_matrix(S,N,beta,personalization_vector)
sv=np.full((1,N),1.0/N)
no_of_iter=10
answer,data_history=return_answer(GM,sv,no_of_iter)
plot_graph(G,answer)
max_ind=np.argmax(answer[0])
plot_graph_max(data_history,max_ind)
