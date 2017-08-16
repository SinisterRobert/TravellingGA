from random import randint, shuffle, choice, random

def generateCities(n, minX, minY, maxX, maxY):
    
    # Generate a list of city tuples (x, y) indicating a location
    
    cities = []
    for i in range(n):
        x = randint(minX, maxX)
        y = randint(minY, maxY)
        cities.append((x,y))
    return cities

def generateTour(cities):
    
    # Generate a tour, or an order in which to visit the cities randomly.
    
    n = len(cities)
    tour = list(range(n))
    shuffle(tour)
    return tour

def generatePop(n, cities):

    # Generates a list of tours
    
    return [generateTour(cities) for i in range(n)]

def mutate(tour):

    # Swaps two random cities in a tour
    
    pos1 = randint(0, len(tour)-1)
    pos2 = randint(0, len(tour)-1)
    while pos1 == pos2:
        pos2 = randint(0, len(tour) - 1)
    tour[pos1], tour[pos2] = tour[pos2], tour[pos1]

def crossover(tour1, tour2):

    # Takes the first half of each tour and uses those to create two new tours
    
    n = len(tour1)//2
    tour3 = tour1[:n]
    tour4 = tour2[:n]
    for i in tour1:
        if i not in tour4:
            tour4.append(i)
    for i in tour2:
        if i not in tour3:
            tour3.append(i)
    return tour3, tour4


def score(cities, tour):
    
    # Traverses the cities in order and finds the total distance.
    
    distance = 0
    for i in range(len(tour) - 1):
        cur = cities[tour[i]]
        next = cities[tour[i+1]]
        distance += ((cur[0] - next[0])**2 + (cur[1] - next[1])**2)**0.5
    next = cities[tour[0]]
    cur = cities[tour[-1]]
    distance += ((cur[0] - next[0])**2 + (cur[1] - next[1])**2)**0.5
    return distance

def avgScore(scored):

    # Find the average score of a population.
    
    total = 0
    for i in scored:
        total += i[1]
    total /= len(scored)
    return total

def main():
    # Initialize cities and starting population of tours.
    inFile = open("scores.txt", "w")
    nCandidates = 1000
    mutateChance = 0.015
    parentPercent = 0.2 # Take the top 20% of candidates to breed.

    cities = generateCities(100, -100, -100, 100, 100)
    pop = generatePop(nCandidates, cities)
    
    # "Evolve" the population for 1000 generations
    for i in range(1000):
        print(i)
        
        # Score the candidates
        scored = [(tour, score(cities,tour)) for tour in pop] 
        scored = sorted(scored, key = lambda x : x[1])
        
        # Take 20% of the best candidates for parents of next generation
        parents = [x[0] for x in scored[:int(parentPercent*len(scored))]] 
        newGen = parents[:]
        inFile.write(str(avgScore(scored)) + "," + str(scored[-1][1]) + "," + \
        str(scored[0][1]) + "\n")
        
        
        while len(newGen) < nCandidates:
        
            # Randomly choose parents and breed them
            parent1 = randint(0, len(parents)-1)
            parent2 = randint(0, len(parents)-1)
            while parent1 == parent2:
                parent2 = randint(0, len(parents)-1)
            parent1 = parents[parent1]
            parent2 = parents[parent2]
            child1, child2 = crossover(parent1, parent2)
            newGen.append(child1)
            newGen.append(child2)
        
        # Randomly mutate some of the new population.
        for c in newGen:
            rMut = random()
            if rMut < mutateChance:
                mutate(c)
        pop = newGen[:]
    inFile.close()
main()