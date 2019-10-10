#All using 2D representation -> Coplanar
import csv 

class Point():
    #Represents a point in space
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return "X: %f Y: %f" % (self.x, self.y)

#Placeholder class...Will be changed later when pointcheck is integrated
class Node():
    def __init__(self, currPoint, nextPoint):
        self.point = currPoint
        self.next = nextPoint
    def __str__(self):
        return "X: %f Y: %f" % (self.point.x, self.point.y)

class BoundaryBox():
    # Describes the x and y coordinates of the boundary
    # that shouldn't be crossed
    def __init__(self, point1, point2, label):
        #1 is left and bottom boundary
        #2 is right and top boundary
        self.point1 = point1
        self.point2 = point2
        self.label = label

    def validPoint(self, testPoint): #Checks if point is valid
        xNonValidity = (self.point1.x <= testPoint.x) and (self.point2.x >= testPoint.x)
        yNonValidity = (self.point1.y <= testPoint.y) and (self.point2.y >= testPoint.y)
        #Seperating two in case want feedback of error
        return not(xNonValidity and yNonValidity)
    
    def lineChecker(self, BPoint1, BPoint2, deltaX, deltaY): #Checks if line is not between boundary lines
        #BPoint means boundary point
        #For Mathematical logic, see docs on Github
        Bcross = (BPoint1.x*BPoint2.y) - (BPoint2.x*BPoint1.y) #Gets cross product of boundary points
        B1cross = (BPoint1.x*deltaY) - (deltaX*BPoint1.y) #Gets cross product between BPoint1 and testPoint vector
        B2cross = (BPoint2.x*deltaY) - (deltaX*BPoint2.y) #Gets cross product between BPoint2 and testPoint vector
        if (Bcross > 0):
            return not((B1cross > 0) and (B2cross < 0))
        elif (Bcross < 0):
            return not((B2cross > 0) and (B1cross < 0))
        else:
            print("Error in lineChecker")
            
    def notInRange(self, testPoint1, testPoint2):
        compare11x = testPoint1.x < self.point1.x
        compare12x = testPoint1.x > self.point2.x
        compare21x = testPoint2.x < self.point1.x
        compare22x = testPoint2.x > self.point2.x
        compare11y = testPoint1.y < self.point1.y
        compare12y = testPoint1.y > self.point2.y
        compare21y = testPoint2.y < self.point1.y
        compare22y = testPoint2.y > self.point2.y
        if (not(compare11x ^ compare21x) and not(compare12x ^ compare22x) and not(compare11y ^ compare21y) and not(compare12y ^ compare22y)):
            return True
        else:
            return False
    
    def validLine(self, testPoint1, testPoint2): #Checks if line between points is valid
        #testPoint1 is first point, testPoint2 is next point
        #assuming that validPoint is satisfied for both points
        if (self.notInRange(testPoint1, testPoint2)): #Checks if points are outside of boundary box domain
            return True
        deltaX = testPoint2.x - testPoint1.x
        deltaY = testPoint2.y - testPoint1.y
        #deltaX, deltaY describes vector components for points
        #See attached papers in github to understand logic and location
        if ((testPoint1.x <= self.point1.x) and (testPoint1.y >= self.point2.y)) or \
           ((testPoint1.x >= self.point2.x) and (testPoint1.y <= self.point1.y)):
            A = Point(self.point1.x, self.point1.y)
            C = Point(self.point2.x, self.point2.y)
            #Following conditions check to see if point 1 and point 2 are in same region
            return self.lineChecker(A, C, deltaX, deltaY)
        elif ((testPoint1.x <= self.point1.x) and (testPoint1.y <= self.point1.y)) or \
           ((testPoint1.x >= self.point2.x) and (testPoint1.y >= self.point2.y)):      
            B = Point(self.point1.x, self.point2.y)
            D = Point(self.point2.x, self.point1.y)
            return self.lineChecker(B, D, deltaX, deltaY)
        elif (testPoint1.x < self.point1.x):
            print("here")
            A = Point(self.point1.x, self.point1.y)
            B = Point(self.point1.x, self.point2.y)
            return self.lineChecker(A, B, deltaX, deltaY)
        elif (testPoint1.x > self.point2.x):
            C = Point(self.point2.x, self.point2.y)
            D = Point(self.point2.x, self.point1.y)
            return self.lineChecker(C, D, deltaX, deltaY)
        elif (testPoint1.y < self.point1.y):
            A = Point(self.point1.x, self.point1.y)
            D = Point(self.point2.x, self.point1.y)
            return self.lineChecker(A, D, deltaX, deltaY)
        elif (testPoint1.y > self.point2.y):
            B = Point(self.point1.x, self.point2.y)
            C = Point(self.point2.x, self.point2.y)
            return self.lineChecker(B, C, deltaX, deltaY)
        else:
            print("Error in ValidLine")

def main():
    boundaryList = [] #Initializes array to hold BoundaryBoxes
    NodeList = [] #Initializes array to hold Nodes -> Placeholder for now
    with open('boundaryPoints.csv', encoding='utf-8-sig') as csvfile: #Change csv file name as required
        csvReader = csv.reader(csvfile)
        #Format of csv: First two values are x1, y1 (Bottom left)
        #Second two values are x2, y2 (Top right)
        #Last value is a label
        for row in csvReader:
            Point1 = Point(float(row[0]), float(row[1]))
            Point2 = Point(float(row[2]), float(row[3]))
            boundaryRegion = BoundaryBox(Point1, Point2, row[4])
            boundaryList.append(boundaryRegion)
    #Below is just a placeholder until can play with tree structure and fix from there
    print("What boundary box conditions are valid?")
    conditions = [str(x) for x in input().split()]
    with open('testPoints.csv', encoding='utf-8-sig') as csvfileb: #Change csv file name as required
        csvReader2 = csv.reader(csvfileb)
        #Current point and next point on same row
        #First two x1, y1 are current point; x2, y2 next are for next point
        for row in csvReader2:
            testPoint = Point(float(row[0]), float(row[1]))
            nextPoint = Point(float(row[2]), float(row[3]))
            valid = True
            for box in boundaryList:
                if (not(box.label in conditions)):
                    continue
                if (box.validPoint(testPoint) and box.validPoint(nextPoint)):
                    if (not(box.validLine(testPoint, nextPoint))):
                        valid = False
                else:
                    valid = False
                if (not(valid)):
                    break
            if (valid):
                validNode = Node(testPoint, nextPoint)
                NodeList.append(validNode)
                print(validNode)

if __name__ == '__main__': #Implemented for usability of file in other files
    main()
