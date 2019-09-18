import numpy as np
import cv2
import math
import time
import copy
## Reads image in HSV format. Accepts filepath as input argument and returns the HSV
## equivalent of the image.
def readImageHSV(filePath):
    mazeImg = cv2.imread(filePath)
    hsvImg = cv2.cvtColor(mazeImg, cv2.COLOR_BGR2HSV)
    return hsvImg

## Reads image in binary format. Accepts filepath as input argument and returns the binary
## equivalent of the image.
def readImageBinary(filePath):
    mazeImg = cv2.imread(filePath)
    grayImg = cv2.cvtColor(mazeImg, cv2.COLOR_BGR2GRAY)
    ret,binaryImage = cv2.threshold(grayImg,200,255,cv2.THRESH_BINARY)
    return binaryImage

##  Returns sine of an angle.
def sine(angle):
    return math.sin(math.radians(angle))

##  Returns cosine of an angle
def cosine(angle):
    return math.cos(math.radians(angle))

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

## The findMarkers() function returns a list of coloured markers in form of a python dictionaries
## For example if a blue marker is present at (3,6) and red marker is present at (1,5) then the
## dictionary is returned as :-
##          list_of_markers = { 'Blue':(3,6), 'Red':(1,5)}
def findMarkers(img):
    list_of_markers = {}

    bgr = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    im = copy.copy(bgr)                                                                             ## Converting the image to grayscale
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,153,255,0)                                                     ## Obtaining binary image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(1,len(contours)):                                                                ## Skipping the first contour as it the whole grid
        M = cv2.moments(contours[i])                                                                ## Moment of contour i
        cx = int(M['m10']/M['m00'])                                                                 ## X coordinate of centroid of contour i
        cy = int(M['m01']/M['m00'])                                                                 ## Y coordinate of centroid of contour i
        value = color(im, cx, cy)
        if value!=0:
            list_of_markers.update(value)

    return list_of_markers

## The findOptimumPath() function returns a python list which consists of all paths that need to be traversed
## in order to start from the START cell and traverse to any one of the markers ( either blue or red ) and then
## traverse to FINISH. The length of path should be shortest ( most optimal solution).
def findOptimumPath(img, listOfMarkers, initial_point, final_point, size): 
    pathArray = []

    graph = buildGraph(img, size)
    pathArray = graph
    for k1, v1 in listOfMarkers.iteritems():                    ## Grab the coordinates of a markers from list of markers
        p1 = [findPath(graph, initial_point, v1)]               ## find shortest path from initial point to the marker point
        for k2, v2 in listOfMarkers.iteritems():                ## Grab another marker from list of markers
            if v1!=v2:                                          ## Check if the markers are not same
                p1+=[findPath(graph, v1, v2)]                   ## Add path from previous marker to next marker
        p1+=[findPath(graph, v2, final_point)]                  ## find shortest path from marker point to final point
        if(len(p1)<len(pathArray)):                        
            pathArray = []                             
            pathArray+=p1                                      ## Add total paths to be traversed by starting from bottom left, collecting all markers and reaching top right corner

    return pathArray

## The colourPath() function highlights the whole path that needs to be traversed in the maze image and
## returns the final image.
def colourPath(img, pathArray, size):

    for path in pathArray:                                      ## Loop to paint the solution path.
        for i in path:
            img = colourCell(img, i[0], i[1], size, 230)

    return img

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

'''
*Function Name: color
*Input:         img  -> image
                x    -> X Co-ordinate of point
                y    -> Y Co-ordinate of point
*Output:        Python Dictionary -> Conatining Colored points with co-ordinates
*Logic:         Checks for the color value of the point and returns python dictionary for that color with position
*Sample Call:   color(img, 230, 320)
'''
def color(img, x, y):
    b, g, r = img[y, x]
    r_sq = (x-len(img)/2)**2 + (y-len(img)/2)**2
    level = (int)(r_sq**(1/2.0))/40
    tan = (y-len(img))/(x-len(img))
    theta = math.degrees(math.atan(tan))
    theta0 = 360.0/val[level-1]
    cellnum= (int)(theta/theta0)+1
    if x<220 and y>220:
        cellnum=cellnum+val[level-1]/4
    if x<220 and y<220:
        cellnum=cellnum+val[level-1]/2
    if x>220 and y<220:
        cellnum=cellnum+3*val[level-1]/4
    if b in range(230,256) and g in range(0,26) and r in range(0,26):           ## RGB range for Blue coloured cell
        return {'Blue' :(level,cellnum)}                                            ## Retun cell co-ordinates of Blue cell
    elif b in range(0,26) and g in range(0,26) and r in range(230,256):         ## RGB range for Red coloured cell
        return {'Red' :(level,cellnum)}                                             ## Retun cell co-ordinates of Red cell
    return 0

## This is the main() function for the code.

def main(filePath, flag = 0):
    img = readImageHSV(filePath)
    imgBinary = readImageBinary(filePath)
    if len(img) == 440:
        size = 1
    else:
        size = 2
    listofMarkers = findMarkers(img)
    path = findOptimumPath(imgBinary, listofMarkers, findStartPoint(imgBinary, size), (0,0), size)
    img = colourPath(imgBinary, path, size)
    print path
    print listofMarkers
    if __name__ == "__main__":                    
        return img
    else:
        if flag == 0:
            return path
        elif flag == 1:
            return str(listofMarkers) + "\n"
        else:
            return img
    
## The main() function is called here. Specify the filepath of image in the space given.
if __name__ == "__main__":
    filePath = "image_00.jpg"     ## File path for test image
    img = main(filePath)           ## Main function call
    cv2.imshow("image",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
