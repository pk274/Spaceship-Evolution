# Spaceship evolution

# Entity is 11x11 Tuple of different components.
# 2 Entities race for resources in each run.
# Each generation consists of 3 runs.
# Win 1 run: survive. Win 2 runs: replicate. Win 3 runs: double replicate


# Blocks are:

# 1: Heart component. Block that is cpable of replication and therefore
# necessary for survival. Energy +5, weight +1

# 2: Basic buildingblock. This component can be used to connect components
# of your ship or as protection from weapons. Energy 0, weight +1

# 3: Engine. Speedbonus. Energy -1, weight +1

# 4: Weapon. Destroys a random of the foremost blocks of the enemy.
# Energy -1, weight +1

# 5: Generator. Energy + 2, weight +1

#6: Sensor. Energy -1, weight +1

import numpy as np
import random
import time
#import matplotlib.pyplot as plt


# TODO: Make weapons and sensors dependend on energy

class PartTracker:
    
    def __init__(self):
        self.numBasicBlocks = 0
        self.numEngines = 0
        self.numWeapons = 0
        self.numSensors = 0
        self.numGenerators = 0
        self.numBasicBlocksHistory = []
        self.numEnginesHistory = []
        self.numWeaponsHistory = []
        self.numSensorsHistory = []
        self.numGeneratorsHistory = []

    def increasePart(self, x):
        if (x == 2):
            self.numBasicBlocks += 1
        elif (x == 3):
            self.numEngines += 1
        elif (x == 4):
            self.numWeapons += 1
        elif (x == 5):
            self.numGenerators += 1
        elif (x == 6):
            self.numSensors += 1

    def resetParts(self):
        self.numBasicBlocks = 0
        self.numEngines = 0
        self.numWeapons = 0
        self.numSensors = 0
        self.numGenerators = 0

    def archive(self):
        self.numBasicBlocksHistory += [self.numBasicBlocks]
        self.numEnginesHistory += [self.numEngines]
        self.numWeaponsHistory += [self.numWeapons]
        self.numSensorsHistory += [self.numSensors]
        self.numGeneratorsHistory += [self.numGenerators]

    def doPlotting(self):
        referenceList = []
        referenceValue = 0
        for i in range(len(self.numEnginesHistory)):
            referenceList += [referenceValue]
            referenceValue += 1
        plt.plot(referenceList, self.numEnginesHistory)
        plt.show()

        

#partTracker = PartTracker()

