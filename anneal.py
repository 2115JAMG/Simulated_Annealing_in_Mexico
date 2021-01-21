from math import sin, cos, sqrt, atan2, exp
import gpxpy.geo
import random
import visualize
import matplotlib.pyplot as plt


class SimAnneal(object):
    def __init__(self, coords, T=-1, alpha=-1, stopping_T=-1, stopping_iter=-1):
        self.coords = coords
        self.N = len(coords)
        self.T = 5000
        self.alpha = 0.999
        self.stopping_temperature = 0.001
        self.stopping_iter = 20000 
        self.iteration = 1
        self.nodes = [i for i in range(self.N)]
        self.best_solution = None
        self.best_fitness = float("Inf") 
        self.flag,self.cont = 0,0
        self.list_outP, self.rute,self.travel,self.fitness_list = [],[],[],[]

    def initial_solution(self): 
        """
        Initial solution, random.
        """
        cur_node = random.choice(self.nodes)  # start from a random node
        solution = [cur_node]

        free_nodes = set(self.nodes) # free nodes
        free_nodes.remove(cur_node) # remove the choice node 
        # while for free nodes
        while free_nodes:
            next_node = min(free_nodes, key=lambda x: self.dist(cur_node, x))# nearest neighbour
            free_nodes.remove(next_node)
            solution.append(next_node) #add the nearest neighbour 
            cur_node = next_node #update

        cur_fit = self.fitness(solution)
        
        if cur_fit < self.best_fitness:  # If best found so far, update best fitness
            self.best_fitness = cur_fit
            self.best_solution = solution
        self.fitness_list.append(cur_fit)
        
        visualize.plotTSP([self.best_solution], self.coords, self.flag)
        
        return solution, cur_fit

    def dist(self, node_0, node_1):
        """
        Distance of Heaviside, 
        the curvature of the earth is contemplated, latitudes and longitudes of 
        two points are occupied, this implemented with a library. 
        """
        self.cont = self.cont + 1
        coord_0, coord_1 = self.coords[node_0], self.coords[node_1]
        distance = gpxpy.geo.haversine_distance(coord_0[1], coord_0[2], coord_1[1], coord_1[2])
        return distance
        
    def fitness(self, solution):
        """
        Total distance of the algorithm
        """
        cur_fit = 0
        for i in range(self.N): 
            cur_fit += self.dist(solution[i % self.N], solution[(i + 1) % self.N])
        return cur_fit

    def p_accept(self, candidate_fitness):
        """
        Probability of accepting if the candidate is worse than current.
        Depends on the current temperature and difference between candidate 
        and current.
        """
        out = exp(-1*(candidate_fitness - self.cur_fitness) / self.T)
        self.list_outP.append(out)
        return out
    

    def accept(self, candidate):
        """
        Accept with probability 1 if candidate is better than current.
        Accept with probabilty p_accept(..) if candidate is worse.
        """
        candidate_fitness = self.fitness(candidate)
        if candidate_fitness < self.cur_fitness:
            self.cur_fitness, self.cur_solution = candidate_fitness, candidate
            if candidate_fitness < self.best_fitness:
                self.best_fitness, self.best_solution = candidate_fitness, candidate
        else:
            if random.random() < self.p_accept(candidate_fitness):
                self.cur_fitness, self.cur_solution = candidate_fitness, candidate
        
    def anneal(self):
        """
        Execute simulated annealing algorithm.
        """
        # Initialize with the greedy solution.
        self.cur_solution, self.cur_fitness = self.initial_solution()
        self.list_T = []
        rep = 0
        print('\n=====================================\n')
        print("Starting Simulated Annealing.") #while de recocido simulado
        print('\n=====================================\n')
        while self.T >= self.stopping_temperature and self.iteration < self.stopping_iter:
            rep = rep + 1
            candidate = list(self.cur_solution)
            l = random.randint(2, self.N - 1)
            i = random.randint(0, self.N - l)
            candidate[i : (i + l)] = reversed(candidate[i : (i + l)])
            self.accept(candidate)
            self.T *= self.alpha
            self.list_T.append(self.T)
            self.iteration += 1
            self.out = 0
            self.fitness_list.append(self.cur_fitness)

        plt.plot(range(rep),self.list_T)
        plt.ylabel("Temperature")
        plt.xlabel("Iteration")
        plt.show()
        
        print('\n=====================================\n')
        print("Best fitness obtained: %0.2f " %(self.best_fitness/1000), ' Km')
        print('The final temperature is: %0.3f  ' %(self.T) )
        print('\n=====================================\n')       
        
    def visualize_routes(self):
        """
        Visualize the rute of S.A. and the first solution (random) 
        """
        self.flag = self.flag + 1
        visualize.plotTSP([self.best_solution], self.coords, self.flag)

    def visualize_routes2(self):
        """
        Visualize the rute of Brute Force
        """
        self.flag = self.flag + 1
        visualize.plotTSP([list(self.rute)], self.coords, self.flag)

    def plot_learning(self):
        """
        Plot the fitness or cost through iterations.
        """
        plt.plot([i for i in range(len(self.fitness_list))], self.fitness_list)
        plt.ylabel("Distance")
        plt.xlabel("Iteration")
        plt.show()
        
    def brute_force(self, n, Republica):
        """
        All the Brute Force algorithm, for the comparative with S.A.
        only if N > 2 and N<10
        """
        print('\nStart de brute force algorithm...')
        print('\nWith brute force algorithm the output is:\n')
        from itertools import permutations 
        l = list(permutations(self.travel))
        total_distance, grax = [], []
        add, limit, self.cont, cont2, index  = 0, 0, 0, 0, 0
        for way in l:
            for capital in range(len(way)):
                if limit >= int(n)-1:
                    total_distance.append(add)
                    grax.append(self.cont)
                    cont2 = cont2 + self.cont
                    add, limit = 0, 0
                    break
                add = add + self.dist(way[capital], way[capital + 1])
                limit = limit + 1
        bestFB = min(total_distance)
        print('\nThe best travel have the longitude of: ',bestFB/1000,' Km',
              '\nWith: ',cont2, 'iterations versus ', self.iteration,
              'iterations de SA algorithm')
        for order in total_distance:
            if order == bestFB:
                self.rute = l[index]
                break
            index = index + 1
        print('The travel is: \n')
        for i in self.rute:
            print(Republica['Nombre'][i],', ',Republica['Estados'][i])
        plt.plot(grax)
        plt.ylabel("Comparision")
        plt.xlabel("Calls")
        plt.show()
        print('\n=====================================\n') 
        
    def list_of_capitals(self, n, Republica):
        """
        Plot the N-capitals in the list of the best_solution
        """
        self.travel = self.best_solution[0:int(n)]
        print('\n=====================================\n')
        print('\nThe begin of the travel is the next: \n')
        for i in self.travel:
            print(Republica['Nombre'][i],', ',Republica['Estados'][i])
        print('...\nAnd the last capital is...\n')
        print(Republica['Nombre'][self.best_solution[31]],', ', 
              Republica['Estados'][self.best_solution[31]])
        print('\n=====================================\n')
        

        
        
        
                
            
            
        