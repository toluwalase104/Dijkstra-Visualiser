import pygame

'''
Divide visualisation speed into
four smaller buttons each determining
the speed of each visualisation.
'''
pygame.init()

black = (0,0,0)
white = (255,255,255)
red = (255, 0,0)
fireBrickRed = (238,44,44)
emerald = (0,255, 0)
pink = (238, 18, 137)
grey = (79,79,79)
darkGrey = (43, 43, 43)
lightGrey = (107,107,107)
lightestGrey = (201,201,201)
cyan, cyan2 = (152,245,255), (0,255,255)
cyan3, cyan4 = (0,205,205),(0,139,139)
lightAzure = (30,144,255)
deepAzure = (24,116,205)
royalBlue = (39, 64, 139)
gold = (218,165,32)

infinity = float("inf")
delay = 50

class Node:
    '''
    This class is used to maintain the state of individual nodes in the graph
    as well as create a doubly-linked matrix data structure (of my own creation)
    within which all adjacent nodes are stored.
    '''
    def __init__(self, status, coordinate):
        stateAttributes = {
            "start": [fireBrickRed, 1],
            "end": [emerald, 1],
            "barrier": [lightGrey, None],
            "visited": [cyan, None],
            "path": [gold, 1],
            "accessible": [white, 1]}
                    
        self.status = status    # This corresponds to the type of node e.g start, visited etc.
        self.coordinate = coordinate # This corresponds to the nodes position in the array-backed grid
        
        self.colour = stateAttributes[self.status][0] 
        self.iweight = stateAttributes[self.status][1] # This is the initial weight of each node (hence the name 'iweight')
        '''
        The four position variables below are used to keep track
        of all the adjacent nodes of each node
        '''
        self.right = None
        self.left = None
        self.up = None
        self.down = None
   
class Button:
    '''
    This class is used to create button objects
    that can show the interaction of the user e.g.
    changing colour when hovered over or carrying out
    actions when clicked.
    '''
    def __init__(self, colour, x, y, width, height, text = ""):
        # This constructor initialises the features of the button including the message within it
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline = None): 
        # This method is used to draw the button at the initialised location variables     
        if outline:
            pygame.draw.rect(win, outline, (self.x - 5, self.y - 5,\
                            self.width + 10, self.height + 10), 0)
            
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height), 0)

        if self.text != "":
            font = pygame.font.SysFont("arialblack", 25)
            text = font.render(self.text, True, black)
            win.blit(text, (self.x + ((self.width)/2 - (text.get_width())/2),\
                            self.y + ((self.height)/2 - (text.get_height())/2)))

    def hovered(self, mousePosition):
        # This method is used to detect whether a mouse is hovering over a button
        if (mousePosition[0] > self.x and mousePosition[0] < (self.x + self.width))\
        and (mousePosition[1] > self.y and mousePosition[1] < (self.y + self.height)):
            return True
        return False

def drawNode(position):
    m_column = position[0] // (width + margin)
    m_row = position[1] // (height + margin)

    if grid[m_row][m_column] == "B":
        grid[m_row][m_column] = 1
        '''    
    elif (m_row == startRow and m_column == startColumn):
        grid[startRow][startColumn] = 2

    elif (m_row == endRow and m_column == endColumn):
        grid[endRow][endColumn] = 2
        '''

    else:
        grid[m_row][m_column] = "B"

    pygame.draw.circle(win, white, position,\
            radius, 2.5)

# The boolean variables below, and the loops that use them,
#  are used to ensure appropriate values are entered for the start and end points
noStart = True
noEnd = True

while noStart:
    i = int(input("Enter a column, between 1 and 20, to start at: "))
    j = int(input("Enter a row, between 1 and 20 to start at: "))

    if (i >= 1 and i <= 20) and (j >= 1 and j <= 20):
        noStart = False
        i -= 1 # The inputted values are shifted back one, as arrays are zero-based
        j -= 1
    else:
        raise ValueError("Row or column was not in correct bounds")

start = (i, j)