class Spaceship:
    
    def __init__(self, newStructure = None, newMaxAge = 3):
        self.structure = []
        if (newStructure is None):
            #create new Startstructure
            newStructure = []
            for i in range(11):
                line = [[0 for j in range(11)]]
                newStructure += line
            newStructure[5][5] = 1

        for i in range(11):
            col = []
            for j in range(11):
                col += [newStructure[i][j]]
            self.structure += [col]

        self.weight = 0
        self.available_energy = 0
        self.used_energy = 0
        self.age = 0
        self.maxAge = 0
        self.maxAge += newMaxAge
        self.mutationChance = 0.001
        self.runWins = 0
        self.numEngines = 0
        self.upperEngines = 0
        self.lowerEngines = 0
        self.numWeapons = 0
        self.numSensors = 0
        self.damagedWeapons = 0
        self.damagedEngines = 0
        self.width = 0
        self.length = 0
        self.leftBound = 12
        self.rightBound = -1
        self.upperBound = 12
        self.lowerBound = -1
        for i in range(0, 11):
            for j in range(0, 11):
                pixel = self.structure[i][j]
                if (pixel == 0):
                    continue
                if (j < self.leftBound):
                    self.leftBound = j
                if (j > self.rightBound):
                    self.rightBound = j
                if (i < self.upperBound):
                    self.upperBound = i
                if (i > self.lowerBound):
                    self.lowerBound = i

                if (pixel == 1):
                    self.available_energy += 6
                    self.weight += 1
                    self.used_energy += 1
                elif (pixel == 2):
                    self.weight += 0.5
                elif (pixel == 3):
                    self.used_energy += 1
                    self.weight += 1
                    if (j == 0 or self.structure[i][j-1] == 0):
                        self.numEngines += 1
                        if (i < 5): self.upperEngines += 1
                        if (i > 5): self.lowerEngines += 1
                elif (pixel == 4):
                    self.used_energy += 1
                    self.weight += 1
                    if (j == 10 or self.structure[i][j+1] == 0):
                        self.numWeapons += 1
                elif (pixel == 5):
                    self.available_energy += 3
                    self.weight += 1
                elif (pixel == 6):
                    self.used_energy += 1
                    self.weight += 1
                    self.numSensors += 1

        self.width = self.lowerBound - self.upperBound + 1
        self.length = self.rightBound - self.leftBound + 1
        self.speed = 1 + 2 * (self.numEngines - self.damagedEngines)**2 *\
        min(self.available_energy / self.used_energy, 1) / self.weight *\
       (self.length / self.width)**2 * (self.numEngines - abs(self.upperEngines - self.lowerEngines))
        


    def updateSpeed(self):
        self.speed = 1 + 2 * (self.numEngines - self.damagedEngines)**2 *\
        min(self.available_energy / self.used_energy, 1) / self.weight *\
       (self.length / self.width)**2 * (self.numEngines - abs(self.upperEngines - self.lowerEngines))
    



    def blockHasNeighbor(self, i, j) -> bool:
        x = i + 1
        if (x <= 10 and self.structure[x][j] != 0):
            return True
        y = j + 1
        if (y <= 10 and self.structure[i][y] != 0):
            return True
        z = i - 1
        if (z >= 0 and self.structure[z][j] != 0):
            return True
        w = j - 1
        if (w >= 0 and self.structure[i][w] != 0):
            return True
        return False
    
    def sayHello(self):
        print("I am a starship\n my weight is", self.weight)
    
    def replicate(self):
        newStructure = self.structure
        for i in range(0, 11):
            for j in range(0, 11):
                rand1 = random.random()
                if (rand1 > 1 - self.mutationChance and self.structure[i][j] != 1 and self.blockHasNeighbor(i, j)):
                    newPart = random.randint(2, 6)
                    #partTracker.increasePart(newPart)
                    #partTracker.archive()
                    newStructure[i][j] = newPart
        rand2 = random.random()
        newMaxAge = self.maxAge
        if (rand2 > 1 - self.mutationChance):
            newMaxAge += 1
        elif (rand2 < self.mutationChance):
            newMaxAge -= 1

        newShip = Spaceship(newStructure, newMaxAge)
        return newShip

    def printShip(self):
        string = ""
        for i in range(11):
            for j in range(11):
                pixel = self.structure[i][j]
                if (pixel == 0):
                    string += " "
                elif (pixel == 1):
                    string += str(chr(129))
                elif (pixel == 2):
                    string += "H"
                elif (pixel == 3):
                    string += "~"
                elif (pixel == 4):
                    string += "="
                elif (pixel == 5):
                    string += "#"
                elif (pixel == 6):
                    string += "O"
            string += "\n"
        string += "\n\n"
        print(string)



    
