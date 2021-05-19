from queue import PriorityQueue

from variables import *


class Search:
    def __init__(self, istate, goal, borders, houses, holes):
        self.istate = istate
        self.goal = goal
        self.borders = borders
        self.houses = houses
        self.holes = holes
        self.end_cost = None

    def search_a_star(self):  # A*
        start_node = Node(self.istate)

        if self.goal_test(start_node.state):
            return []

        fringe = PriorityQueue()
        fringe.put((0, start_node))

        action_list = []
        explored = []

        while fringe.qsize() > 0:  # if fringe is not empty
            current_node = fringe.get()[1]  # picking element from fringe
            explored.append(current_node.state)  # adding node where we currently are to visited ones

            if self.goal_test(current_node.state):
                self.end_cost = current_node.cost  # remembering found best route cost

                while current_node.parent is not None:
                    action_list.append(current_node.action)
                    current_node = current_node.parent

                action_list.reverse()

                return action_list

            for successor in self.successors(current_node.state):
                successor.parent = current_node
                power = self.heuristic(successor, self.goal[0])
                successor.cost = power

                if self.no_node_in_list_for_queue(successor, fringe) and self.no_state_in_list(successor.state, explored):
                    fringe.put((power, successor))

                elif not self.no_node_in_list_for_queue(successor, fringe):  # if node is present in fringe
                    return_node, index = self.node_list_state_test_values(successor, fringe)

                    if return_node[0] > power:  # better way to node - change
                        temp_queue = PriorityQueue()

                        for i in range(index):
                            temp_queue.put(fringe.get())

                        fringe.put((power, successor))

                        for j in range(index - 1):
                            fringe.put(temp_queue.get())

    def search_BFS(self):
        start_node = Node(self.istate)

        if self.goal_test(start_node.state):
            return []

        fringe = [start_node]
        action_list = []
        explored = []

        while fringe:
            current_node = fringe.pop(0)
            explored.append(current_node.state)

            if self.goal_test(current_node.state):
                while current_node.parent is not None:
                    action_list.append(current_node.action)
                    current_node = current_node.parent

                action_list.reverse()

                return action_list

            for successor in self.successors(current_node.state):
                if self.no_node_in_list(successor, fringe) and self.no_state_in_list(successor.state, explored):
                    successor.parent = current_node
                    fringe.append(successor)

    def goal_test(self, state):  # if state is in the states list = goal achieved
        if not self.no_state_in_list(state, self.goal):
            return True

        return False

    @staticmethod
    def no_node_in_list(node_to_check, test_node_list):
        for node in test_node_list:
            if node.state.x == node_to_check.state.x and node.state.y == node_to_check.state.y and node.state.rotation == node_to_check.state.rotation:
                return False

        return True

    @staticmethod
    def no_node_in_list_for_queue(node_to_check, test_node_list):
        for node in test_node_list.queue:
            if node[1].state.x == node_to_check.state.x and node[1].state.y == node_to_check.state.y and node[1].state.rotation == node_to_check.state.rotation:
                return False

        return True

    @staticmethod
    def no_state_in_list(state_to_check, state_list):
        for state in state_list:
            if state.x == state_to_check.x and state.y == state_to_check.y and state.rotation == state_to_check.rotation:
                return False

        return True

    @staticmethod
    def node_list_state_test_values(test_node, test_node_list):
        i = 0

        for node in test_node_list.queue:
            i += 1

            if node[1].state.x == test_node.state.x and node[1].state.y == test_node.state.y and node[1].state.rotation == test_node.state.rotation:
                return node, i

    def successors(self, state):
        successor_list = []

        if state.rotation == 0:
            if self.no_collision(state):
                successor_list.append(Node(State(state.x + 1, state.y, 0), "forward"))

            successor_list.append(Node(State(state.x, state.y, 3), "rotate_left"))
            successor_list.append(Node(State(state.x, state.y, 1), "rotate_right"))

        elif state.rotation == 1:
            if self.no_collision(state):
                successor_list.append(Node(State(state.x, state.y + 1, 1), "forward"))

            successor_list.append(Node(State(state.x, state.y, 0), "rotate_left"))
            successor_list.append(Node(State(state.x, state.y, 2), "rotate_right"))

        elif state.rotation == 2:
            if self.no_collision(state):
                successor_list.append(Node(State(state.x - 1, state.y, 2), "forward"))

            successor_list.append(Node(State(state.x, state.y, 1), "rotate_left"))
            successor_list.append(Node(State(state.x, state.y, 3), "rotate_right"))

        elif state.rotation == 3:
            if self.no_collision(state):
                successor_list.append(Node(State(state.x, state.y - 1, 3), "forward"))

            successor_list.append(Node(State(state.x, state.y, 2), "rotate_left"))
            successor_list.append(Node(State(state.x, state.y, 0), "rotate_right"))

        return successor_list

    def no_collision(self, state):
        dx = 0
        dy = 0

        if state.rotation == 0:
            dx = 1
        elif state.rotation == 1:
            dy = 1
        elif state.rotation == 2:
            dx = -1
        elif state.rotation == 3:
            dy = -1

        for border in self.borders:
            if border.x == state.x + dx and border.y == state.y + dy:
                return False

        for house in self.houses:
            if house.x == state.x + dx and house.y == state.y + dy:
                return False

        return True

    def heuristic(self, a, b):
        distance_manhattan = abs(a.state.x - b.x) + abs(a.state.y - b.y)

        if a.parent is not None:
            a.cost += a.parent.cost

            for hole in self.holes:
                if hole.x == a.state.x and hole.y == a.state.y:
                    a.cost += HOLE_COST

        return a.cost + distance_manhattan


class Node:
    def __init__(self, state, action=None, parent=None, cost=1):
        self.state = state
        self.action = action
        self.parent = parent
        self.cost = cost

    def __lt__(self, other):  # in case of equal priority
        return self.state.x < other.state.y and self.state.y < other.state.y


class State:
    def __init__(self, x, y, rotation, cost=REGULAR_COST):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.cost = cost
