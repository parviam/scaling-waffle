#parv mahajan: implementation of genetic algorithms to knapsack
#UNFINISHED

import random
import math

#the items that go in the knapsack

numberOfItems = 5000

class Item:
    def __init__(self):
        self.size = math.floor(random.random() * 20) + 1 #b/w (1, 20)
        self.value = math.floor(random.random() * 50) + 1 #b/w (1, 50)
    def toString(self):
        return ("Size ", self.size, " Value ", self.value)

items = [Item()]*numberOfItems #list of items

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
    for x in child.bits:
        if x == True:
            totalSize += items[x].size
            totalValue += items[x].value
    if totalSize > 100000:      #number is abritrary here
        return 0
    #return value if not disqualified
    return totalValue

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
                newFitness.append(oldGen.fit[x])
                break
    return Generation(len(oldGen.gen), 0, newMembers, newFitness)

#conducts mutation on a generation according to a set chance
def mutation(aGen, per):
        for x in aGen.gen:
                for y in x.bits:
                        rand = random.random()
                        if rand < per:
                                x.bits[y] = not x.bits[y]
        return aGen

def crossover(aGen, per, l):
        newGen = Generation(len(aGen.gen), 0, aGen.gen, aGen.fit)
        for x in range(len(aGen.gen)):
                rand = random.random()
                if per > rand:
                        randA = random.randint(0, numberOfItems - l - 1)
                        temp = aGen.gen[x].bits[randA:randA + l]
                        randB = random.randint(0, numberOfItems - l - 1)
                        aGen.gen[x].bits[randA:randA + l] = newGen.gen[x].bits[randB:randB + l]
                        newGen.gen[x].bits[randB:randB + l] = temp
        return newGen

#runs the genetic algortithm for a number of generations
def evolve(generations):
        g = Generation(500, 1, [], [])
        for x in range(generations):
                g = newGen(g)
                g = crossover(g, 0.5, 5)
                g = mutation(g, 0.05)
                print(g.avgFitness())
                
evolve(1000)                
        


    
        


        
        
