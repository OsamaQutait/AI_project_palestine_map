
print("\n\t\t\t\t\t\t\tSearch Algorithms for Route Navigation\n\n\t\t\t\t\t\t\t{Welcome to our program}")
print("\n\t\t(Note that : you can enter an infinite number pf starts and goals)\n")

while True:                                # keep going in the while loop to let user use the program many times

 # make a grapgh to read the input file BFS that contain the citites that are connected together to design our graph
 # and it is undirected graph this file will be used for BFS and UCS
 def BFS_graph():
  vertex_list = [] #array of 20 element that contain the names of the cities
  adj_list = []    # array is made of 20 element every element in it is an array to know for each city which cities is directly connected with it
  sub_adj_list = [] # we will use it to make dictinary
  with open("BFS.txt", "r") as input_file:        #choose the input file and intialize it to be read file
    for line in input_file:            # for loop to read all input file data
        line = line.split("##")       # we will split the informations using ## so when there ## mean new value or city
        del line[-1]
        if len(line) == 1 or len(line) == 0:
            break
        else:
            if line[0] not in vertex_list:
             if sub_adj_list:
                adj_list.append(sub_adj_list)
             sub_adj_list = []
             vertex_list.append(line[0])
             sub_adj_list.append([line[1], line[2]])
            else:
                sub_adj_list.append([line[1], line[2]])
    adj_list.append(sub_adj_list)
  map = {}
  for i in range(len(vertex_list)):
    sub_map = {}
    for j in range(len(adj_list[i])):
        sub_map[adj_list[i][j][0]] = adj_list[i][j][1]
    map[vertex_list[i]] = sub_map
  return map


 # first algorithm bfs that uses queue idea and it is uninformed search algorithm

 def Bredth_First_Search(Start_city,Goal_city,Algorithm_graph):
    # Intialize a queue to save the cities in it (we used queue since BFS use FIF0)
    BFS_queue = []
    BFS_queue.append([Start_city])       # put the first city into the queue and save it in the queue to be used later
    # while loop to keep visiting all cities depend on the algorithm from the start until the goal found
    while BFS_queue:
        # get the first path from the queue
        path = BFS_queue.pop(0)
        goal = path[-1]          # get and save the goal that is the last node from the path
        # path found
        if goal == Goal_city:  # when the goal equal goal city then we found our goal so we will return it and stop searching
            return path        # goal found stop searching
        # new path and push it into the queue
        for adjacent in Algorithm_graph.get(goal, []):
            new_road = list(path)        # intitialize new path to be sure that all possible paths will be checked until we find our goal
            new_road.append(adjacent)
            BFS_queue.append(new_road)


 def BFS_graph1():
     vertex_list = []  #array of 20 element that contain the names of the cities
     adj_list = []      # array is made of 20 element every element in it is an array to know for each city which cities is directly connected with it
     sub_adj_list = []
     with open("BFS.txt", "r") as input_file:    # choose the input file and intialize it to be read file

         for line in input_file:                     # for loop to read all input file data
             line = line.split("##")                     # Split the data from the file and append it to a new list, then cut the data based on ##) .
                                                        # we will split the informations using ## so when there ## mean new value or city
             del line[-1]
             if len(line) == 1 or len(line) == 0:
                 break
             else:
                 if line[0] not in vertex_list:
                     if sub_adj_list:
                         adj_list.append(sub_adj_list)
                     sub_adj_list = []
                     vertex_list.append(line[0])            # Add item in items array.
                     sub_adj_list.append(line[1])           # Add item in items array.
                 else:
                     sub_adj_list.append(line[1])
         adj_list.append(sub_adj_list)
     map = {}
     for i in range(len(vertex_list)):
         map[vertex_list[i]] = adj_list[i]
     return map

