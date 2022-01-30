#parv mahajan: implementation of genetic algorithms to knapsack problem
#v1 1/30/2022

import random
import math

#inputs
numberOfItems = 100
crossoverRate = 0.5
mutationRate = 0.5
numberOfGenerations = 1000
membersPerGeneration = 500
rucksackLength = 100
rucksackWidth = 75
rucksackDepth = 30


class Item:
    def __init__(self):
        random.seed()
        self.size = math.floor(random.random() * 50) + 1 #b/w [1, 50)
        random.seed(self.size)
        self.value = math.floor(random.random() * 500) + 1 #b/w [1, 50)
        random.seed(self.value)
        self.robustness = random.random() + 1 #b/w [1, 2)
        random.seed(self.robustness)
        self.length = random.random()*10 #b/w [0, 10)
        random.seed(self.length)
        self.width = random.random()*10 #b/w [0, 10)
        random.seed(self.width)
        self.depth = random.random()*10 #b/w [0, 10)
        random.seed()
        self.fighting = random.randint(0, 50)/self.value
    def toString(self):
        return ("Size ", self.size, " Value ", self.value, "Robustness", self.robustness, "Length", self.length, "Width", self.width, "Depth", self.depth, "Fighting", self.fighting)

items = [] #list of items
for x in range(numberOfItems):
    items.append(Item())

#each member of a generation ==> just a list
class Member:
    def __init__(self):
        self.bits = [True]*numberOfItems
        randDoubles = []
        for x in range(numberOfItems):
            randDoubles.append(random.random())
        for i in range(numberOfItems):
            if randDoubles[i] < 0.5:
                self.bits[i] = False

#fitness function for a Member, named child
def fitness(child):
    #check size
    totalSize = 0
    totalValue = 0
    totalLength = 0
    totalDepth = 0
    totalWidth = 0
    time = 0
    totalFighting = 0
    for x in child.bits:
        if x == True:
            if items[x].robustness > 1.5:
                totalFighting += items[x].fighting
                if totalWidth < rucksackWidth and totalLength < rucksackLength and totalDepth < rucksackDepth:
                    totalLength += items[x].length
                    totalWidth += items[x].width
                    totalDepth += items[x].depth
                    totalSize += items[x].size
                    totalValue += items[x].value
                else:
                    time += math.floor((items[x].length*items[x].depth*items[x].width)/items[x].value)
            else:
                totalValue -= items[x].value
            
    if totalSize > 50*numberOfItems/4:      #number 4 is abritrary here
        return 0
    if totalFighting > 1:
        totalValue += 100*totalFighting
    #return value if not disqualified
    return max(0, math.floor(totalValue - time))

#holds one generation, does tournament, crossover, etc.
class Generation:
    def __init__(self, num, i, gen, fit):
        if(i == 1):   #for the first generation
            self.gen = [] #holds the Members
            self.fit = [] #holds fitness for each Member
            for x in range(num):                                
                self.gen.append(Member())
                self.fit.append(fitness(self.gen[x]))
        else:   #for subsequent generations
            self.gen = gen
            self.fit = fit
    def avgFitness(self): #returns avg fitness
        total = 0
        for x in range(len(self.fit)):
            total += self.fit[x]
        return total/len(self.gen)
    def highestFitness(self):   #returns the highest fitness in the generation
        maximum = 0
        for x in self.fit:
            if maximum < x:
                maximum = x
        return maximum
    def totalFitness(self):     #returns the sum of all the fitnesses
        total = 0
        for f in self.fit:
            total += f
        return total

#creates a new generation from a previous one using weighted roulette wheel
def newGen(oldGen):
    newMembers = []
    newFitness = []
    for i in range(len(oldGen.gen)):
        total = oldGen.totalFitness()
        rand = random.randint(0, total)
        for x in range(len(oldGen.gen)):
            rand -= oldGen.fit[x]
            if rand <= 0:
                newMembers.append(oldGen.gen[x])
                newFitness.append(fitness(oldGen.gen[x]))
                break
    return Generation(len(oldGen.gen), 0, newMembers, newFitness)

#conducts mutation on a generation according to a set chance
def mutation(aGen, per):
        mutations = 0
        for x in range(len(aGen.gen)):
                rand = random.random()
                for y in aGen.gen[x].bits:
                        if rand < per:
                                aGen.gen[x].bits[y] = not aGen.gen[x].bits[y]
                                mutations += 1
                aGen.fit[x] = fitness(aGen.gen[x])
        return aGen

#crossover on a generation according to a set chance, of l length
def crossover(aGen, per, le):
        newGen = Generation(len(aGen.gen), 0, aGen.gen, aGen.fit)
        for x in range(len(aGen.gen)):
                rand = random.random()
                if per > rand:
                        randA = random.randint(0, numberOfItems - 1 - le)
                        temp = newGen.gen[x].bits[randA: randA + le]
                        randB = random.randint(0, numberOfItems - 1 - le)
                        newGen.gen[x].bits[randA:randA + le] = newGen.gen[x-1].bits[randB:randB + le]
                        newGen.gen[x-1].bits[randB:randB + le] = temp
                aGen.fit[x] = fitness(aGen.gen[x]
                                      )
        return newGen

#runs the genetic algortithm for a number of generations
def evolve(generations, m):
        g = Generation(m, 1, [], [])
        print("Avg value: $", g.avgFitness(), "Highest Value: $", g.highestFitness())
        fitnesses = []
        for x in range(generations):
                g = newGen(g) #roullete wheel
                g = crossover(g, crossoverRate, math.floor(numberOfItems/2)) #crossover with a random length upto 50% of the total length
                g = mutation(g, mutationRate) #mutation
                uncertainty = 1
                if g.avgFitness() > 0:
                    uncertainty = (g.highestFitness()-g.avgFitness())/g.avgFitness()
                print("Avg value: $", g.avgFitness(), "Uncertainty: ", uncertainty, "Highest Value: $", g.highestFitness())
                fitnesses.append(g.avgFitness())
                if uncertainty < 0.00001 and x > 100:
                                 break
        print(g.highestFitness())

evolve(numberOfGenerations, membersPerGeneration)

        


    
        


        
        
