import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import math


class Creature:
    def __init__(self, name, life, atack, local,bornLocal):
        self.name = name
        self.life = life
        self.atack = atack
        self.local = local
        self.bornLocal = bornLocal

    def moveFor(self, local):
        self.local = local
    
    def atackCreature(self, creature):
        creature.life = creature.life - self.atack

        if creature.life <=0:
            return True

        return False
    
class Weapon:
    def __init__(self,name,atackPts,use,local):
        self.name = name
        self.atackPts= atackPts
        self.use = use
        self.local = local
    
    def brokeWeapon(self):
        if(self.use == 0 ):
            self.atackPts = 0
            return True
        else:
            return False


class LifeFruit:
    def __init__(self, name,lifePts,local):
        self.name = name
        self.lifePts = lifePts
        self.local
          

class Player(Creature):
    def __init__(self,name,life,atack,local,bornLocal):
        super().__init__(self,name,life,atack,local,bornLocal)
        self.inventory[None,None,None]
        self.weaponPoints = 0
        self.numInventory = 0
    
    def takeWeapon(self,weapon):
        if(self.numInventory <=2):
            self.inventory.append(weapon)
            self.numInventory = self.numInventory + 1
            self.atack = self.atack + weapon.atackPts
            self.weaponPoints = self.weaponPoints + weapon.atackPts
        else:
            print("inventario cheio")

    def dropWeapon(self,weapon):
        self.weaponPoints = self.weaponPoints - weapon.atackPts
        self.atack = self.atack - weapon.atackPts
        self.inventory.remove(weapon)


    def takeLifeFruit(self,fruit):
        if self.numInventory <=2:
            self.inventory.append(fruit)
            self.numInventory = self.numInventory + 1
        else:
            print("inventario cheio")
    
    def useLifeFruit(self,fruit):
        self.life = self.life + fruit.lifePts
        self.inventory.remove(fruit)

        

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
    G.nodes[0]['evento'] = 'praia'
    G.nodes[31]['evento'] = 'tesouro'
    i = 0
    n_numbers = 6
    allNodes = list(range(0,32))
    
    for node in allNodes:
        G.nodes[node]['numero'] = node

    num_danger = random.sample(possible_numbers,n_numbers)
    for element in num_danger:
        possible_numbers.remove(element)
        if(element%2==0):
            G.nodes[element]['evento'] = 'areiaMovedica'
        else:
            G.nodes[element]['evento'] = 'florestaPerigosa'
    
    num_checkpoints = random.sample(possible_numbers,3)
    for element in num_checkpoints:
        possible_numbers.remove(element)
        G.nodes[element]['evento'] = 'checkpoint'

    num_helps =random.sample(possible_numbers,n_numbers)
    for element in num_helps:
        possible_numbers.remove(element)
        if(element%2==0):
            G.nodes[element]['evento'] = 'fruta'
        else:
            G.nodes[element]['evento'] = 'arma'
    
    for element in possible_numbers:
         G.nodes[element]['evento'] = 'none'
    
    
    # Apenas para verificar se a caracteristica foi adicionada
    for nodes in G.nodes(data=True): 
        print(nodes)
    
    inputXY(G)

    return G


def inputXY(G):
    G.nodes[0]["x"] = 131
    G.nodes[0]["y"] = 542
    G.nodes[1]["x"] = 244
    G.nodes[1]["y"] = 455
    G.nodes[2]["x"] = 455
    G.nodes[2]["y"] = 467
    G.nodes[3]["x"] = 476
    G.nodes[3]["y"] = 574
    G.nodes[4]["x"] = 599
    G.nodes[4]["y"] = 434
    G.nodes[5]["x"] = 230
    G.nodes[5]["y"] = 333
    G.nodes[6]["x"] = 393
    G.nodes[6]["y"] = 351
    G.nodes[7]["x"] = 660
    G.nodes[7]["y"] = 349
    G.nodes[8]["x"] = 627
    G.nodes[8]["y"] = 494
    G.nodes[9]["x"] = 689
    G.nodes[9]["y"] = 538
    G.nodes[10]["x"] = 251
    G.nodes[10]["y"] = 245
    G.nodes[11]["x"] = 391
    G.nodes[11]["y"] = 252
    G.nodes[12]["x"] = 511
    G.nodes[12]["y"] = 282
    G.nodes[13]["x"] = 767
    G.nodes[13]["y"] = 366
    G.nodes[14]["x"] = 833
    G.nodes[14]["y"] = 335
    G.nodes[15]["x"] = 886
    G.nodes[15]["y"] = 557
    G.nodes[16]["x"] = 1072
    G.nodes[16]["y"] = 380
    G.nodes[17]["x"] = 330
    G.nodes[17]["y"] = 175
    G.nodes[18]["x"] = 394
    G.nodes[18]["y"] = 129
    G.nodes[19]["x"] = 549
    G.nodes[19]["y"] = 195
    G.nodes[20]["x"] = 625
    G.nodes[20]["y"] = 263
    G.nodes[21]["x"] = 731
    G.nodes[21]["y"] = 251
    G.nodes[22]["x"] = 893
    G.nodes[22]["y"] = 301
    G.nodes[23]["x"] = 974
    G.nodes[23]["y"] = 308
    G.nodes[24]["x"] = 291
    G.nodes[24]["y"] = 109
    G.nodes[25]["x"] = 193
    G.nodes[25]["y"] = 78
    G.nodes[26]["x"] = 1028
    G.nodes[26]["y"] = 257
    G.nodes[27]["x"] = 1037
    G.nodes[27]["y"] = 139
    G.nodes[28]["x"] = 924
    G.nodes[28]["y"] = 99
    G.nodes[29]["x"] = 782
    G.nodes[29]["y"] = 111
    G.nodes[30]["x"] = 653
    G.nodes[30]["y"] = 203
    G.nodes[31]["x"] = 776
    G.nodes[31]["y"] = 165

setSeed()
G = createisland()
inputInGraph(G)


comeco = G[0]
termino = G[31]

#caminho = random.choice(list(nx.all_simple_paths(G,)))


if G.nodes[0]['evento'] == 'praia':
    print('deu certo adiconar caracteriscas ao nó')

#plt.show()






