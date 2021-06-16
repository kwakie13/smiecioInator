import copy
import random

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import Classes.Searching as Searching


class GeneticAlgorithm:
    def __init__(self, game):
        self.game = game
        self.trash_list = self.split_trash()
        self.best_route_np = None
        self.run()
        self.best_route = self.best_route_np.tolist()

    def get_distance(self, starting_object, ending_object):
        goal = [Searching.State(ending_object.x, ending_object.y, 0),
                Searching.State(ending_object.x, ending_object.y, 1),
                Searching.State(ending_object.x, ending_object.y, 2),
                Searching.State(ending_object.x, ending_object.y, 3)]
        istate = Searching.State(starting_object.x, starting_object.y, 0)
        search_obj = Searching.Search(istate, goal, self.game.borders, self.game.houses, self.game.holes)
        move_list = search_obj.search_a_star()

        return search_obj.end_cost

    def split_trash(self):
        trash_list = []
        for trash in self.game.trashes:
            trash_list.append(trash)

        return trash_list

    def initialize_map(self, n):
        the_map = np.zeros((n, n))

        for i in range(0, n):
            for j in range(0, i + 1):
                if i == j:
                    the_map[i][j] = 0
                else:
                    the_map[i][j] = self.get_distance(self.trash_list[i], self.trash_list[j])
                    the_map[j][i] = the_map[i][j]

        # sns.heatmap(the_map)
        # plt.show()

        return the_map

    def score_population(self, population, the_map):
        scores = []

        for element in population:
            scores += [self.fitness(element, the_map)]

        return scores

    def fitness(self, route, the_map):
        score = 0

        for i in range(1, len(route)):
            score += the_map[route[i - 1]][route[i]]

        return score

    def plot_best(self, the_map, route, iteration_number):
        sns.heatmap(the_map)

        x = [0.5] + [x + 0.5 for x in route[0: len(route) - 1]] + [len(the_map) - 0.5]
        y = [0.5] + [x + 0.5 for x in route[1: len(route)]] + [len(the_map) - 0.5]

        plt.plot(x, y, marker="o", linewidth=3, markersize=10, linestyle="-", color="yellow")
        plt.savefig("./Assets/new1000plot_%i.png" % iteration_number, dpi=300)
        plt.show()

    def run(self):
        population_size = 100
        number_of_iterations = 300
        number_of_couples = 10
        number_of_winners_to_keep = 2
        mutation_probability = 0.05

        the_map = self.initialize_map(len(self.trash_list))
        population = self.create_starting_population(population_size)

        last_distance = 1000000000

        for i in range(0, number_of_iterations):
            new_population = []

            scores = self.score_population(population, the_map)  # score of each element (fitness)
            best = population[np.argmin(scores)]  # best element = least cost
            self.best_route_np = best
            number_of_moves = len(best)
            distance = self.fitness(best, the_map)

            if distance != last_distance:  # check if best is new best
                print("Iteration %i: Best so far is %i steps for a distance of %f" % (i, number_of_moves, distance))
                self.plot_best(the_map, best, i)

            for j in range(0, number_of_couples):  # start creating new population by crossing over
                pick_1 = self.pick_mate(scores)
                pick_2 = self.pick_mate(scores)
                new_1, new_2 = self.crossover(population[pick_1], population[pick_2]), self.crossover(
                    population[pick_2], population[pick_1])
                new_population = new_population + [new_1, new_2]

            for j in range(0, len(new_population)):  # mutate members of new population
                new_population[j] = np.copy(self.mutate(new_population[j], mutation_probability))

            new_population += [population[np.argmin(scores)]]  # keep members of previous generation
            for j in range(1, number_of_winners_to_keep):
                keeper = self.pick_mate(scores)
                new_population += [population[keeper]]

            while len(new_population) < population_size:  # add new random members
                new_population += [self.create_new_member()]

            population = copy.deepcopy(new_population)  # replace the old population

            last_distance = distance  # last best to keep

    def pick_mate(self, scores):  # pick two high scorers
        array = np.array(scores)
        temp = array.argsort()  # sorted indexes
        ranks = np.empty_like(temp)  # same array as temp
        ranks[temp] = np.arange(len(array))

        fitness = [len(ranks) - x for x in ranks]
        local_scores = copy.deepcopy(fitness)

        for i in range(1, len(local_scores)):
            local_scores[i] = fitness[i] + local_scores[i - 1]

        probabilities = [x / local_scores[-1] for x in local_scores]

        rand = random.random()

        for i in range(0, len(probabilities)):  # if score is higher -> more likely to cross
            if rand < probabilities[i]:
                return i

    def crossover(self, array1, array2):
        list_1 = array1.tolist()
        list_2 = array2.tolist()
        point = random.randint(1, 8)

        temp_list = []

        i = 0

        for element in list_1:
            if i <= point:
                temp_list.append(element)
                i += 1
            else:
                break

        for element in temp_list:
            list_2.remove(element)

        for element in list_2:
            temp_list.append(element)

        return np.array(temp_list)

    def mutate(self, route, probability):
        new_route = copy.deepcopy(route)

        index_1 = random.randint(1, 8)
        index_2 = random.randint(1, 8)

        while index_1 == index_2:
            index_1 = random.randint(1, 8)
            index_2 = random.randint(1, 8)

        if random.random() > probability:
            new_route[index_1], new_route[index_2] = new_route[index_2], new_route[index_1]

        return new_route

    @staticmethod
    def create_new_member():
        route = np.zeros(1, dtype=int)  # starting array type = int, 1 dimension, 1 element
        i = 1

        possibilities = np.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=int)

        while len(possibilities) > 0:
            proposed_value = random.randint(0, len(possibilities) - 1)
            route = np.append(route, possibilities[proposed_value])
            possibilities = np.delete(possibilities, proposed_value)

            i += 1

        route = np.append(route, 9)
        return route

    def create_starting_population(self, size):
        population = list()

        for i in range(0, size):
            population.append(self.create_new_member())

        return population
