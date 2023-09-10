import sys
import time
import collections
import csv
import heapq
from datetime import datetime
import timeit

class GraphModeling(object):
    
    def __init__(self):
        self.driveDistance = collections.defaultdict(dict)     #Dictionary to hold drive distance between states
        self.striaghtDistance = collections.defaultdict(dict)  #Dictionary to hold striaght distance between states
        self.stateIndexMapping = dict()                        #Dictionary to hold State Index Map
        self.indexStateMapping = dict()                        #Dictionary to hold Index State Map
        self.driveDistancePath  = "driving.csv"                #Location of file
        self.striaghtDistancePath ="straightline.csv"          #Location of file
        self.drivingDataValsAssign()                           #Calling functions which will assign values to Dicts
        self.striaghtDataValsAssign()                          #Calling functions which will assign values to Dicts
        
    
    #Function to return state values with index
    def stateIndexMapReturn(self):
        return self.stateIndexMapping
    
    #Function to return drive distance between states
    def driveDistanceValue(self):
        return self.driveDistance
    
    #Function to return Striaght distance between states
    def striaghtDistanceValue(self):
        return self.striaghtDistance
    
    #Function to assign drive Distance
    def drivingDataValsAssign(self):
        ind = 0
        
        file = open(self.driveDistancePath, 'r')
        #Reading the Driving File
        read = csv.reader(file)
        #print(r)
        #Looping through all rows in the Excel file
        for state in read: 
            
            if ind!=0:
                #Looping through and reading each value corresponding to the row
                for i in range(1, len(state)):
                    if state[i] != '0' and state[i] !='-1':
                        #Reading the start and target state values from mapping list
                        start = self.indexStateMapping[ind]
                        target = self.indexStateMapping[i]
                        #Assigning the Drive distance value
                        self.driveDistance[start][target] = int(state[i])
                ind = ind+1

            elif ind == 0:
                #Creating a Mapping Table for index and states to iterate over
                self.stateIndexMap(state) 
                ind=ind+1
                continue
    
    #function to assign striaght line distance
    def striaghtDataValsAssign(self):
        ind = 0
        
        file = open(self.striaghtDistancePath, 'r')
        read = csv.reader(file)
        #Looping through all rows in the Excel file
        for state in read:
            if ind!=0:
                #Looping through and reading each value corresponding to the row
                for i in range(1, len(state)):
                #Reading the start and target state values from mapping list
                    start = self.indexStateMapping[ind]
                    target = self.indexStateMapping[i]
                #Assigning the Straight line distance value
                    self.striaghtDistance[start][target] = int(state[i])
                ind = ind+1
            #Skipping when index is 0 as index 0 contains state name
            elif ind == 0:
                ind=ind+1
                continue 
    #Method to create mapping between state and indexes in the data frame   
    def stateIndexMap(self, row):
        for n in range(1, len(row)):
            self.stateIndexMapping[row[n]] = n   #This forms dict like {AL:'1'}
            self.indexStateMapping[n] = row[n]   #This forms dict like {1:'AL'}
            
    
    

class BFS(object):
    
    
        def __init__(self, GraphInstance):
            self.GraphInstance = GraphInstance                                 #Object to store Graph Object
            self.parent = dict()                                               #Dictionary to keep parent information
            self.driveDistance = self.GraphInstance.driveDistanceValue()       #Variable to hold drive distance
            self.striaghtDistance = self.GraphInstance.striaghtDistanceValue() #Variable to hold striaght distance
            self.pathCost = 0                                                  #Variable to hold path cost
            self.expandedNodes=None                                            #List to hold all expanded nodes
            
        
        def BFS(self, initial, goal):
            open = []             #Initializing an open List
            visited = set()       #Initializing a List to keep track of visited nodes                                        
        
            heapq.heappush(open, [self.striaghtdistanceValue(initial, goal), initial]) #pushing initial node to open with heuristic distance
            visited.add(initial)                                                   #Add initial node to visited list
        
            while open:                                                        #Loop over all nodes in Graph
                dist, node = heapq.heappop(open)
                neighbors = self.neighbors(node)                       #Getting neighbors of current node
            
                if node != goal:                                                   #Checking if current node is the Goal
                    for neighbor, dist in neighbors.items():
                      if neighbor not in visited:                                  #If neighbor is not in visited state
                        
                        heapq.heappush(open, [self.striaghtdistanceValue(neighbor, goal), neighbor]) #pushing the child into open 
                                                                                                 #with heuristic value
                        
                        self.parent[neighbor] = node #Assigning parent value of current node(useful in backtracking from goal to initial)
                        visited.add(neighbor)        #Adding child to visited state
 
                else:
                    self.expandedNodes=visited
                    return self.targetPath(initial, goal)                           #calling function to return path
        
        def ExpandedNodes(self):
            return list(self.expandedNodes)
        
        def striaghtdistanceValue(self,start,target):    #helper function to return straight distance value
            return self.striaghtDistance[start][target]
    
        def neighbors(self, node):                       #helper function to return neighbors of current node
            return self.driveDistance[node]

        def targetPath(self, start, target):             #function to back track the path and cost value from goal to intitial
            path = []
        
            while target != start:                                    #Looping till goal reaches start
                parent = self.parent[target]
                self.pathCost += self.driveDistance[parent][target]   #Adding path cost
                path.append(target)                                   #Adding the target value into path
                target = parent                                       #Changing target to parent of current node
            
            path.append(start)                                        #adding initial node
            return path[::-1]                                         #reversing path
    
        def costOfPath(self):                                         #helper function to return path cost
            return self.pathCost


