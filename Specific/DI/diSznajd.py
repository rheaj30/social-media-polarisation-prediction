import networkx as nx
import numpy as np
from matplotlib import figure
import matplotlib.pyplot as plt
import random

Num_nodes = 30

H = nx.DiGraph()

votes = [+1,-1]
q = 5
# Create the nodes
for n in range(Num_nodes):
    if(n%2==0):
        H.add_node(n, vote=1)
    else:
        H.add_node(n,vote=-1)

Nodes = list(range(1,Num_nodes))

# To print the random choice of voter's vote
# for nl in Nodes:
#     print(H.nodes[nl]['vote']) 

# Add one and only one connection for each pair of nodes
for p in range(len(H)):
    for j in range(30):
        if(p==0 or j==0 ):
            H.add_edge(p,j)
        elif((p!=j )and (p%j==0 or j%p==0)):
            H.add_edge(p,j)
            # print(p,j)

def repaint(H):
    
    color_map = []
    for node, data in H.nodes(data=True):
        if data['vote'] == +1:
            color_map.append(0.25)  # blue color
        elif data['vote'] == -1:
            color_map.append(0.9)  # red color
            
    return color_map


def compute_c(H):
   
    Nplus = 0

    for node, data in H.nodes(data=True):
        if data['vote'] == +1:
            Nplus = Nplus + 1

    c = Nplus / H.number_of_nodes()

    return c
# print(c)
c_list=[]
c_list.append(compute_c(H))

# Initialization
Nsteps = 10000
viz_step = 5000

# An array with all the possible nodes
Nodes = list(range(1,Num_nodes))
# Simulation loop
for i in range(Nsteps):
    voter1=[]
    voter1.append(Nodes[1])
    # print(voter1)
    Edges_list1=H.edges(voter1)
    
    # print(Edges_list1)
    lobby1 =[]
    for l in Edges_list1:
        lobby1.append(l[1])
    # print(lobby1)
    voter2=[]
    voter2.append(lobby1[1])
    # print(voter2)
    Edges_list2=H.edges(voter2)
    lobby2 =[]
    for m in Edges_list2:
        lobby2.append(m[1])
    # print(lobby2)
    if(H.nodes[voter1[0]]['vote']==H.nodes[voter2[0]]['vote']):
        for m in lobby1:
            H.nodes[m]['vote']=H.nodes[voter2[0]]['vote']
        for m in lobby2:
            H.nodes[m]['vote']=H.nodes[voter1[0]]['vote']
    else:
        for m in lobby1:
            H.nodes[m]['vote']=H.nodes[voter2[0]]['vote']
        for m in lobby2:
            H.nodes[m]['vote']=H.nodes[voter1[0]]['vote']
        common_neighbour = [c for c in lobby1 if c in lobby2]
        # print(common_neighbour)
        for d in common_neighbour:
            H.nodes[d]['vote']=-H.nodes[d]['vote']
    c_list.append(compute_c(H))


    # show a snapshot of our system for every viz_step step
    if i % viz_step == 0:
        color_map = repaint(H)
        nx.draw(H, vmin=0, vmax=1, cmap=plt.cm.jet, node_color=color_map, with_labels=True)
        plt.show()

plt.figure(figsize=(20, 3))
plt.plot(np.arange(len(c_list)),c_list,'r-')
plt.xlabel('Monte Carlo Steps')
plt.ylabel(r'$c=N_{+}/N$')
plt.title(r'steps={},$N=${},$vizstep=${},q={}'.format(Nsteps,Num_nodes,viz_step,q))
plt.show()