# this function will be used to print all the visited cities from start to goal the from this visited cities we can get the best path

 def bfs_visited(graph, node, goal):  # function for BFS
     visited = []  # List for visited nodes.
     queue = []  # Initialize a queue
     visited.append(node)
     queue.append(node)
     while queue:  # Creating loop to visit each node
         m = queue.pop(0)
         for neighbour in graph[m]:
             if goal in visited:
                 break
             if neighbour not in visited:
                 visited.append(neighbour)
                 queue.append(neighbour)

     return visited   # print all the visited cities from start until the goal


 # this function is dijkstra function that will be used for uniform cost algorithm , this function will find the
 # shortest distance between two cities by comparing each city with its neighbours and the short will take it
 def dijkstra(graph, src,dest):

     queue = [src]        # intilize queue array and put in it the start city
     minDistances = {v: float("inf") for v in graph}     # variable will be used to find the minimum distance
     minDistances[src] = 0
     Previous = {}
     print("The visited cities from ", str(src), " to the goal ", str(dest), " are: ")

     # while loop to keep saving all visited citites until we arrived to our goal
     while queue:
         queue.sort(key=lambda x: minDistances[x])
         currentNode = queue.pop(0)     # first element in the queue
         print("Visit ",currentNode,end="=> ")
         if currentNode==dest:       # since we arrived to our goal then break and stop searching
             break
         for neighbor in graph[currentNode]:
             # get potential newDist from start to neighbor
             newDist = minDistances[currentNode] + int(graph[currentNode][neighbor])

             # if sttement to see if the newDist is shorter to reach neighbor updated it to be the new menimum distance
             if newDist < minDistances[neighbor]:
                 minDistances[neighbor] = min(newDist, minDistances[neighbor])    # update the new minimum distance since we found one shorter
                 queue.append(neighbor)                                           ## Add the new distance and save it in the array.
                 Previous[neighbor] = currentNode
     return minDistances, Previous

#uniform cost search algorithm that is si,ilar as dijkstra with a different that we must visit all possible cities until we
 # find city less than current city
 def UCS(graph, src, dest):

     minDistances, Previous_cities = dijkstra(graph, src,dest)

     path = []      #define array
     currentNode = dest     # the intialize value for current node is the destination city that user will enter in the main

     # while loop to keep checking all the cities from source to destination and it will stop from begining if source is same as dest
     while currentNode != src:
         if currentNode not in Previous_cities:        # after checking all possible cities and we didn't find the dest so the dest not found
             print("Path not exist")
             break
         else:
             path.insert(0, currentNode)         # keep inserting in the array path each new node we visit
             currentNode = Previous_cities[currentNode]  # update the value of current node
     path.insert(0, src)

     if dest in minDistances and minDistances[dest] != float("inf"):
         print("\n=============================================================================")
         print("The real path from ", str(src), " to the goal ", str(dest), " are: ", path), \
         print("\n============================================================================="),\
         print('\nShortest distance between ',str(src),' to the goal ',str(dest),' is '+ str(minDistances[dest]))

