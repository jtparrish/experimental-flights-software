#All using 2D representation -> Coplanar
import csv 

class Point():
	#Represents a point in space
	def __init__(self, x, y):
		self.x = x
		self.y = y

#Placeholder class...Will be changed later when pointcheck is integrated
class Node():
	def __init__(self, currPoint, nextPoint)
		self.point = currPoint
		self.next = nextPoint

class BoundaryBox():
	# Describes the x and y coordinates of the boundary
	# that shouldn't be crossed
	def __init__(self, point1, point2):
		#1 is left and bottom boundary
		#2 is right and top boundary
		self.point1 = point1
		self.point2 = point2

    def validPoint(self, testPoint): #Checks if point is valid
    	xNonValidity = (self.point1.x <= testPoint.x) and (self.point2.x >= testPoint.x)
    	yNonValidity = (self.point1.y <= testPoint.y) and (self.point2.y >= testPoint.y)
    	#Seperating two in case want feedback of error
    	return not(xNonValidity and yNonValidity)
    
    def validLine(self, testPoint1, testPoint2): #Checks if line between points is valid
    	#testPoint1 is first point, testPoint2 is next point
    	#assuming that validPoint is satisfied for both points
    	deltaX = testPoint2.x - testPoint1.x
    	deltaY = testPoint2.y - testPoint1.y
    	#deltaX, deltaY describes vector components for points
        deltaXB = 0;
        deltaYB = 0;
        #deltaXB, deltaYB describes vector components from testPoint1 to
        #applicable boundary box position
        #See attached papers in github to understand logic and location
    	if ((testPoint1.x <= self.point1.x) and (testPoint1.y >= self.point2.y)) or \
    	   ((testPoint1.x >= self.point2.x) and (testPoint1.y <= self.point1.y)):
    		A = Point(self.point1.x, self.point1.y)
    		C = Point(self.point2.x, self.point2.y)
    		return lineChecker(A, C, deltaX, deltaY)
    	elif ((testPoint1.x <= self.point2.x) and (testPoint1.y >= self.point1.y)) or \
    	   ((testPoint1.x >= self.point1.x) and (testPoint1.y <= self.point2.y)):	   
    	   	B = Point(self.point1.x, self.point2.y)
    		D = Point(self.point2.x, self.point1.y)
    		return lineChecker(B, D, deltaX, deltaY)
    	elif (testPoint1.x < self.point1.x):
    		A = Point(self.point1.x, self.point1.y)
    		B = Point(self.point1.x, self.point2.y)
    		return lineChecker(A, B, deltaX, deltaY)
    	elif (testPoint1.x > self.point2.x):
    		C = Point(self.point2.x, self.point2.y)
    		D = Point(self.point2.x, self.point1.y)
    		return lineChecker(C, D, deltaX, deltaY)
    	elif (testPoint1.y < self.point1.y):
    		A = Point(self.point1.x, self.point1.y)
    		D = Point(self.point2.x, self.point1.y)
    		return lineChecker(A, D, deltaX, deltaY)
    	elif (testPoint1.y > self.point2.y):
    		B = Point(self.point1.x, self.point2.y)
    		C = Point(self.point2.x, self.point2.y)
    		return lineChecker(B, C, deltaX, deltaY)
    	else:
    		print("Error in ValidLine")

    def lineChecker(BPoint1, BPoint2, deltaX, deltaY): #Checks if line is not between boundary lines
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

def main():
	boundaryList = [] #Initializes array to hold BoundaryBoxes
	NodeList = [] #Initializes array to hold Nodes -> Placeholder for now
	with open('boundaryPoints.csv') as csvfile: #Change csv file name as required
		csvReader = csv.reader(csvfile, delimiter = ',')
		#Format of csv: First two values are x1, y1 (Bottom left)
		#Second two values are x2, y2 (Top right)
		for row in csvReader:
			Point1 = Point(float(row[0]), float(row[1]))
			Point2 = Point(float(row[2]), float(row[3]))
			boundaryRegion = BoundaryBox(Point1, Point2)
			boundaryList.append(boundaryRegion)
	#Below is just a placeholder until can play with tree structure and fix from there
	with open('testPoints.csv') as csvfile: #Change csv file name as required
		csvReader2 = csv.reader(csvfile, delimiter = ',')
		#Current point and next point on same row
		#First two x1, y1 are current point; x2, y2 next are for next point
		for row in csvReader2:
			testPoint = Point(float(row[0]), float(row[1]))
			nextPoint = Point(float(row[2]), float(row[3]))
			valid = true
			for box in boundaryList:
				if (box.validPoint(testPoint) and box.validPoint(nextPoint)):
					if (not(box.validLine(testPoint, nextPoint))):
						valid = false
				else:
					valid = false
				if (not(valid)):
					break
			if (valid):
				validNode = Node(testPoint, nextPoint)
				NodeList.append(validNode)

if __name__ == '__main__': #Implemented for usability of file in other files
	main()
