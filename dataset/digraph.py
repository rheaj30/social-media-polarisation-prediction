import networkx as nx
import numpy as np
from matplotlib import figure
import matplotlib.pyplot as plt
import random
import numpy as np

with open('C:/Users/rheaj/OneDrive/Desktop/ekta final/MinorFinal/facebook_dataset/edges.txt')  as f:
        temp_list=[tuple(line.split()) for line in f]

Edges_list=[]
for q in temp_list:
    Edges_list.append(tuple(int(item) for item in q))


Num_nodes = 4039

H = nx.DiGraph()

votes = [+1,-1]

# Create the nodes
for n in range(Num_nodes):
    if(n%2==0):
        H.add_node(n, vote=1)
    else:
        H.add_node(n,vote=-1)

Nodes = list(range(1,Num_nodes))


H.add_edges_from(Edges_list)
# nx.draw(H,with_labels=True)
# plt.show()
def repaint(H):
    
    color_map = []
    for node, data in H.nodes(data=True):
        if data['vote'] == +1:
            color_map.append(0.25)  # blue color
        elif data['vote'] == -1:
            color_map.append(0.9)  # red color
            
    return color_map

Nsteps = 1000
viz_step = 100

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

for i in range(Nsteps):
    voter = random.sample(Nodes, 1)
    # print(voter)
    # print(type(H.edges()))
    Edges_list_lobby=H.edges(voter)
    
    # print(Edges_list_lobby)
    lobby =[]
    for l in Edges_list_lobby:
        lobby.append(l[1])
    # print(lobby)

    # sum all votes in lobby
    # sum_votes = 0
    # for qs in lobby:
    #     sum_votes = sum_votes + H.nodes[qs]['vote']
    # # print(abs(sum_votes))
       
    # If all the votes in lobby were the same, the voter changes his mind,
    # If all the votes are not the same, our voter flips with probability -1
    sum_votes_minus_one=0
    sum_votes_one=0
    for k in lobby:
        if(H.nodes[k]['vote']==-1):
            sum_votes_minus_one+=-1
        elif(H.nodes[k]['vote']==1):
            sum_votes_one+=1
    print(sum_votes_one)
    print(sum_votes_minus_one)
    if(abs(sum_votes_minus_one)<sum_votes_one):
        H.nodes[voter[0]]['vote'] = 1
    else:
        H.nodes[voter[0]]['vote'] = -1

    # show a snapshot of our system for every viz_step step
    if i % viz_step == 0:
        color_map = repaint(H)
        # nx.draw(H, vmin=0, vmax=1, cmap=plt.cm.jet, node_color=color_map, with_labels=True)
        # plt.show()
        cnewlist.append(compute_c(H))
        c_list.append(compute_c(H))

plt.figure(figsize=(20, 3))
plt.plot(np.arange(len(c_list)),c_list,'r-')
plt.xlabel('Steps')
plt.ylabel(r'$c=N_{+}/N$')
plt.title(r'steps={},$N=${},$vizstep=${}'.format(Nsteps,Num_nodes,viz_step))
plt.show()
print(cnewlist)