#function to read the heuristic input values for walking for all cities
 def walk_heuristic():
     vertex_list = []           #array of 20 element that contain the names of the cities
     adj_list = []          # array is made of 20 element every element in it is an array to know for each city which cities is directly connected with it
     sub_adj_list = []      # we will use it to make dictinary for heuristic values

     with open("data.txt", "r") as input_file:        # choose the input file and intialize it to be read file
         for line in input_file:     # for loop to read all input file data
             line = line.split("##")    # we will split the informations using ## so when there ## mean new value or city
             del line[-1]      #delete line
             if len(line) == 1 or len(line) == 0: # check the length of the line after split
                 break
             else:
                 if line[0] not in vertex_list:   # to be sure the line in the array or not
                     if sub_adj_list:
                         adj_list.append(sub_adj_list)
                     sub_adj_list = []
                     vertex_list.append(line[0])
                     sub_adj_list.append([line[1], int(line[3])])
                 else:
                     sub_adj_list.append([line[1], int(line[3])])
         adj_list.append(sub_adj_list)
     map = {}
     for i in range(len(vertex_list)):
         sub_map = {}
         for j in range(len(adj_list[i])):
             sub_map[adj_list[i][j][0]] = adj_list[i][j][1]
         map[vertex_list[i]] = sub_map
     return map


 def Greedy(graph, src, dest, walk_heuristic):

     path = [src]    #intialize value for the path that is th start city
     currentNode = src
     while currentNode != dest:   #while we still not arrived to the goal
         nodes = sorted(list(graph[currentNode].items()), key=lambda x: walk_heuristic[x[0]][dest])
         currentNode = nodes[0][0]
         if currentNode in path:
             break
         path.append(currentNode) #save the current node in the array

    #print the full information for greedy algorithm between start city and goal city
     print("The visited cities from ",str(src)," to the goal ",str(dest)," are: ",path)
     print("\n=============================================================================")
     return print("The real path from ",str(src)," to the goal ",str(dest)," are: ",path),\
            print("\n============================================================================="),\
            print("\nthere is no cost since it is heuristic values")


 # function to read the heuristic input values for aerial_heuristic for all cities

 def aerial_heuristic():
     vertex_list = []       #array of 20 element that contain the names of the cities
     adj_list = []          # array is made of 20 element every element in it is an array to know for each city which cities is directly connected with it
     sub_adj_list = []       # we will use it to make dictinary for heuristic values

     with open("data.txt", "r") as input_file:       # choose the input file and intialize it to be read file
         for line in input_file:    # for loop to read all input file data
             line = line.split("##")    # we will split the informations using ## so when there ## mean new value or city
             del line[-1]
             if len(line) == 1 or len(line) == 0:       # check the length of the line after split
                 break
             else:
                 if line[0] not in vertex_list:   # to be sure the line in the array or not
                     if sub_adj_list:
                         adj_list.append(sub_adj_list)
                     sub_adj_list = []
                     vertex_list.append(line[0])
                     sub_adj_list.append([line[1], int(line[2])])
                 else:
                     sub_adj_list.append([line[1], int(line[2])])
         adj_list.append(sub_adj_list)
     map = {}
     for i in range(len(vertex_list)):
         sub_map = {}
         for j in range(len(adj_list[i])):
             sub_map[adj_list[i][j][0]] = adj_list[i][j][1]
         map[vertex_list[i]] = sub_map
     return map   #return the path between start city and goal city

 def A_star_graph1():
     vertex_list = []       #array of 20 element that contain the names of the cities
     adj_list = []          # array is made of 20 element every element in it is an array to know for each city which cities is directly connected with it
     sub_adj_list = []   # we will use it to make dictinary
     with open("data.txt", "r") as input_file:      # choose the input file and intialize it to be read file
         for line in input_file:
             line = line.split("##")            # we will split the informations using ## so when there ## mean new value or city
             del line[-1]
             if len(line) == 1 or len(line) == 0:           # to be sure the line in the array or not
                 break
             else:
                 if line[0] not in vertex_list:
                     if sub_adj_list:
                         adj_list.append(sub_adj_list)
                     sub_adj_list = []
                     vertex_list.append(line[0])
                     sub_adj_list.append([line[1], int(line[3])])
                 else:
                     sub_adj_list.append([line[1], int(line[3])])
         adj_list.append(sub_adj_list)
     map = {}
     for i in range(len(vertex_list)):
         sub_map = {}
         for j in range(len(adj_list[i])):
             sub_map[adj_list[i][j][0]] = adj_list[i][j][1]
         map[vertex_list[i]] = sub_map
     return map


 def A_graph():
     vertex_list = []       #array of 20 element that contain the names of the cities
     adj_list = []          # array is made of 20 element every element in it is an array to know for each city which cities is directly connected with it
     sub_adj_list = []
     with open("A.txt", "r") as input_file:
         for line in input_file:
             line = line.split("##")
             del line[-1]
             if len(line) == 1 or len(line) == 0:
                 break
             else:
                 if line[0] not in vertex_list:
                     if sub_adj_list:
                         adj_list.append(sub_adj_list)
                     sub_adj_list = []
                     vertex_list.append(line[0])
                     sub_adj_list.append([line[1], line[2]])
                 else:
                     sub_adj_list.append([line[1], line[2]])
         adj_list.append(sub_adj_list)
     map = {}
     for i in range(len(vertex_list)):
         sub_map = {}
         for j in range(len(adj_list[i])):
             sub_map[adj_list[i][j][0]] = adj_list[i][j][1]
         map[vertex_list[i]] = sub_map
     return map


 # this function is dijkstra function that will be used for uniform cost algorithm , this function will find the
 # shortest distance between two cities by comparing each city with its neighbours and the short will take it

 def dijkstra_A_star(graph, src, dest, heurestic):
     #  adding a node to queue is if its distance has changed at the current step.
     queue = [src] # intilize queue array and put in it the start city
     minDistances = {v: float("inf") for v in graph}     # variable will be used to find the minimum distance
     minDistances[src] = 0
     Previous = {}
     print("The visited cities from ", str(src), " to the goal ", str(dest), " are: ")
     while queue:
         queue.sort(key=lambda x: minDistances[x] + heurestic[x][dest])
         currentNode = queue.pop(0)     # first element in the queue
         print("Visit ",currentNode, end="=> ")
         if currentNode==dest:      # since we arrived to our goal then break and stop searching
             break
         for neighbor in graph[currentNode]:
             # get potential newDist from start to neighbor
             newDist = minDistances[currentNode] + int(graph[currentNode][neighbor])

             # if sttement to see if the newDist is shorter to reach neighbor updated it to be the new menimum distance
             if newDist < minDistances[neighbor]:
                 minDistances[neighbor] = min(newDist, minDistances[neighbor])      # update the new minimum distance since we found one shorter
                 queue.append(neighbor)         ## Add the new distance and save it in the array.
                 Previous[neighbor] = currentNode
     return minDistances, Previous    #return the minimum distance between two cities


 def A_star(graph, src, dest, heurestic):
     minDistances, Previous = dijkstra_A_star(graph, src, dest, heurestic) # dijkstra_A_star that we made in previous functions
     path = []
     currentNode = dest
     while currentNode != src:     #while we still not arrived to the goal
         if currentNode not in Previous:
             print("Path not exist")
             break
         else:
             path.insert(0, currentNode)
             currentNode = Previous[currentNode]
     path.insert(0, src)

     # print the full information for greedy algorithm between start city and goal city
     if dest in minDistances and minDistances[dest] != float("inf"):
         print("\n=============================================================================")
         print("The real path from ", str(src), " to the goal ", str(dest), " are: ", path), \
         print("\n============================================================================="),\
         print('\nShortest distance between ', str(src), ' to the goal ', str(dest), ' is ' + str(minDistances[dest]))


 if __name__ == "__main__":

  #intialize array that contain all 20 cities that used in our program
  arr_test = ["Aka","Bethlehem","Dura","Haifa","Halhoul","Hebron","Jenin","Jericho",
                "Jerusalem","Nablus","Nazareth","Qalqilya","Ramallah","Ramleh","Sabastia",
                "Safad","Salfit","Tubas","Tulkarm","Yafa"]

  map1 = BFS_graph()   #calling BFS_graph function that we make in it the graph for BFS and UCS
  map2 = A_graph()     #calling A_graph function that we make in it the graph for A* algorithm
  map123 = BFS_graph1()   #graph to know the visited cities for BFS algorithm
  aerial = aerial_heuristic() # read the aerial_heuristic values that will be used in A* case 1 with walk real cost
  walk = walk_heuristic()  # read the walk heuristic values that will be used in A* case 2 with car real cost

  #MENU
  print(
        "\n\n\t\t\t\t\t\t\t\tWELCOME\n\n\t\tHello,Please select number of algorithm you want from the following MENU:\n"
        "\t\t1. Show the 20 cities of (Historical Palestine) that are used for the Project\n"
        "\t\t2. Breadth First Search Algorithm(BFS)\n"
        "\t\t3. Uniform Cost Search Algorithm(UCS)\n"
        "\t\t4. Greedy Best Search Algorithm\n"
        "\t\t5. A* Search Algorithm( Aerial (heuristic) and Walk (real cost)\n"
        "\t\t6. A* Search Algorithm( Walk (heuristic) and Car (real cost)\n"
        "\t\t0. EXIT\n\n")
  try:
    menu_input=input("PLZ enter number of algorithm from the previous MENU\n")  # read the entered number from the menu
    menu_input = int(menu_input)

    # if menu number is 1 then the program will print the 20 Palestinian cities
    if menu_input==1:
        print(arr_test)

    #############################################################################################################

    # if menu number is 2 then the program will print start working with BFS algorithm
    elif menu_input == 2:
      try:
          print("WELCOME to Breadth First Search Algorithm(BFS)\n")
          print("\nThe 20 cities and how they must be wrote:\n"+str(arr_test)+"\n")
          start_city: str = input("PLZ enter the start city\n")

          while start_city not in arr_test:   #while loop to keep checking the entered start city is true if yes exit is no keep asking user to enter right input start city

              print("Error, the start city u entered is not one of the cities in the graph Please enter the start city again")
              start_city: str = input("PLZ enter the start city\n")
              continue
          while True:
              number_of_goal_cities = int(input("PLZ enter number of goal cities\n"))
              if number_of_goal_cities < 1 or number_of_goal_cities > 20:
                  print("number of you entered is wrong since number of goals should be between 1 and 20")
              else:
                  print("\nthe number of goals is: " + str(number_of_goal_cities))
                  break

          for a in range(1, number_of_goal_cities + 1):
              print("\nPLZ enter the goal city number",a, "\n")
              goal_city: str = input()
              while goal_city not in arr_test:                #while loop to keep checking the entered goal city is true if yes exit is no keep asking user to enter right input goal city

                  print("Error,the goal city u entered is not one of the cities in the graph Please enter the goal city again")
                  print("\nPLZ enter the goal city number", a, "\n")
                  goal_city: str = input()
                  continue
              city1 = start_city
              city2 = goal_city
              if start_city==goal_city:
                  print("\nYou are already in the Goal city as it is the start city so there is no path or cost")
              else:
               print("The visited cities from ", str(start_city), " to the goal ", str(goal_city), " are: ")
               print(bfs_visited(map123, start_city, goal_city))
               print("\n=============================================================================")
               print("The real and best path From " + str(city1) + " to " + str(city2) + " is: ")
               print(Bredth_First_Search(start_city, goal_city, map1))

      except:
          print("<<<<Error>>>>Your input is wrong\nBACK TO THE MAIN MENU\nEnter a number only and it is integer greater than 0")
          print("=============================================================================")

    #############################################################################################################

    # if menu number is 3 then the program will print start working with UCS algorithm
    elif menu_input == 3:
        try:
            print("WELCOME to Uniform Cost Search Algorithm(UCS)\n")
            print("\nThe 20 cities and how they must be wrote:\n" + str(arr_test) + "\n")
            start_city: str = input("PLZ enter the start city\n")
            # while loop to keep checking the entered start city is true if yes exit is no keep asking user to enter right input start city

            while start_city not in arr_test:
                print("Error, the start city u entered is not one of the cities in the graph Please enter the start city again")
                start_city: str = input("PLZ enter the start city\n")
                continue
            while True:
                number_of_goal_cities = int(input("PLZ enter number of goal cities\n"))
                if number_of_goal_cities < 1 or number_of_goal_cities > 20:
                    print("number of you entered is wrong since number of goals should be between 1 and 20")
                else:
                    print("\nthe number of goals is: " + str(number_of_goal_cities))
                    break

            for a in range(1, number_of_goal_cities + 1):
                print("\nPLZ enter the goal city number", a, "\n")
                goal_city: str = input()
                # while loop to keep checking the entered goal city is true if yes exit is no keep asking user to enter right input goal city
                while goal_city not in arr_test:
                    print("Error,the goal city u entered is not one of the cities in the graph Please enter the goal city again")
                    print("\nPLZ enter the goal city number", a, "\n")
                    goal_city: str = input()
                    continue
                city1 = start_city
                city2 = goal_city
                if start_city == goal_city:
                    print("\nYou are already in the Goal city as it is the start city so there is no path or cost")
                else:
                 UCS(map1, start_city, goal_city)

        except:
            print("<<<<Error>>>>Your input is wrong\nBACK TO THE MAIN MENU\nEnter a number only and it is integer greater than 0")
            print("=============================================================================")

    #############################################################################################################

    # if menu number is 4 then the program will print start working with Greedy Best Search algorithm

    elif menu_input == 4:
        try:
            print("WELCOME to Greedy Best Search Algorithm\n")
            print("\nThe 20 cities and how they must be wrote:\n" + str(arr_test) + "\n")
            start_city: str = input("PLZ enter the start city\n")
            # while loop to keep checking the entered start city is true if yes exit is no keep asking user to enter right input start city

            while start_city not in arr_test:
                print("Error, the start city u entered is not one of the cities in the graph Please enter the start city again")
                start_city: str = input("PLZ enter the start city\n")
                continue
            while True:
                number_of_goal_cities = int(input("PLZ enter number of goal cities\n"))
                if number_of_goal_cities < 1 or number_of_goal_cities > 20:
                    print("number of you entered is wrong since number of goals should be between 1 and 20")
                else:
                    print("\nthe number of goals is: " + str(number_of_goal_cities))
                    break

            for a in range(1, number_of_goal_cities + 1):
                print("\nPLZ enter the goal city number", a, "\n")
                goal_city: str = input()
                # while loop to keep checking the entered goal city is true if yes exit is no keep asking user to enter right input goal city
                while goal_city not in arr_test:
                    print("Error,the goal city u entered is not one of the cities in the graph Please enter the goal city again")
                    print("\nPLZ enter the goal city number", a, "\n")
                    goal_city: str = input()
                    continue
                city1 = start_city
                city2 = goal_city
                if start_city == goal_city:
                    print("\nYou are already in the Goal city as it is the start city so there is no path or cost")
                else:
                 Greedy(map1, start_city, goal_city, walk)

        except:
            print("<<<<Error>>>>Your input is wrong\nBACK TO THE MAIN MENU\nEnter a number only and it is integer greater than 0")
            print("=============================================================================")

    #############################################################################################################

    # if menu number is 5 then the program will print start working with A* Search Algorithm( Aerial (heuristic)
    # and Walk (real cost) algorithm

    elif menu_input == 5:
      try:
          print("WELCOME to A* Search Algorithm( Aerial (heuristic) and Walk (real cost)\n")
          print("\nThe 20 cities and how they must be wrote:\n"+str(arr_test)+"\n")
          start_city: str = input("PLZ enter the start city\n")
          while start_city not in arr_test:
              print("Error, the start city u entered is not one of the cities in the graph Please enter the start city again")
              start_city: str = input("PLZ enter the start city\n")
              continue
          while True:
              number_of_goal_cities = int(input("PLZ enter number of goal cities\n"))
              if number_of_goal_cities < 1 or number_of_goal_cities > 20:
                  print("number of you entered is wrong since number of goals should be between 1 and 20")
              else:
                  print("\nthe number of goals is: " + str(number_of_goal_cities))
                  break

          for a in range(1, number_of_goal_cities + 1):
              print("\nPLZ enter the goal city number", a, "\n")
              goal_city: str = input()
              while goal_city not in arr_test:
                  print("Error,the goal city u entered is not one of the cities in the graph Please enter the goal city again")
                  print("\nPLZ enter the goal city number", a, "\n")
                  goal_city: str = input()
                  continue
              city1 = start_city
              city2 = goal_city
              if start_city==goal_city:
                  print("\nYou are already in the Goal city as it is the start city so there is no path or cost")
              else:
               A_star(map2, start_city, goal_city, aerial)

      except:
          print("<<<<Error>>>>Your input is wrong\nBACK TO THE MAIN MENU\nEnter a number only and it is integer greater than 0")
          print("=============================================================================")

