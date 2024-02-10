import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import math

def setSeed(): 
    seed = 0
    random.seed(seed)
    np.random.seed(seed)

def createisland(): #criando a "ilha"
    G=nx.Graph()
    nodes_to_add = {0,1,2,3,4,5,6,7,8,9,
                    10,11,12,13,14,15,16,
                    17,18,19,20,21,22,23,
                    24,25,26,27,28,29,30,31}
    G.add_nodes_from(nodes_to_add)
    edges_to_add = {(0,1),(0,2),(0,3),(3,4),(1,5),(2,20),
                    (1,6),(4,7),(4,8),(3,9),(8,9),(23,31),
                    (5,10),(5,11),(5,12),(6,12),(7,13),
                    (13,20),(13,14),(9,15),(12,20),(28,27),
                    (15,16),(15,22),(15,23),(14,22),
                    (20,30),(20,21),(20,22),(21,22),
                    (21,30),(21,31),(10,25),(10,17),
                    (11,19),(11,17),(19,30),(19,18),
                    (19,31),(18,17),(18,24),(24,25),
                    (29,25),(29,31),(29,28),(25,31),
                    (26,28),(26,27),(26,23),(26,16)}
    
    G.add_edges_from(edges_to_add)
    
    nx.draw(G,node_color="lightblue",node_size=200,with_labels=True,font_size=10,font_family="Times New Roman",font_weight="bold",width=1.5)
    plt.margins(0.2)
    return G

def inputInGraph(G):
    possible_numbers = list(range(1,31))
    G.nodes[0]['start'] = 'start'
    G.nodes[31]['end'] = 'end'
    n_numbers = 6
    allNodes = list(range(0,32))
    num_danger = random.sample(possible_numbers,n_numbers)
    for element in num_danger:
        possible_numbers.remove(element)
        if(element%2==0):
            G.nodes[element]['danger'] = 'DeathSand'
        else:
            G.nodes[element]['danger'] = 'DeathFlorest'
    
    num_checkpoints = random.sample(possible_numbers,3)
    for element in num_checkpoints:
        possible_numbers.remove(element)
        G.nodes[element]['checkpoint'] = 'checkpoint'

    num_helps =random.sample(possible_numbers,n_numbers)
    for element in num_helps:
        possible_numbers.remove(element)
        if(element%2==0):
            G.nodes[element]['help'] = 'findLife'
        else:
            G.nodes[element]['help'] = 'findWeapon'
    
    for element in possible_numbers:
         G.nodes[element]['event'] = 'none'
    
    # Apenas para verificar se a caracteristica foi adicionada
    for element in allNodes: 
        print(element)
        print(G.nodes[element])

setSeed()
G = createisland()
inputInGraph(G)
plt.show()






