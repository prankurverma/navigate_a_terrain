import numpy as np
import cv2

## The readImage function takes a file path as argument and returns image in binary form.

def readImage(filePath):

    img = cv2.imread(filePath)                                      ## Read image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                    ## Convert image to grayscale image
    ret, binaryImage = cv2.threshold(gray, 127, 255, 0)             ## Convert image to Binary image

    return binaryImage

## The findNeighbours function takes a maze image and row and column coordinates of a cell as input arguments
## and returns a stack consisting of all the neighbours of the cell as output.
## Note :- Neighbour refers to all the adjacent cells one can traverse to from that cell provided only horizontal
## and vertical traversal is allowed.

def findNeighbours(img,row,column):
    neighbours = []

    if img[20*row+10, 20*column+1]>=51:                             ## Check the left edge pixel value
        neighbours.append((row, column-1))                          ## If true decrease column value and return left cell coordinate
    if img[20*row+1, 20*column+10]>=51:                             ## Check the upper edge pixel value
        neighbours.append((row-1, column))                          ## If true decrease row value and return upper cell coordinate
    if img[20*row+19, 20*column+10]>=51:                            ## Check the lower edge pixel value
        neighbours.append((row+1, column))                          ## If true increase row value and return lower cell coordinate
    if img[20*row+10, 20*column+19]>=51:                            ## Check the right edge pixel value
        neighbours.append((row, column+1))                          ## If true increase column value and return right cell coordinate

    return neighbours

##  colourCell function takes 4 arguments:-
##            img - input image
##            row - row coordinates of cell to be coloured
##            column - column coordinates of cell to be coloured
##            colourVal - the intensity of the colour.
##  colourCell basically highlights the given cell by painting it with the given colourVal. Care should be taken that
##  the function doesn't paint over the black walls and only paints the empty spaces. This function returns the image
##  with the painted cell.

def colourCell(img,row,column,colourVal):

    for i in range(20*row,20*row+20):                               ## Specify row range of a cell to be highlighted
        for j in range(20*column,20*column+20):                     ## Specify column range of a cell to be highlighted
            if img[i,j]==255:                                       ## Only empty white spaces with value=255 are highlighted with colourVal
                img[i,j]=colourVal

    return img

##  Function that accepts some arguments from user and returns the graph of the maze image.
def buildGraph(img, final_point):  ## You can pass your own arguments in this space.
    graph = {}

    for i in range(0,final_point[0]+1):                             ## Range of i(abscissa) from 0 to abscissa of final point
        for j in range(0,final_point[1]+1):                         ## Range of j(ordinate) from 0 to ordinate of final point
            neighbours = findNeighbours(img, i, j)                  ## Call function findNeignbours to find neighbours
            graph[(i, j)] = neighbours                              ## Returns coordinates of neighbours to graph string

    return graph

##  Finds shortest path between two coordinates in the maze. Returns a set of coordinates from initial point
##  to final point.
def findPath(graph, start, end, path=[]): ## You can pass your own arguments in this space.

    path = path + [start]
    if start == end:                                                ## Dijkstra's algorithm to find shortest between nodes in the graph
        return path                                                 
    if not graph.has_key(start):                                     
        return path                                                 
    shortest = None                                                 
    for node in graph[start]:                                        
        if node not in path:                                         
            newpath = findPath(graph, node, end, path)               
            if newpath:                                              
                if not shortest or len(newpath) < len(shortest):     
                    shortest = newpath                              


    return shortest

## This is the main function where all other functions are called. It accepts filepath
## of an image as input.

def main(filePath, flag = 0):                 
    img = readImage(filePath)      ## Read image with specified filepath.
    breadth = len(img)/20          ## Breadthwise number of cells
    length = len(img[0])/20        ## Lengthwise number of cells
    if length == 10:
        initial_point = (0,0)      ## Start coordinates for maze solution
        final_point = (9,9)        ## End coordinates for maze solution    
    else:
        initial_point = (0,0)
        final_point = (19,19)
    graph = buildGraph(img, final_point)       ## Build graph from maze image. Pass arguments as required.
    shortestPath = findPath(graph, initial_point, final_point)  ## Find shortest path. Pass arguments as required.
    print shortestPath             ## Print shortest path to verify
    string = str(shortestPath) + "\n"
    for i in shortestPath:         ## Loop to paint the solution path.
        img = colourCell(img, i[0], i[1], 200)
    if __name__ == '__main__':     ## Return value for main() function.
        return img
    else:
        if flag == 0:
            return string
        else:
            return graph

## The main() function is called here. Specify the filepath of image in the space given.
          
if __name__ == '__main__':
    filePath = 'maze09.jpg'        ## File path for test image
    img = main(filePath)           ## Main function call
    cv2.imshow('canvas', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




