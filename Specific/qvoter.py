import networkx as nx
import numpy as np
from matplotlib import figure
import matplotlib.pyplot as plt
import random

# G = nx.complete_graph(20)
# len(G)
# G.size()
# nx.draw(G, with_labels=True, font_weight='bold')
# Number of nodes
Num_nodes = 30

# Create graph
H = nx.Graph()

votes = [+1,-1]

# Create the nodes
for n in range(Num_nodes):
    if(n%2==0):
        H.add_node(n, vote=1)
    else:
        H.add_node(n,vote=-1)

# Add one and only one connection for each pair of nodes
for p in range(len(H)):
     for j in range(30):
        if(p==0 or j==0 ):
            H.add_edge(p,j)
        elif((p!=j )and (p%j==0 or j%p==0)):
            H.add_edge(p,j)


def repaint(H):
    color_map = []
    for node, data in H.nodes(data=True):
        if data['vote'] == +1:
            color_map.append(0.25)  # blue color
        elif data['vote'] == -1:
            color_map.append(0.9)  # red color
            
    return color_map

# Initialization
Nsteps = 1000
q = 7
viz_step = 500
epsilon = 0.25
def compute_c(H):
   
    Nplus = 0

    for node, data in H.nodes(data=True):
        if data['vote'] == +1:
            Nplus = Nplus + 1

    c = Nplus / H.number_of_nodes()

    return c

c_list = []
c_list.append(compute_c(H))

# An array with all the possible nodes
Nodes = list(range(1,Num_nodes))

# Simulation loop
for i in range(Nsteps):
    voter=[]
    voter.append(Nodes[1])
    # print(voter)
    Edges_list=H.edges(voter)
    
    # print(Edges_list)
    lobby =[]
    for l in Edges_list:
        lobby.append(l[1])
    # print(lobby)
    sum_votes=0
    for qs in lobby:
        sum_votes = sum_votes + H.nodes[qs]['vote']
       
    # If all the votes in lobby were the same, the voter changes his mind,
    # If all the votes are not the same, our voter flips with probability -1
    if sum_votes == q:
        
        H.nodes[voter[0]]['vote'] = H.nodes[qs]['vote']
    elif random.uniform(0, 1) < epsilon:
        H.nodes[voter[0]]['vote'] = -H.nodes[voter[0]]['vote']
    c_list.append(compute_c(H))
    # show a snapshot of our system for every viz_step step
    if i % viz_step == 0:
        color_map = repaint(H)
        nx.draw(H, vmin=0, vmax=1, cmap=plt.cm.jet, node_color=color_map, with_labels=True)
        plt.show()
        

plt.figure(figsize=(20, 3))
plt.plot(np.arange(len(c_list)),c_list,'r-')
plt.xlabel('Steps')
plt.ylabel(r'$c=N_{+}/N$')
plt.title(r'steps={},$N=${},$vizstep=${},q={}'.format(Nsteps,Num_nodes,viz_step,q))
plt.show()