#############################################################################################################

    # if menu number is 6 then the program will print start working with A* Search Algorithm( Walk (heuristic) and car (real cost) algorithm

    elif menu_input == 6:
      try:
          print("WELCOME to A* Search Algorithm( Walk (heuristic) and Car (real cost)\n")
          print("\nThe 20 cities and how they must be wrote:\n"+str(arr_test)+"\n")
          start_city: str = input("PLZ enter the start city\n")
          while start_city not in arr_test:
              print("Error, the start city u entered is not one of the cities in the graph Please enter the start city again")
              start_city: str = input("PLZ enter the start city\n")
              continue
          while True:
              number_of_goal_cities = int(input("PLZ enter number of goal cities\n"))
              if number_of_goal_cities < 1 or number_of_goal_cities > 20:
                  print("number of you entered is wrong since number of goals should be between 1 and 20")
              else:
                  print("\nthe number of goals is: " + str(number_of_goal_cities))
                  break

          for a in range(1, number_of_goal_cities + 1):
              print("\nPLZ enter the goal city number", a, "\n")
              goal_city: str = input()
              while goal_city not in arr_test:
                  print("Error,the goal city u entered is not one of the cities in the graph Please enter the goal city again")
                  print("\nPLZ enter the goal city number", a, "\n")
                  goal_city: str = input()
                  continue
              city1 = start_city
              city2 = goal_city
              if start_city==goal_city:
                  print("\nYou are already in the Goal city as it is the start city so there is no path or cost")
              else:
               A_star(map1, start_city, goal_city, walk)

      except:
          print("<<<<Error>>>>Your input is wrong\nBACK TO THE MAIN MENU\nEnter a number only and it is integer greater than 0")
          print("=============================================================================")


    #############################################################################################################

    # if the user entered 0 then the program will stop and quit

    elif menu_input==0:
     print("THANK YOU FOR USING OUR PROGRAM")
     quit()

    else:
        print("\nError the number you entered is not in the previous Menu numbers\nBACK TO THE MAIN MENU")

   # exception if the user entered wrong input as string instead of integer then he will back to the menu again
  except:
   print("Error the number u entered is not in MENU\nPLZ enter number of algorithm from the previous MENU and only numbers\n")
   print("=============================================================================")

