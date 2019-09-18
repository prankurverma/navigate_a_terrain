import numpy as np
import cv2
import math
import time
##  Returns sine of an angle.
def sine(angle):
    return math.sin(math.radians(angle))

##  Returns cosine of an angle
def cosine(angle):
    return math.cos(math.radians(angle))

##  Reads an image from the specified filepath and converts it to Grayscale. Then applies binary thresholding
##  to the image.
def readImage(filePath):
    mazeImg = cv2.imread(filePath)
    grayImg = cv2.cvtColor(mazeImg, cv2.COLOR_BGR2GRAY)
    ret,binaryImage = cv2.threshold(grayImg,127,255,cv2.THRESH_BINARY)
    return binaryImage

##  This function accepts the img, level and cell number of a particular cell and the size of the maze as input
##  arguments and returns the list of cells which are traversable from the specified cell.
def findNeighbours(img, level, cellnum, size):
    neighbours = []

    ## radius of each level
    r = level*40
    ## angular width of each cell
    theta = 360.0/val[level-1]
    ## parameters for middle point on inner arc of current level
    theta1 = theta*cellnum-theta/2
    side1x = (int)(r*cosine(theta1))
    side1y = (int)(r*sine(theta1))
    ## check if pixel is white
    if check(img, side1x, side1y)==1:
    ## if the level is 1, then inner nieghbour is (0,0)
        if level==1:
            neighbours.append((0,0))
        ## if the level is 4 or 5, then for inner nieghbours cellnum remains same
        elif level==4 or level==5:
            neighbours.append((level-1,cellnum))
        else:
            ## if the cellnum of current cell is divisible by 2, then nieghbours cellnum is halfed
            if cellnum%2==0:
                neighbours.append((level-1,cellnum/2))
            ## if the cellnum of current cell is not divisible by 2, then nieghbours cellnum is halfed+1
            else:
                neighbours.append((level-1,(cellnum+1)/2))

    ## paramters for middle point on outer arc of current level   
    if level==3 or level==4 or level==6:
        theta2 = theta*cellnum-theta/2
        side2x = (int)((r+40)*cosine(theta2))
        side2y = (int)((r+40)*sine(theta2))
        if check(img, side2x, side2y)==1:
            neighbours.append((level+1,cellnum))

    ## parameters for middle point on clockwise right wall of current level  
    theta3 = theta*cellnum
    side3x = (int)((r+20)*cosine(theta3))
    side3y = (int)((r+20)*sine(theta3))
    if check(img, side3x, side3y)==1:
        if cellnum==val[level-1]:
            neighbours.append((level,1))
        else:
            neighbours.append((level,cellnum+1))

    ## parameters for middle point on clockwise left wall of current level  
    theta4 = theta*(cellnum-1)
    side4x = (int)((r+20)*cosine(theta4))
    side4y = (int)((r+20)*sine(theta4))
    if check(img, side4x, side4y)==1:
        if cellnum==1:
            neighbours.append((level,val[level-1]))
        else:
            neighbours.append((level,cellnum-1))

    if level!=3 and level!=4 and level!=6:
        ## paramters for right middle point on outer arc of current level   
        theta5 = theta*cellnum-0.75*theta
        side5x = (int)((r+40)*cosine(theta5))
        side5y = (int)((r+40)*sine(theta5))
        if check(img, side5x, side5y)==1:
            neighbours.append((level+1,2*cellnum-1))
        ## paramters for left middle point on outer arc of current level   
        theta6 = theta*cellnum-theta/4
        side6x = (int)((r+40)*cosine(theta6))
        side6y = (int)((r+40)*sine(theta6))
        if check(img, side6x, side6y)==1:
            neighbours.append((level+1,2*cellnum))


    return neighbours

##  colourCell function takes 5 arguments:-
##            img - input image
##            level - level of cell to be coloured
##            cellnum - cell number of cell to be coloured
##            size - size of maze
##            colourVal - the intensity of the colour.
##  colourCell basically highlights the given cell by painting it with the given colourVal. Care should be taken that
##  the function doesn't paint over the black walls and only paints the empty spaces. This function returns the image
##  with the painted cell.
def colourCell(img, level, cellnum, size, colorVal):

    r = level*40
    theta = 360.0/val[level-1]
    for i in range(r, r+40):
        angle_start = theta*(cellnum-1)
        angle_end = theta*cellnum if level!=0 else 360
        while angle_start<=angle_end:
            x = i*cosine(angle_start)+len(img)/2
            y = i*sine(angle_start)+len(img)/2
            if img[y,x]>=150:
                img[y,x]=colorVal
            angle_start+=.5

    return img

##  Function that accepts some arguments from user and returns the graph of the maze image.
def buildGraph(img, size):
    graph = {}

    lgth = 4 if size==1 else 6
    for i in range(1, lgth+1):
        for j in range(1, val[i-1]+1):
            neighbours = findNeighbours(img, i, j, size)
            graph[(i, j)] = neighbours
            if (lgth+1,j) in neighbours:
                graph[(lgth+1,j)]=[(lgth,j)]
    #print graph

    return graph


##  Function accepts some arguments and returns the Start coordinates of the maze.
def findStartPoint(img, size):
    if size==1:
        cellnum=24
        level=4
    else:
        cellnum=48
        level=6
    r = (level+1)*40
    theta = 360.0/val[level-1]
    for i in range(1,cellnum+1):
        theta2 = theta*i-theta/2
        side2x = (int)(r*cosine(theta2))
        side2y = (int)(r*sine(theta2))
        if check(img, side2x, side2y)==1:
            start = (level,i)
            break

    return start

##  Finds shortest path between two coordinates in the maze. Returns a set of coordinates from initial point
##  to final point.
def findPath(graph, start, end, path=[]):

    path = path + [start]
    if start == end:
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

val = [6, 12, 24, 24, 24, 48]
'''
*Function Name: check
*Input:         img  -> image
                x    -> X Co-ordinate of point
                y    -> Y Co-ordinate of point
*Output:        flag -> Variable conatining if point is white or not
*Logic:         Checks for the color value of the point and returns 1 for white and 0 for black
*Sample Call:   check(img, 230, 320)
'''
def check(img, x, y):
        flag = 0
        if img[y+len(img)/2, x+len(img)/2]>=153:
                    flag=1
        return flag
    
##  This is the main function where all other functions are called. It accepts filepath
##  of an image as input.
def main(filePath, flag = 0):
    img = readImage(filePath)     ## Read image with specified filepath
    if len(img) == 440:           ## Dimensions of smaller maze image are 440x440
        size = 1
    else:
        size = 2
    maze_graph = buildGraph(img, size)   ## Build graph from maze image. Pass arguments as required
    start = findStartPoint(img, size)  ## Returns the coordinates of the start of the maze
    print start
    shortestPath = findPath(maze_graph, start, (0,0))  ## Find shortest path. Pass arguments as required.
    print shortestPath
    string = str(shortestPath) + "\n"
    for i in shortestPath:               ## Loop to paint the solution path.
        img = colourCell(img, i[0], i[1], size, 230)
    if __name__ == '__main__':     ## Return value for main() function.
        return img
    else:
        if flag == 0:
            return string
        else:
            return graph
## The main() function is called here. Specify the filepath of image in the space given.
if __name__ == "__main__":
    filepath = "image_00.jpg"     ## File path for test image
    img = main(filepath)          ## Main function call
    cv2.imshow("image",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