class Astar(object):
    
    
    def __init__(self, GraphInstance):
        self.GraphInstance = GraphInstance                                 #Object to store Graph Object
        self.parent = dict()                                               #Dictionary to keep parent information                                              
        self.driveDistance = self.GraphInstance.driveDistanceValue()       #Variable to hold drive distance
        self.striaghtDistance = self.GraphInstance.striaghtDistanceValue() #Variable to hold striaght distance
        self.pathCost = 0                                                  #Variable to hold path cost
        self.expandedNodes=None                                            #List to hold all expanded nodes
        
    def Astar(self, initial, goal):
        allVisitedNodes = []                                               #List to keep track of all visited nodes
        nodesInPath = set()                                                #Set to keep track of nodes in the path
        weight = dict()                                                    #Dictionary to hold travelled distance of nodes
        function = dict()                                                  #Dictionary to hold total cost function of nodes 
        
        allVisitedNodes.append(initial)                                    #Adding initial state to open list
        weight[initial] = 0                                                #Assigning travel cost to 0 for initial node
        function[initial] = self.striaghtLineValue(initial, goal)          #Adding heuristic value as total cost for initial node
        
        while len(allVisitedNodes) > 0:                                    #Traversing through all nodes in open list
            present_node = allVisitedNodes[0]                              #Current node
            ind = 0  
            for i in range(1, len(allVisitedNodes)):                       #Getting the element index with minimum cost function from open list
                if  function[allVisitedNodes[i]] != function[present_node] and function[allVisitedNodes[i]] < function[present_node]:
                    present_node = allVisitedNodes[i]
                    ind = i
                    
            allVisitedNodes.pop(ind)                                      #getting the node with least cost function
            nodesInPath.add(present_node)                                 #adding that node to the path
            
            if present_node != goal:                                      #Checking if current node is goal state
                neighbors = self.neighbors(present_node)                  #getting neighbors of current node
            else:
                self.expandedNodes=allVisitedNodes
                return self.targetPath(initial, goal)                    #Calling function to return target path
                     
            for neighbor, dist in neighbors.items():                     #getting neighbors of current node
                if neighbor in nodesInPath:                              #if child node is part of path continue
                    continue
                
                #If child is not part of path calculate f(n)=g(n)+h(n)
                cost = weight[present_node] + dist + self.striaghtLineValue(neighbor, goal)
                
                if neighbor not in weight or weight[neighbor] > weight[present_node] + dist:
                    weight[neighbor] = weight[present_node] + dist     #updating travelled cost of child with cost till parent
                    self.parent[neighbor] = present_node
                    function[neighbor] = cost
                #Add child to open list   
                allVisitedNodes.append(neighbor)
        
    def ExpandedNodes(self):
            return list(self.expandedNodes)
            
    def striaghtLineValue(self, start, target):               #helper function to return straight distance value
        return self.striaghtDistance[start][target]
    
    def driveDistanceValue(self, start, target):              #helper function to return straight distance value
        return self.driveDistance[start][target]
    
    def neighbors(self, node):                                #helper function to return neighbors of a node
        return self.driveDistance[node]
    
    def targetPath(self, start, target):                       #function to back track the path and cost value from goal to intitial
        path = []
        
        while target != start:                                 #Looping till goal reaches start
            parent = self.parent[target]
            self.pathCost += self.driveDistance[parent][target]#Adding path cost
            path.append(target)                                #Adding the target value into path
            target = parent                                    #Changing target to parent of current node
            
        path.append(start)                                     #adding initial node
        return path[::-1]                                      #reversing path
    
    def costOfPath(self):                                      #helper function to return path cost
        return self.pathCost


#Main function to call all functions
def main(initial, goal):
    graph = GraphModeling()
    states = graph.stateIndexMapReturn()
    
    if initial not in states or goal not in states:
        print("\n")      
        print("Solution path: FAILURE: NO PATH FOUND")
        print("Number of states on a path: 0")
        print("Path Cost: 0 ")
        print("Execution time: T3 Seconds")
        print("\n")
        return

    bfs = BFS(graph)
    startTimeBFS = time.perf_counter()
    pathBFS = bfs.BFS(initial, goal)
    timeEndBFS = time.perf_counter()
    bfsTime = (timeEndBFS-startTimeBFS)*10**-6
    ExpandedNodesBFS=bfs.ExpandedNodes()

    aStar = Astar(graph)
    startTimeAstar = time.perf_counter()
    pathAstar = aStar.Astar(initial, goal)
    timeEndAstar = time.perf_counter()
    aStarTime = (timeEndAstar-startTimeAstar)*10**-6
    
    ExpandedNodesAstar=aStar.ExpandedNodes()
    print("\nDonthula, Sumanth,A20519856 solution:")
    print("Initial State: ", sys.argv[1])
    print("Goal State: ", sys.argv[2])
    
    print("\nGreedy Best First Search:")
    print("Expanded Nodes: ", ExpandedNodesBFS)
    print("Number of Expanded Nodes : ", len(ExpandedNodesBFS))
    print("Solution path: ", pathBFS)
    print("Number of States on a Path: ", len(pathBFS))
    print("Path Cost: ", bfs.costOfPath())
    print("Execution time:", bfsTime ,"Seconds")

    print("\nA* Search:")
    print("Expanded Nodes: ", ExpandedNodesAstar)
    print("Number of Expanded Nodes : ", len(ExpandedNodesAstar))
    print("Solution path: ", pathAstar)
    print("Number of States on a Path: ", len(pathAstar))
    print("Path Cost: ", aStar.costOfPath())
    print("Execution time:", aStarTime ,"Seconds")
    print("\n")

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("\nERROR: Not enough or too many input arguments\n")
        exit()

    initial = sys.argv[1]
    goal = sys.argv[2]
    main(initial,goal)