while noEnd:
    i = int(input("Enter a column, between 1 and 20, to end at: "))
    j = int(input("Enter a row, between 1 and 20, to end at: "))

    if (i >= 1 and i <= 20) and (j >= 1 and j <= 20):
        noEnd = False
        i -= 1
        j -= 1
    else:
        raise ValueError("Row or column was not in correct bounds")

end = (i, j)

startColumn = start[0]
startRow = start[1]

endColumn = end[0]
endRow = end[1]

width, height, margin = 20, 20, 5

radius, linkLength = 10, 25

screenSize = (900, 1020)

length, depth = 300, 120

visualiseButton = Button(lightGrey, 0, screenSize[1] - depth, length, depth, "Visualise")

speedButton = Button(lightGrey, length, screenSize[1] - depth, length, depth, "Visualisation Speed")

resetButton = Button(lightGrey, screenSize[0] - length, screenSize[1] - depth, length, depth, "Reset")

win = pygame.display.set_mode(screenSize)

pygame.display.set_caption("Dijkstra Visualiser - Base Speed")

Fast = 1

clock = pygame.time.Clock()

running = True

gridLength = 20

grid = [[1 for i in range(gridLength)] for j in range(gridLength)]

def redrawWindow():
    visualiseButton.draw(win, darkGrey)
    speedButton.draw(win, darkGrey)
    resetButton.draw(win, darkGrey)

    pygame.display.update()

def getKey(val, dictionary):
    '''
    This function is used to return the key of a given value from
    a dictionary. Only used when all keys and values are distinct.
    '''
    for key, value in dictionary.items():
        if value == val:
            return key
          
def drawBarrier(graph =[[]], n = None):
    pygame.event.get()
    directions1 = []
    try:
        if graph[n].status == "barrier":
            pygame.draw.circle(win, white, graph[n].coordinate,\
                (radius))
            directions1 = [graph[n].right, graph[n].left,\
                graph[n].up, graph[n].down]
    except AttributeError:
        print(0)
        return

    for item in directions1:
        try:
            if item.status == "barrier":
                pygame.draw.line(win, white, graph[n].coordinate,\
                    item.coordinate, radius*2)
                pygame.draw.circle(win, white, item.coordinate,\
                (radius))
        except AttributeError:
            continue

def drawVisited(graph =[[]], n = None, colour = None):
    pygame.time.delay(delay)
    pygame.event.get()
    directions1 = []
    try:
        if graph[n].status == "visited" or "path":
            pygame.draw.circle(win, colour, graph[n].coordinate,\
                (radius))
            directions1 = [graph[n].right, graph[n].left,\
                graph[n].up, graph[n].down]
            pygame.display.update()
    except AttributeError:
        print(0)
        return

    for item in directions1:
        try:
            if item.status == "visited":
                pygame.draw.line(win, colour, graph[n].coordinate,\
                    item.coordinate, 3)
                pygame.draw.circle(win, colour, item.coordinate,\
                (radius))
                pygame.display.update()
        except AttributeError:
            continue

def drawPath(graph =[[]], n = None):
    pygame.time.delay(delay)
    directions1 = []
    pygame.event.get()
    try:
        if graph[n].status == "path" or "end":
            pygame.draw.circle(win, gold, graph[n].coordinate,\
                (radius))
            directions1 = [graph[n].right, graph[n].left,\
                graph[n].up, graph[n].down]
            pygame.display.update()
    except AttributeError:
        print(1)
        return
    for item in directions1:
        try:
            if item.status == "path":
                pygame.draw.line(win, gold, graph[n].coordinate,\
                    item.coordinate, 3)
                pygame.display.update()
        except AttributeError:
            continue

