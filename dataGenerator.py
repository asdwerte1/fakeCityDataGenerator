import random
import os
import numpy as np

#Normal dist RNG for ages
rng = np.random.default_rng()

#LOCATION CLASS
#A class for creating objects for the different city districts
#There are 5 main city districts:
    #centre
    #industrial
    #inner
    #outer
    #suburb
#each district also has a north, south, east and west area, meaning there are a total 20 districts to generate
class Location:

    #intialise by setting the city district and its compa ss direction (e.g. center north, or outer west)
    def __init__(self, district, direction):
        self.district = district
        self.direction = direction

        #set key data: population density, congestion, accident rates, crime rates, noise pollution
        self.populationDensity = self.populationDensityGenerator(self.district)
        self.congestion = self.congesttionGenerator()
        self.accidentRate = self.accidentRateGenerator()
        self.noisePollution = self.noisePollutionGenerator()
        self.crimeRate = self.crimeRateGenerator()
        self.greenSpace = self.greenSpacesAmount()
        self.airQualityIndex = self.airQualityIndexGenerator()
        self.distanceToClosestHospital = self.findDistanceToHospital()
        self.ambulanceCalloutTime = self.findAmbulanceCalloutTime()
        self.accessToFitness = self.generateAccessToFitness()
        self.obesityRate = self.generateObesityRate()


    def populationDensityGenerator(self, district):
    
        #function to generate a biased population density
        if(district == "centre"): popDen = random.randrange(5000, 10000)
        elif(district == "industrial"): popDen = random.randrange(250, 500)
        elif(district =="inner"): popDen = random.randrange(1000, 5000)
        elif(district == "outer"): popDen = random.randrange(500, 1000)
        elif(district == "suburb"): popDen = random.randrange(50, 200)
        return popDen

    def congesttionGenerator(self):
        #set the congestion levels (cars passing a point per hour)
        congestion = (random.randrange(150, 200) / 100) * self.populationDensity
        return int(congestion)

    def accidentRateGenerator(self):
        #generate an accident rate per 100000 people
        #create a base rate
        accRate = random.randrange(0, 10)
        if(self.district == "centre"): accRate += random.randrange(20, 30) + int(self.congestion / 100)
        elif(self.district == "industrial"): accRate += random.randrange(80, 140) + int(self.congestion / 10)
        elif(self.district == "inner"): accRate += random.randrange(10, 20) + int(self.congestion / 100)
        elif(self.district == "outer"): accRate += random.randrange(5, 10) + int(self.congestion / 10)
        elif(self.district == "suburb"): accRate += random.randrange(2, 8) + int(self.congestion)
        return accRate
    
    def noisePollutionGenerator(self):
        #generate a noise pollution in dB
        standard = 70
        if(self.district == "centre"): noisePoll = standard + random.randrange(10, 25)
        elif(self.district == "industrial"): noisePoll = standard + random.randrange(18, 25)
        elif(self.district == "inner"): noisePoll = standard + random.randrange(10, 15)
        elif(self.district == "outer"): noisePoll = standard + random.randrange(-5, 5)
        elif(self.district == "suburb"): noisePoll = standard + random.randrange(-15, -5)
        return noisePoll

    def crimeRateGenerator(self): 
        #function to create a crime rate per 100000
        #create a multiplier based on location
        if(self.district == "centre"): multiplier = 2.5
        elif(self.district == "industrial"): multiplier = 1.5
        elif(self.district == "inner"): multiplier = 4.5
        elif(self.district == "outer"): multiplier = 1.2
        elif(self.district == "suburb"): multiplier = 0.6
        crimeRate = random.randrange(1, int(self.populationDensity * 0.05)) * multiplier
        return int(crimeRate)
    
    def greenSpacesAmount(self):
        #function to define the green space available in a district given as a percentage of total space
        if(self.district =="centre"): greenSpace = random.randrange(100, 300) / 10
        elif(self.district=="industrial"): greenSpace = random.randrange(0, 50) / 10
        elif(self.district == "inner"): greenSpace = random.randrange(0, 100) / 10
        elif(self.district == "outer"): greenSpace = random.randrange(200, 400) / 10
        elif(self.district == "suburb"): greenSpace = random.randrange(600, 800) / 10
        return greenSpace

    def airQualityIndexGenerator(self):
        aqi = ((20000 - self.congestion) / 20000) * 10
        #update aqi based on green space in district - only for poor air quiality areas
        if(aqi < 5):
            aqi += self.greenSpace / 10
        return round(aqi, 2)
    
    def generateAccessToFitness(self):
        #decide if there is fitness facilities within the district - use a D20 style choice make
        #Gym most likely in city centre, outer city and suburb
        decider = random.randrange(1, 20)
        gym = False
        if(self.district == "centre"):
            if(decider >= 3):
                gym = True
        elif(self.district == "industrial"):
            if(decider == 20):
                gym = True
        elif(self.district == "inner"):
            if(decider >= 10):
                gym = True
        elif(self.district == "outer"):
            if(decider >= 5):
                gym = True
        elif(self.district == "suburb"):
            if(decider >= 6):
                gym = True
        return gym
    
    def generateObesityRate(self):
        #function to generate an obesity rate as a percentage
        #start with base value 20% - use factors to decide on increases or decreases based on location factors
        rate = 20
        if(self.greenSpace > 75):
            rate -= random.randrange(5, 10)
        elif(self.greenSpace < 35):
            rate += random.randrange(5, 10)

        if(self.accessToFitness == True):
            rate -= random.randrange(5, 10)
        else:
            rate += random.randrange(10, 20)

        if(self.distanceToClosestHospital > 6):
            rate += random.randrange(10, 20)

        if(self.district == "industrial" or self.district == "inner"):
            #use a dice roll to possible add more
            roll = random.randrange(1, 20)
            if(roll < 8):
                rate += random.randrange(25, 35)
        return rate
    
    #this function will find the distance from the current district to the nearest hospital
    #given as a value based on number of districts between - max is 9 min is 0
    def findDistanceToHospital(self):
        #the city hospitls are located in the east outer city housing and the south city centre
        #to find the distance, a random number generation will be used along with a multiplier based on
        #the location district - this multiplier will be found using horizontal and vertical dimensions, no
        #"arcing" movements causing reduced distances
        if(self.district == "centre"):
            if(self.direction == "north"): distance = 1
            elif(self.direction == "east"): distance = 1
            elif(self.direction == "south"): distance = 0
            elif(self.direction == "west"): distance = 1
        elif(self.district == "industrial"):
            if(self.direction == "north"): distance = 2
            elif(self.direction == "east"): distance = 2
            elif(self.direction == "south"): distance = 1
            elif(self.direction == "west"): distance = 2
        elif(self.district == "inner"):
            if(self.direction == "north"): distance = 2
            elif(self.direction == "east"): distance = 1
            elif(self.direction == "south"): distance = 2
            elif(self.direction == "west"): distance = 3
        elif(self.district == "outer"):
            if(self.direction == "north"): distance = 1
            elif(self.direction == "east"): distance = 0
            elif(self.direction == "south"): distance = 3
            elif(self.direction == "west"): distance = 4
        elif(self.district == "suburb"):
            if(self.direction == "north"): distance = 2
            elif(self.direction == "east"): distance = 1
            elif(self.direction == "south"): distance = 4
            elif(self.direction == "west"): distance = 5
        #generate a random multiplier - convert distance to suitbale miles value
        multiplier = random.randrange(2, 4)
        return distance * multiplier
    
    def findAmbulanceCalloutTime(self):
        #function to generate the ambulance callout time to the given location, given in minutes
        #this is based on the distance to closest hospital
        if(self.distanceToClosestHospital <= 4): return random.randrange(3, 5)
        elif(self.distanceToClosestHospital <= 8): return random.randrange(6, 15)
        else: return random.randrange(16, 30)

