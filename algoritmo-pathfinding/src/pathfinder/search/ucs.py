from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Uniform Cost Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)

        # Initialize the explored dictionary to be empty
        explored = {}

        # Add the node to the explored dictionary
        explored[node.state] = node.cost

        frontier = PriorityQueueFrontier()
        frontier.add(node, node.cost)

        while True:

            if frontier.is_empty():
                return NoSolution(explored)

            node = frontier.pop()

            if node.state == grid.end:
                return Solution(node, explored)

            for action, state in grid.get_neighbours(node.state).items():
                s = state
                c = node.cost + grid.get_cost(s)

                if s not in explored or c < explored[s]:
                    n = Node("",s, c, node)
                    explored[s] = c
                    frontier.add(n, n.cost)

        return NoSolution(explored)
