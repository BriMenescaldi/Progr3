from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node

class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Depth First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)

        # Initialize the explored dictionary to be empty
        explored = {}

        #Test objetivo
        if node.state == grid.end:
            return Solution(node, explored)

        # Add the node to the explored dictionary
        explored[node.state] = True

        # Create a frontier
        frontier = StackFrontier()
        frontier.add(node)

        while True:

            if frontier.is_empty():
                return NoSolution(explored)

            n = frontier.remove()

            if n.state in explored == True:
                continue

            explored[n.state] = True

            for accion, state in grid.get_neighbours(n.state).items():

                s = state
                n2 = Node("", state, n.cost + grid.get_cost(s),parent = n)

                if n2.state not in explored:

                    if n2.state == grid.end:
                        return Solution(n2, explored)

                    frontier.add(n2)



        return NoSolution(explored)