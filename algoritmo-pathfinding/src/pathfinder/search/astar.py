from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


def heuristica(estado_inicial, estado_final):
    a = estado_final[0]-estado_inicial[0]
    b = estado_final[1]-estado_inicial[1]

    return ((a**2)+(b**2))**(1/2)


class AStarSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using A* Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)

        frontier = PriorityQueueFrontier()
        frontier.add(node, node.cost + heuristica(node.state, grid.end))

        # Initialize the explored dictionary to be empty
        explored = {}

        # Add the node to the explored dictionary
        explored[node.state] = node.cost

        while True:

            if frontier.is_empty():
                return NoSolution(explored)

            node = frontier.pop()

            if node.state == grid.end:
                return Solution(node, explored)

            for action, state in grid.get_neighbours(node.state).items():
                s = state
                c = grid.get_cost(s) + node.cost

                if s not in explored or c < explored[s]:
                    new_node = Node("",s,c,node)
                    explored[s] = c
                    frontier.add(new_node, new_node.cost + heuristica(new_node.state, grid.end))






        return NoSolution(explored)