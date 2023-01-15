import networkx as nx
import numpy as np
from matplotlib import figure
import matplotlib.pyplot as plt
import random
with open('C:/Users/rheaj/OneDrive/Desktop/ekta final/MinorFinal/facebook_dataset/edges.txt') as f:
        temp_list=[tuple(line.split()) for line in f]

Edges_list=[]
for q in temp_list:
    Edges_list.append(tuple(int(item) for item in q))


Num_nodes = 4039
# Create graph
H = nx.Graph()

votes = [+1,-1]

# Create the nodes
for n in range(Num_nodes):
    if(n%2==0):
        H.add_node(n, vote=1)
    else:
        H.add_node(n,vote=-1)


H.add_edges_from(Edges_list)


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
viz_step = 100
epsilon = 0.25
def compute_c(H):
   
    Nplus = 0

    for node, data in H.nodes(data=True):
        if data['vote'] == +1:
            Nplus = Nplus + 1

    c = Nplus / H.number_of_nodes()

    return c

c_list = []
cnewlist=[]
c_list.append(compute_c(H))

# An array with all the possible nodes
Nodes = list(range(1,Num_nodes))

# Simulation loop
for i in range(Nsteps):
    qlobby = random.sample(Nodes, q)
    voter = random.sample(Nodes, 1)
    
    # sum all votes in lobby
    sum_votes = 0
    for qs in qlobby:
        sum_votes = sum_votes + H.nodes[qs]['vote']
       
    # If all the votes in lobby were the same, the voter changes his mind,
    # If all the votes are not the same, our voter flips with probability -1
    if sum_votes == q:
        H.nodes[voter[0]]['vote'] = H.nodes[qs]['vote']
    elif random.uniform(0, 1) < epsilon:
        H.nodes[voter[0]]['vote'] = -H.nodes[voter[0]]['vote']
    
    # show a snapshot of our system for every viz_step step
    if i % viz_step == 0:
        color_map = repaint(H)
        cnewlist.append(compute_c(H))
        # nx.draw(H, vmin=0, vmax=1, cmap=plt.cm.jet, node_color=color_map, with_labels=True)
        # plt.show()
        c_list.append(compute_c(H))
        

plt.figure(figsize=(20, 3))
plt.plot(np.arange(len(c_list)),c_list,'r-')
plt.xlabel('Steps')
plt.ylabel(r'$c=N_{+}/N$')
plt.title(r'steps={},$N=${},$vizstep=${},q={}'.format(Nsteps,Num_nodes,viz_step,q))
plt.show()
print(cnewlist)