def initiateNodeGrid(position = None, matrix = [[]], click = False, void = True):
    def alterNodeClick(position, matrix, nodeDictionary):
        '''
        This variable is used to change the colour of a node at a certain point in the
        array backed grid
        '''
        global startRow, startColumn
        global endRow, endColumn
        global radius, linkLength

        m_column = position[0] // (2*radius + linkLength)
        m_row = position[1] // (2*radius + linkLength)
    
        if grid[m_row][m_column] == 3:
            grid[m_row][m_column] = 1
        else:
            grid[m_row][m_column] = 3
        
        x, y = 0, 0 
        count = 1

        for row in matrix:
            for node in matrix:
                centre = (x + radius, y + radius)
                if node == 1:
                    nodeDictionary[count] = Node("accessible", centre)

                elif node == 3:
                    nodeDictionary[count] = Node("barrier", centre)
                

                x += 2*radius + linkLength
                count += 1

            x = 0
            y += 2*radius + linkLength
    #------------------------------------------------------------------------------------
     
    global startRow, startColumn
    global endRow, endColumn

    x, y = 0, 0 
    count = 1
    nodeDictionary = dict()

    for row in matrix:
        for node in row:
            pygame.draw.circle(win, white, (x + radius, y + radius),\
            radius, 1)

            if node == 1:
                state = "accessible"
                       
            elif node == 3:
                state = "barrier"
                pygame.draw.circle(win, white, (x + radius, y + radius),\
                (radius))

            if (count == (gridLength*startRow + (startColumn + 1))):
                state = "start"
                pygame.draw.circle(win, fireBrickRed, (x + radius, y + radius),\
                (radius -1))
            elif (count == (gridLength*endRow + (endColumn + 1))):
                state = "end"
                pygame.draw.circle(win, emerald, (x + radius, y + radius),\
                (radius - 1))

            if x < 855:
                pygame.draw.line(win, grey, (x + 2*radius, y + radius),\
                (x + 2*radius + linkLength, y + radius), 3)
            if y < 855:
                pygame.draw.line(win, grey, (x + radius, y + 2*radius),\
                (x + radius, y + 2*radius + linkLength), 3)
         
 

            centre = (x + radius, y + radius)
            x += 2*radius + linkLength

            nodeDictionary[count] = Node(state, centre)
            count += 1

        x = 0
        y += 2*radius + linkLength

    if click:
        alterNodeClick(position, matrix, nodeDictionary)
    # The for loop  below sets the values of the adjacent node in a
    # two-dimensional-doubly-linked list fashion
    count = 1
    for count in range(1, len(nodeDictionary) + 1):
        node = nodeDictionary[count]
        try:
            if count % gridLength == 0:
                raise KeyError
            node.right = nodeDictionary[count + 1]
        except KeyError:
            pass
        try:
            if (count - 1) % gridLength == 0:
                raise KeyError
            node.left = nodeDictionary[count - 1]
        except KeyError:
            pass
        try:
            node.up = nodeDictionary[count - gridLength]
        except KeyError:
            pass
        try:
            node.down = nodeDictionary[count + gridLength] 
        except KeyError:
            pass


    graph = dict()
    for count in range(1, len(nodeDictionary) + 1):
        node = nodeDictionary[count]
        if node.status == "barrier":
            continue
        directions = []

        try:
            leftWeight = (node.left).iweight
            left = count - 1

            if left % gridLength == 0:
                left -= 1

            row = (left // gridLength)
            left += 1
            column = (left - 1) - (row*gridLength)

            leftWeight = matrix[row][column]
            if leftWeight == "B": 
                raise AttributeError

            left = getKey(node.left, nodeDictionary)
            L = (left, leftWeight)
        except AttributeError:
            L = False
        
        try:
            rightWeight = (node.right).iweight
            right = count + 1

            if right % gridLength == 0:
                right -= 1
                
            row = (right // gridLength)
            right += 1

            column = (right - 1) - (row*gridLength)

            rightWeight = grid[row][column]
            if rightWeight == "B":
                raise AttributeError

            right = getKey(node.right, nodeDictionary)
            R = (right, rightWeight)
        except AttributeError:
            R = False
        
        try:
            upWeight = (node.up).iweight
            up = count - gridLength

            if up % gridLength == 0:
                up -= 1

            row = (up // gridLength)
            up += 1
            column = (up - 1) - (row*gridLength)

            upWeight = grid[row][column]
            if upWeight == "B":
                raise AttributeError
            
            upWeight = gridLength
            up = getKey(node.up, nodeDictionary)
            U = (up, upWeight)
        except AttributeError:
            U = False

        try:
            downWeight = (node.down).iweight
            down = count + gridLength

            if down % gridLength == 0:
                down -= 1

            row = (down // gridLength)
            down += 1
            column = (down - 1) - (row*gridLength)

            downWeight = grid[row][column]
            if downWeight == "B":
                raise AttributeError
            
            downWeight = gridLength
            down = getKey(node.down, nodeDictionary)
            D = (down, downWeight)
        except AttributeError:
            D = False

        directions = [L, R, U, D]
        
        delList = []
        for item in directions:
            if item == False:
                directions.remove(item)
                delList.append(item)

        for item in directions:
            if item in delList:
                directions.remove(item)

        graph[getKey(node, nodeDictionary)] = dict(directions)

    if not void:
        return (graph, nodeDictionary)

def DijkstrasAlgorithm(grid, sourceNode, endNode, nodeDict):
    # "allnodes" is used to contain all nodes present in the grid inputted into the function.
    # "distanceFromStart" contains the distance from the sourceNode to an inputted node from the grid
    # path contains the shortest path determined by the algorithm
    # "parents" is a dictionary used to form the basis with
    # which the shortest path can be outputted, by interlinking the 
    # the parents of each class from the end to the start, then reversing the list.

    currentNode, allNodes = sourceNode, grid
    distanceFromStart, parents, path, length  = dict(), dict(), [], 0

    # This for loop initialises the distances to allNodes as infinity
    for node in allNodes:
        distanceFromStart[node] = infinity

    distanceFromStart[sourceNode] = 0 # This sets the distance to the start as zero as we are already there
   
   # This while loop ensures that all possible paths are explored, by continuing to iterate until the 
   # dictionary allNodes is empty
    pygame.event.get()
    while allNodes:

        closestNode = None

        # This for loop is used to set the closest node equal to the first node availabe out of all of them
        for node in allNodes:
            if node == None:
                continue

            if closestNode == None:
                closestNode = node

        # As the graph is written in nested dictionary form 
        # The line of code below extracts the subdictionary from the key of the 'closestNode'
        # this creates a list with all the keys and values (in tuple form) of the inputted node
        # These values are stored in the variable to analyse all possible routes that can be taken from the 
        # closest node

        nodesToConsider = allNodes[closestNode].items()
        if  nodeDict[closestNode].status == "accessible":
            nodeDict[closestNode].status = "visited"
           
        # This for loop updates the distance from the start by checking if an alternative distance to the node in question
        # can be determined
        pygame.event.get()
        for node, weight in nodesToConsider:
            try:
                if weight == None:
                    continue            
                if weight + distanceFromStart[closestNode]\
                    < distanceFromStart[node]:

                    distanceFromStart[node] = weight + distanceFromStart[closestNode]

                    # This line is usedto update the parent of each node
                    parents[node] = closestNode
            except KeyError:
                continue

        # This line remove values from the entire dictionary of nodes
        allNodes.pop(closestNode)
    try:
        if sourceNode != 1:   
            distanceFromStart[1] = distanceFromStart[2] + 1
    except:
        pass

    visitationOrder = sorted(distanceFromStart, key = lambda x: distanceFromStart[x])

    pygame.event.get()
    colours, colourCount = [cyan, cyan2, cyan3, cyan4], 0
    for x in visitationOrder:
        if distanceFromStart[x] != infinity:
            colourIndex = colourCount // 100
            drawVisited(nodeDict, x, colours[colourIndex])
            colourCount += 1

    # This variable is used in the while loop underneath it
    # to backtrack the path from the end to the beginning
    reference = endNode
    pygame.event.get()
    while reference != sourceNode:
        path.append(reference)
        # This try/except block  is used to determine whether if an unregistered parent node is called
        try:
            reference = parents[reference] 
            nodeDict[reference].status = "path"

        except KeyError:
            print(path)
            raise TypeError("Start or end unreachable")

    path.append(sourceNode)
    
    # This is used to revereses the list as it was created backwards
    pygame.event.get()
    path = list(reversed(path))
    pygame.time.delay(2000)
    for x in path:
        drawPath(nodeDict, x)

    print("Shortest distance is of weight {} \n".format(distanceFromStart[endNode])\
    + " and the path is {}".format(path))
    return path

while running:

    win.fill(black)
    
    graph = initiateNodeGrid(matrix = grid, void = False)

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if visualiseButton.hovered(pos):
                print("Visualisation commencing!")
                start = 20*startRow + (startColumn + 1)
                destination = 20*endRow + (endColumn + 1)
                x, y, count = 0, 0, 1
                for node in graph[1]:
                    if x < 855:
                        pygame.draw.line(win, black, (x + 2*radius, y + radius),\
                        (x + 2*radius + linkLength, y + radius), 3)
                    if y < 855:
                        pygame.draw.line(win, black, (x + radius, y + 2*radius),\
                        (x + radius, y + 2*radius + linkLength), 3)

                    x += 2*radius + linkLength

                    count +=1
                    if count % 20 == 0:
                        y += 2*radius + linkLength
                        x = 0

                pygame.display.update()
                pygame.time.delay(100)

                for key, val in graph[1].items():
                    if val.status == "barrier":
                        drawBarrier(graph[1], key)
                
                pygame.display.update()
                pygame.time.delay(100)

                DijkstrasAlgorithm(graph[0], start, destination, graph[1])
                pygame.time.delay(3000)

                
            elif resetButton.hovered(pos):
                grid = [[1 for i in range(20)] for j in range(20)]
                grid[startRow][startColumn] = 2
                grid[endRow][endColumn] = 2
            
            elif speedButton.hovered(pos):
                print("Visualisation speed altering")
                if Fast == 0:
                    delay //= 5
                    Fast = 0.5
                    pygame.display.set_caption("Dijkstra Visualiser - Very-High Speed")
                    pygame.display.flip()
                
                elif Fast == 0.5:
                    delay *= 5
                    Fast = 2
                    pygame.display.set_caption("Dijkstra Visualiser - High Speed")
                    pygame.display.flip()

                elif Fast == 1:
                    delay //= 5
                    Fast = 0
                    pygame.display.set_caption("Dijkstra Visualiser - High Speed")
                    pygame.display.flip()
                
                elif Fast == 5:
                    delay *= 5
                    Fast = 4.5
                    pygame.display.set_caption("Dijkstra Visualiser - Very-Low Speed")
                    pygame.display.flip()
                
                elif Fast == 4.5:
                    delay //= 5
                    Fast = 4
                    pygame.display.set_caption("Dijkstra Visualiser - Low Speed")
                    pygame.display.flip()

                elif Fast == 3:
                    delay *= 5
                    Fast = 5
                    pygame.display.set_caption("Dijkstra Visualiser - Low Speed")
                    pygame.display.flip()

                elif Fast == 2:
                    delay *= 5
                    Fast = 3
                    pygame.display.set_caption("Dijkstra Visualiser - Base Speed")
                    pygame.display.flip()

                elif Fast == 4:
                    delay //= 5
                    Fast = 1
                    pygame.display.set_caption("Dijkstra Visualiser - Base Speed")
                    pygame.display.flip()
       
            else:
                initiateNodeGrid(position = pos, matrix = grid,\
                    click = True)

        elif event.type == pygame.MOUSEMOTION:
            if visualiseButton.hovered(pos):
                visualiseButton.colour = lightestGrey
                resetButton.colour = lightGrey
                speedButton.colour = lightGrey
                
            elif resetButton.hovered(pos):
                resetButton.colour = lightestGrey
                visualiseButton.colour = lightGrey
                speedButton.colour = lightGrey

            elif speedButton.hovered(pos):
                speedButton.colour = lightestGrey
                visualiseButton.colour = lightGrey
                resetButton.colour = lightGrey            
                
            else:
                visualiseButton.colour = lightGrey
                speedButton.colour = lightGrey 
                resetButton.colour = lightGrey

    redrawWindow()

    clock.tick(60)

pygame.quit()
