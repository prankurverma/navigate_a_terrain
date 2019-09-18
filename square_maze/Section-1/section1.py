import numpy as np
import cv2

## The readImage function takes a file path as argument and returns image in binary form.
def readImage(filePath):

    img = cv2.imread(filePath)                              ## Read image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)            ## Convert image to grayscale image
    ret, binaryImage = cv2.threshold(gray, 127, 255, 0)     ## Convert image to Binary image

    return binaryImage

## The findNeighbours function takes a maze image and row and column coordinates of a cell as input arguments
## and returns a stack consisting of all the neighbours of the cell as output.
## Note :- Neighbour refers to all the adjacent cells one can traverse to from that cell provided only horizontal
## and vertical traversal is allowed.
def findNeighbours(img,row,column):
    neighbours = []

    if img[20*row+10, 20*column+1]>=51:                     ## Check the left edge pixel value
        neighbours.append((row, column-1))                  ## If true decrease column value and return left cell coordinate
    if img[20*row+1, 20*column+10]>=51:                     ## Check the upper edge pixel value
        neighbours.append((row-1, column))                  ## If true decrease row value and return upper cell coordinate
    if img[20*row+19, 20*column+10]>=51:                    ## Check the lower edge pixel value
        neighbours.append((row+1, column))                  ## If true increase row value and return lower cell coordinate
    if img[20*row+10, 20*column+19]>=51:                    ## Check the right edge pixel value
        neighbours.append((row, column+1))                  ## If true increase column value and return right cell coordinate

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

    for i in range(20*row,20*row+20):                       ## Specify row range of a cell to be highlighted
        for j in range(20*column,20*column+20):             ## Specify column range of a cell to be highlighted
            if img[i,j]==255:                               ## Only empty white spaces with value=255 are highlighted with colourVal
                img[i,j]=colourVal

    return img

##  Main function takes the filepath of image as input.

def main(filePath):
    img = readImage(filePath)
    coords = [(0,0),(9,9),(3,2),(4,7),(8,6)]
    string = ""
    for coordinate in coords:
        img = colourCell(img, coordinate[0], coordinate[1], 150)
        neighbours = findNeighbours(img, coordinate[0], coordinate[1])
        print neighbours
        string = string + str(neighbours) + "\n"
        for k in neighbours:
            img = colourCell(img, k[0], k[1], 230)
    if __name__ == '__main__':
        return img
    else:
        return string + "\t"

## Specify filepath of image here. The main function is called in this section.

if __name__ == '__main__':
    filePath = 'maze09.jpg'
    img = main(filePath)
    cv2.imshow('canvas', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
