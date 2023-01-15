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

H = nx.Graph()

votes = [+1,-1]

# Create the nodes
for n in range(Num_nodes):
    if(n%2==0):
        H.add_node(n, vote=1)
    else:
        H.add_node(n,vote=-1)

Nodes = list(range(1,Num_nodes))


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
c_list.append(compute_c(H))
cnewlist=[]
p=0.2
# Simulation loop
for i in range(Nsteps):
    # choose randomly a voter and a q-lobby
    voter = random.sample(Nodes, 1)
    print(voter)
    # the voter can't be in the q-lobby
    Edges_list_lobby = H.edges(voter)
    # qlobby = random.sample(new_list, q)
    print(Edges_list_lobby)
    lobby = []
    for l in Edges_list_lobby:
        lobby.append(l[1])
    print(lobby)
    
       
    # with probability p, the voter behaves independently
        # with probability 1-p behaves like a conformist
    if random.uniform(0, 1) < p:  # Independent
        if random.uniform(0, 1) < 0.5:
            H.nodes[voter[0]]['vote'] = -H.nodes[voter[0]]['vote']
    else:  # Conformist
        sum_votes_minus_one = 0
        sum_votes_one = 0
        for k in lobby:
            if(H.nodes[k]['vote'] == -1):
                sum_votes_minus_one += -1
            elif(H.nodes[k]['vote'] == 1):
                sum_votes_one += 1
        if(abs(sum_votes_minus_one) < sum_votes_one):
            H.nodes[voter[0]]['vote'] = 1
        else:
            H.nodes[voter[0]]['vote'] = -1
        
    # show a snapshot of our system for every viz_step step
    if i % viz_step == 0:
        color_map = repaint(H)
        cnewlist.append(compute_c(H))
        # nx.draw(H, vmin=0, vmax=1, cmap=plt.cm.jet,
        #         node_color=color_map, with_labels=True)
        # plt.title('Network for t={}'.format(i), fontsize=18)
        # plt.show()
        c_list.append(compute_c(H))

plt.figure(figsize=(20, 3))
print(c_list)
print(len(c_list))
plt.plot(np.arange(len(c_list)), c_list, 'r-')
plt.xlabel('Steps')
plt.ylabel(r'$c=N_{+}/N$')
plt.title(r'steps={},$N=${},$q=${}, $p=${}, MC_step'.format(
    Nsteps, Num_nodes, q, p))
plt.show()