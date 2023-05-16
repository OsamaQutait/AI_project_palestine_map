import sys

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow
from design import *


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.arr_test = ["Aka", "Bethlehem", "Dura", "Haifa", "Halhoul", "Hebron", "Jenin", "Jericho",
            "Jerusalem", "Nablus", "Nazareth", "Qalqilya", "Ramallah", "Ramleh", "Sabastia",
            "Safad", "Salfit", "Tubas", "Tulkarm", "Yafa"]

        self.ui.city1.addItems(self.arr_test)
        self.ui.city2.addItems(self.arr_test)
        self.ui.algorithm.addItems(["Breadth First Search", "Uniform Cost Search", "Greedy",
                                    "A* (Aerial (heuristic) and Walk (real cost))",
                                    "A* (Walk (heuristic) and Car (real cost))"])

        self.map1 = self.BFS_graph()
        self.map2 = self.A_graph()
        self.map123 = self.BFS_graph1()
        self.walk = self.walk_heuristic()
        self.aerial = self.aerial_heuristic()

        self.ui.btn_run.clicked.connect(self.run)
        self.ui.btn_close.clicked.connect(exit)

        self.show()

    def run(self):
        start_city = self.ui.city1.currentText()
        goal_city = self.ui.city2.currentText()
        algorithm = self.ui.algorithm.currentText()
        path_lst = []
        if algorithm == "BFS":
            self.ui.distance.setText("0")

            visited_lst = self.bfs_visited(self.map123, start_city, goal_city)
            visited_str = ''
            for item in visited_lst:
                visited_str += item + '\n'
            self.ui.visited.setText(visited_str)

            path_lst = self.Bredth_First_Search(start_city, goal_city, self.map1)

        elif algorithm == "UCS":
            self.UCS(self.map1, start_city, goal_city)
            path_lst = self.Bredth_First_Search(start_city, goal_city, self.map1)


        elif algorithm == "Greedy":
            self.ui.visited.setText("")
            self.ui.distance.setText("no cost, heuristic values")
            path_lst = self.Greedy(self.map1, start_city, goal_city, self.walk)
            visited_str = ''
            for item in path_lst:
                visited_str += item + '\n'
            self.ui.visited.setText(visited_str)
        elif algorithm == "A* (Aerial (heuristic) and Walk (real cost))":
            path_lst = self.A_star(self.map2, start_city, goal_city, self.aerial)

        else:
            path_lst = self.A_star(self.map1, start_city, goal_city, self.walk)

        path_str = ''
        for item in path_lst:
            path_str += item + '\n'
        self.ui.path.setText(path_str)

    def BFS_graph(self):
        vertex_list = []
        adj_list = []
        sub_adj_list = []
        with open("BFS.txt", "r") as input_file:
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

    def Bredth_First_Search(self, Start_city, Goal_city, Algorithm_graph):
        # Intialize a queue to save the cities in it (we used queue since BFS use FIF0)
        BFS_queue = []
        # push the first path into the queue
        BFS_queue.append([Start_city])
        while BFS_queue:
            # get the first path from the queue
            path = BFS_queue.pop(0)
            # get the last node from the path
            node = path[-1]

            # path found
            if node == Goal_city:
                return path
            # enumerate all adjacent nodes, construct a
            # new path and push it into the queue
            for adjacent in Algorithm_graph.get(node, []):
                new_path = list(path)
                new_path.append(adjacent)
                BFS_queue.append(new_path)

    def BFS_graph1(self):
        vertex_list = []
        adj_list = []
        sub_adj_list = []
        with open("BFS.txt", "r") as input_file:
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
                        sub_adj_list.append(line[1])
                    else:
                        sub_adj_list.append(line[1])
            adj_list.append(sub_adj_list)
        map = {}
        for i in range(len(vertex_list)):
            map[vertex_list[i]] = adj_list[i]
        return map

    def bfs_visited(self, graph, node, goal):  # function for BFS
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

        return visited

    def dijkstra(self, graph, src, dest):
        # The only criterium of adding a node to queue is if its distance has changed at the current step.
        queue = [src]
        minDistances = {v: float("inf") for v in graph}
        minDistances[src] = 0
        predecessor = {}
        visited_str = ''
        while queue:
            queue.sort(key=lambda x: minDistances[x])
            currentNode = queue.pop(0)
            visited_str += currentNode + '\n'
            if currentNode == dest:
                break
            for neighbor in graph[currentNode]:
                # get potential newDist from start to neighbor
                newDist = minDistances[currentNode] + int(graph[currentNode][neighbor])

                # if the newDist is shorter to reach neighbor updated to newDist
                if newDist < minDistances[neighbor]:
                    minDistances[neighbor] = min(newDist, minDistances[neighbor])
                    queue.append(neighbor)
                    predecessor[neighbor] = currentNode
        self.ui.visited.setText(visited_str)
        return minDistances, predecessor

    def UCS(self, graph, src, dest):
        minDistances, predecessor = self.dijkstra(graph, src, dest)

        path = []
        currentNode = dest
        while currentNode != src:
            if currentNode not in predecessor:
                print("Path not exist")
                break
            else:
                path.insert(0, currentNode)
                currentNode = predecessor[currentNode]
        path.insert(0, src)

        if dest in minDistances and minDistances[dest] != float("inf"):
            self.ui.distance.setText(str(minDistances[dest]))
            path_str = ''
            for item in path:
                path_str += item + '\n'
            self.ui.path.setText(path_str)

    def Greedy(self, graph, src, dest, walk_heuristic):
        path = [src]
        currentNode = src
        while currentNode != dest:
            nodes = sorted(list(graph[currentNode].items()), key=lambda x: walk_heuristic[x[0]][dest])
            currentNode = nodes[0][0]
            if currentNode in path:
                break
            path.append(currentNode)
        return path

    def walk_heuristic(self):
        vertex_list = []
        adj_list = []
        sub_adj_list = []
        with open("data.txt", "r") as input_file:
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

    def aerial_heuristic(self):
        vertex_list = []
        adj_list = []
        sub_adj_list = []
        with open("data.txt", "r") as input_file:
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
        return map

    def A_star_graph1(self):
        vertex_list = []
        adj_list = []
        sub_adj_list = []
        with open("data.txt", "r") as input_file:
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

    def A_graph(self):
        vertex_list = []
        adj_list = []
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

    def dijkstra_A_star(self, graph, src, dest, heurestic):
        # The only criterium of adding a node to queue is if its distance has changed at the current step.
        queue = [src]
        minDistances = {v: float("inf") for v in graph}
        minDistances[src] = 0
        predecessor = {}
        visited_str = ''
        while queue:
            queue.sort(key=lambda x: minDistances[x] + heurestic[x][dest])
            currentNode = queue.pop(0)
            visited_str += currentNode + '\n'
            if currentNode == dest:
                break
            for neighbor in graph[currentNode]:
                # get potential newDist from start to neighbor
                newDist = minDistances[currentNode] + int(graph[currentNode][neighbor])

                # if the newDist is shorter to reach neighbor updated to newDist
                if newDist < minDistances[neighbor]:
                    minDistances[neighbor] = min(newDist, minDistances[neighbor])
                    queue.append(neighbor)
                    predecessor[neighbor] = currentNode
        self.ui.visited.setText(visited_str)
        return minDistances, predecessor

    def A_star(self, graph, src, dest, heurestic):
        minDistances, predecessor = self.dijkstra_A_star(graph, src, dest, heurestic)
        path = []
        currentNode = dest
        while currentNode != src:
            if currentNode not in predecessor:
                print("Path not exist")
                break
            else:
                path.insert(0, currentNode)
                currentNode = predecessor[currentNode]
        path.insert(0, src)

        if dest in minDistances and minDistances[dest] != float("inf"):
            self.ui.distance.setText(str(minDistances[dest]))
            return path

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())