#END OF LOCATION CLASS

#INDIVIDUAL CLASS
#A class to create objects representing individual people within the city
#Each will be given a unique identifer, and assigned a portion of the city that they live in, then factors will be used to determine other
#values for the individual
        
relationshipStatues = ["single", "in a relationship", "married"]
                 #0          1         2          3            4               5               6
employments = ["public", "finance", "health", "private", "construction", "manufacturing", "self-employed"]
                  #0      1       2        3        4
stressLevels = ["none", "low", "medium", "high", "severe"]
class Individual:
    id = 1
    def __init__(self) -> None:

        self.id = Individual.id
        Individual.id += 1
        
        self.age = (int)(abs(rng.normal()) * 85)
        if self.age > 100: self.age = (self.age // 2) - 20
        if self.age < 10: self.age += 10

        self.location = self.setLocation()

        self.respirationIssues = self.setRespIssues()

        self.obesity = self.setObesity()

        self.relationshipStatus = self.setRelStatus()

        if self.age <= 18:
            self.employmentStatus = "student"
        elif self.age > 65:
            self.employmentStatus = "retired"
        else:
            self.employmentStatus = self.setEmploymentStatus()

        self.stress = self.setStressLevels()

    def setLocation(self):
        roll1 = random.randrange(1, 21)
        roll2 = random.randrange(1, 5)

        if roll1 <= 8: district = "centre"
        elif roll1 <= 12: district = "inner"
        elif roll1 <= 14:  district = "outer"
        elif roll1 <= 16: district = "industrial"
        else: district = "suburb"
        
        match(roll2):
            case 1:
                direction = "north"
            case 2:
                direction = "east"
            case 3:
                direction = "south"
            case 4: 
                direction = "west"
        
        return locations[f"{district} {direction}"]
    
    def setRespIssues(self):
        roll = round(random.randrange(1, 61) / 2, 2)
        if roll + self.location.airQualityIndex > 13: return True
        else: return False

    def setObesity(self):
        roll = random.randrange(1, 51)
        chance = roll + self.location.obesityRate
        if self.location.accessToFitness: chance -= 45
        if chance > 85: return True
        else: return False

    def setRelStatus(self):
        if self.age < 18: return relationshipStatues[0]
        roll = random.randrange(1, 11)
        if self.location == centreEast or self.location == centreNorth or self.location == centreSouth or self.location == centreWest:
            if roll <= 6: return relationshipStatues[0]
            elif roll <= 9: return relationshipStatues[1]
            else: return relationshipStatues[2]
        elif self.location == industrialNorth or self.location == industrialEast or self.location == industrialSouth or self.location == industrialWest:
            if roll <= 7: return relationshipStatues[0]
            elif roll <= 9: return relationshipStatues[1]
            else: return relationshipStatues[2]
        elif self.location == innerNorth or self.location == innerEast or self.location == innerSouth or self.location == innerWest:
            if roll <= 5: return relationshipStatues[0]
            elif roll <= 8: return relationshipStatues[1]
            else: return relationshipStatues[2]
        elif self.location == outerNorth or self.location == outerEast or self.location == outerSouth or self.location == outerWest:
            if roll <= 4: return relationshipStatues[0]
            elif roll <= 7: return relationshipStatues[1]
            else: return relationshipStatues[2]
        else:
            if roll <= 2: return relationshipStatues[0]
            elif roll <= 5: return relationshipStatues[1]
            else: return relationshipStatues[2]

    def setEmploymentStatus(self):
        roll = random.randrange(1, 7)
        match(self.location.district):
            case "centre":
                if roll <= 3: return employments[3]
                elif roll <= 5: return employments[1]
                else: return employments[random.randrange(0, len(employments))]
            case "industrial":
                if roll <= 4: return employments[5]
                else: return employments[random.randrange(0, len(employments))]
            case "inner":
                if roll <= 2: return "private"
                elif roll <= 4: return "public"
                else: return employments[random.randrange(0, len(employments))]
            case "outer":
                return employments[random.randrange(0, len(employments))]
            case "suburb":
                if roll <= 2: return employments[6]
                else: return employments[random.randrange(0, len(employments))]
    
    def setStressLevels(self):
        match(self.employmentStatus):
            case "public":
                return stressLevels[random.randrange(2, 4)]
            case "finance":
                return stressLevels[random.randrange(2, 5)]
            case "health":
                return stressLevels[random.randrange(3, 4)]
            case "private":
                return stressLevels[random.randrange(1, 4)]
            case "construction":
                return stressLevels[random.randrange(1, 3)]
            case "manufacturing":
                return stressLevels[random.randrange(0, 4)]
            case "self-employed":
                return stressLevels[random.randrange(2, 5)]
            case "student":
                return stressLevels[random.randrange(3, 5)]
            case "retired":
                return stressLevels[random.randrange(0, 2)]


#END OF INDIVIDUAL CLASS

#CREATE LOCATION OBJECTS

centreNorth = Location("centre", "north")
centreEast = Location("centre", "east")
centreSouth = Location("centre", "south")
centreWest = Location("centre", "west")
industrialNorth = Location("industrial", "north")
industrialEast = Location("industrial", "east")
industrialSouth = Location("industrial", "south")
industrialWest = Location("industrial", "west")
innerNorth = Location("inner", "north")
innerEast = Location("inner", "east")
innerSouth = Location("inner", "south")
innerWest = Location("inner", "west")
outerNorth = Location("outer", "north")
outerEast = Location("outer", "east")
outerSouth = Location("outer", "south")
outerWest = Location("outer", "west")
suburbNorth = Location("suburb", "north")
suburbEast = Location("suburb", "east")
suburbSouth = Location("suburb", "south")
suburbWest = Location("suburb", "west")

locations = {
    "centre north": centreNorth,
    "centre east": centreEast,
    "centre south": centreSouth,
    "centre west": centreWest,
    "industrial north": industrialNorth,
    "industrial east": industrialEast,
    "industrial south": industrialSouth,
    "industrial west": industrialWest,
    "inner north": innerNorth,
    "inner east": innerEast,
    "inner south": innerSouth,
    "inner west": innerWest,
    "outer north": outerNorth,
    "outer east": outerEast,
    "outer south": outerSouth,
    "outer west": outerWest,
    "suburb north": suburbNorth,
    "suburb east": suburbEast,
    "suburb south": suburbSouth,
    "suburb west": suburbWest
    }

#END OF LOCATION OBJECT CREATION

#Functions to write data to the output files
def writeLocationToFile(object, file):
    line_to_write = f"\n{object.direction} {object.district},{object.populationDensity},{object.congestion},{object.accidentRate},{object.noisePollution},{object.crimeRate},{object.greenSpace},{object.airQualityIndex},{object.distanceToClosestHospital},{object.ambulanceCalloutTime},{object.accessToFitness},{object.obesityRate}"
    file.write(line_to_write)

def writePersonToFile(object, file):
    line_to_write = f"\n{object.id},{object.age},{object.location.direction} {object.location.district},{object.respirationIssues},{object.obesity},{object.relationshipStatus},{object.employmentStatus},{object.stress}"
    file.write(line_to_write)

#Open files to write the data to
#first check if file exists, and delete if so
complete = False
while complete != True:
    try:
        if(os.path.exists("locations.csv")):
            print("Attempting to delete existing locations.csv")
            os.remove("locations.csv")
            print("Existing locations.csv deleted")
            locationFile = open("locations.csv", "a")
            print("New locations.csv opened")
        else:
            locationFile = open("locations.csv", "a")
            print("locatons.csv opened")
            #write out the correct headings
    except PermissionError:
        print("The file locations.csv is currently open so cannot be removed or edited, please close the file.\nThen hit enter to try again.")
        input()
    try:
        if(os.path.exists("people.csv")):
            print("Attempting to delete existing people.csv")
            os.remove("people.csv")
            print("Existing people.csv deleted")
            peopleFile = open("people.csv", "a")
            print("New people.csv opened")
        else:
            peopleFile = open("people.csv", "a")
            print("people.csv opened")
            #write out the correct headings
    except PermissionError:
        print("The file people.csv is currently open so cannot be removed or edited, please close the file.\nThen hit enter to try again.")
        input()
    else:
        complete = True
#Create the headers within the location and people file
locationFile.write("City District,\
                    Population Density (per square km),\
                    Congestion (Cars per hour at peak time),\
                    Accident Rate (per 100000),\
                    Noise Pollution (dB),\
                    Crime Rate (per 100000),\
                    Green Space (percentage of total land),\
                    Air Quality Index,\
                    Distance to Nearest Hospital (miles),\
                    Average Ambulance Callout Time (minutes),\
                    Access to fitness facilities,\
                    Obesity Rate (percentage)")

peopleFile.write("ID,\
                 Age,\
                 Location,\
                 Respiratory Issues,\
                 Obese,\
                 Relationship Status,\
                 Employment Status,\
                 Stress")

#Create objects for people and write data out to file
for i in range (10000):
    person = Individual()
    writePersonToFile(person, peopleFile)

# Write location data to file
writeLocationToFile(centreNorth, locationFile)
writeLocationToFile(centreEast, locationFile)
writeLocationToFile(centreSouth, locationFile)
writeLocationToFile(centreWest, locationFile)
writeLocationToFile(industrialNorth, locationFile)
writeLocationToFile(industrialEast, locationFile)
writeLocationToFile(industrialSouth, locationFile)
writeLocationToFile(industrialWest, locationFile)
writeLocationToFile(innerNorth, locationFile)
writeLocationToFile(innerEast, locationFile)
writeLocationToFile(innerSouth, locationFile)
writeLocationToFile(innerWest, locationFile)
writeLocationToFile(outerNorth, locationFile)
writeLocationToFile(outerEast, locationFile)
writeLocationToFile(outerSouth, locationFile)
writeLocationToFile(outerWest, locationFile)
writeLocationToFile(suburbNorth, locationFile)
writeLocationToFile(suburbEast, locationFile)
writeLocationToFile(suburbSouth, locationFile)
writeLocationToFile(suburbWest, locationFile)