class Simulation:
    
    def __init__(self, starters1 = 100, populations = 4, generations1 = 80, runs1 = 3, resources1 = 800, outputLength1 = 40):
        self.starters = starters1
        self.populations = populations
        self.generations = generations1
        self.runs = runs1
        self.resources = resources1
        self.outputLength = outputLength1
        self.ships = []
        self.readyShips = []
        self.doneShips = []
        self.metaShips = []
        for n in range(self.starters):
            self.ships += [Spaceship()]

    def runMetaSimulation(self):
        for n in range(self.populations):
            self.runSimulation()
            self.resetShips()
            #partTracker.resetParts()
        for i in range(len(self.metaShips)):
            self.ships += [self.metaShips[i]]
        self.runSimulation()
        #print(partTracker.numEnginesHistory)
        #partTracker.doPlotting()

    def resetShips(self):
        self.ships = []
        self.doneSHips = []
        self.readyShips = []
        for n in range(self.starters):
            self.ships += [Spaceship()]


    def runSimulation(self):
        for n in range(self.generations):
            print("\rGeneration:", n, "   ", "    ", "Number of ships in population:", len(self.ships))
            printWinner = False
            if (n % 100 == 0): printWinner = True
            self.runGeneration(printWinner)
        self.runFinalRound()
        print("The winners are:")
        for a in range(len(self.ships)):
            self.metaShips += [self.ships[a]]
            self.ships[a].printShip()



    def runFinalRound(self):
        while (len(self.ships) > self.outputLength):
            if (len(self.ships) % 100 == 0):
                print("Knockout-phase! Ships left:", len(self.ships))
            i1 = random.randint(0, len(self.ships) - 1)
            ship1 = self.ships[i1]
            self.ships.pop(i1)
            i2 = random.randint(0, len(self.ships) - 1)
            ship2 = self.ships[i2]
            self.ships.pop(i2)
            if (ship1.numSensors >= ship2.numSensors):
                self.ships += [self.runRace(ship1, ship2)]
            else:
                self.ships += [self.runRace(ship2, ship1)]


    def runGeneration(self, printWinner):
        printedWinner = not printWinner
        for i in range(len(self.ships)):
            self.readyShips += [self.ships[0]]
            self.ships.pop(0)
        for n in range(self.runs):
            takenResources = 0
            while (len(self.readyShips) > 1 and takenResources < self.resources):
                i1 = random.randint(0, len(self.readyShips) - 1)
                ship1 = self.readyShips[i1]
                self.readyShips.pop(i1)
                i2 = random.randint(0, len(self.readyShips) - 1)
                ship2 = self.readyShips[i2]
                self.readyShips.pop(i2)
                if (ship1.numSensors >= ship2.numSensors):
                    self.runRace(ship1, ship2)
                else:
                    self.runRace(ship2, ship1)
                takenResources += 1
                self.doneShips += [ship1, ship2]
            for x in range(len(self.doneShips)):
                self.readyShips += [self.doneShips[0]]
                self.doneShips.pop(0)
        for j in range(len(self.readyShips)):
            runsWon = self.readyShips[0].runWins
            self.readyShips[0].runWins = 0
            if (runsWon == 0):
                self.readyShips.pop(0)
            elif (runsWon == 1):
                if (self.readyShips[0].age < self.readyShips[0].maxAge):
                    self.readyShips[0].age += 1
                    self.ships += [self.readyShips[0]]
                self.readyShips.pop(0)
            elif (runsWon == 2):
                if (self.readyShips[0].age < self.readyShips[0].maxAge):
                    self.readyShips[0].age += 1
                    self.ships += [self.readyShips[0]]
                self.ships += [self.readyShips[0].replicate()]
                self.readyShips.pop(0)
            elif (runsWon == 3):
                if (self.readyShips[0].age < self.readyShips[0].maxAge):
                    self.readyShips[0].age += 1
                    self.ships += [self.readyShips[0]]
                self.ships += [self.readyShips[0].replicate()]
                self.ships += [self.readyShips[0].replicate()]
                self.ships += [self.readyShips[0].replicate()]
                self.readyShips.pop(0)
                if (not printedWinner):
                    self.readyShips[0].printShip()
                    printedWinner = True






    def runRace(self, ship1, ship2):
        t = 0
        ship1pos = 0
        ship2pos = 0
        ship1hits = 0
        ship2hits = 0
        ship1.damagedWeapons = 0
        ship1.damagesEngines = 0
        ship2.damagedWeapons = 0
        ship2.damagesEngines = 0
        ship1.updateSpeed()
        ship2.updateSpeed()
        while (t < 1000):
            t += 1

            # Let them move
            ship1pos += ship1.speed
            ship2pos += ship2.speed

            # Let them fight
            if (ship1.numWeapons - ship1.damagedWeapons > 0 and t % (128/ship1.numWeapons) == 0):
                killshot = self.shipAttack(ship1, ship2, ship1hits)
                if (killshot):
                    ship1.runWins += 1
                    return ship1
                ship1hits += 1
            if (ship2.numWeapons - ship2.damagedWeapons > 0 and t % (128/ship2.numWeapons) == 0):
                killshot = self.shipAttack(ship2, ship1, ship2hits)
                if (killshot):
                    ship2.runWins += 1
                    return ship2
                ship2hits += 1

            # Check for destination reached
            if (ship1pos >= 500):
                ship1.runWins += 1
                return ship1
            if (ship2pos >= 500):
                ship2.runWins += 1
                return ship2


    def shipAttack(self, attacker, defender, shiphits):
        shot = False
        for i in range(11):
            i = 10 - i
            for j in range(11):
                if (i - shiphits < 0): return True
                if (defender.structure[i][j - shiphits] != 0):
                    while (not shot):
                        jj = random.randint(0, 10)
                        if (defender.structure[i][jj] != 0):
                            killshot = self.executeExplosion(defender, i, jj, defender.structure[i][jj])
                            if (killshot):
                                return True
                        break
                    if (shot): break
                if (shot): break
            if (shot): break


    def executeExplosion(self, ship1, i, j, explosion):
        if (explosion == 1):
            return True
        if (explosion == 3):
            ship1.damagedEngines += 1
            ship1.updateSpeed()
            return False
        elif (explosion == 4):
            ship1.damagedWeapons += 1
            return False
        elif (explosion == 5 and i != 0 and j != 0 and j != 10):
            return (self.executeExplosion(ship1, i, j-1, explosion)
                    or self.executeExplosion(ship1, i-1, j-1, explosion) or self.executeExplosion(ship1, i+1, j-1, explosion))
        elif (explosion == 6):
            return False





if __name__ == "__main__":
    simulation1 = Simulation()
    simulation1.runMetaSimulation()
