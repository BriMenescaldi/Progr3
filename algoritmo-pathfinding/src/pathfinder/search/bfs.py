from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Breadth First Search

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
        explored[node.state] = True

        # Verify is the current state is a solution
        if node.state == grid.end:
            return Solution(node, explored)

        # Create a frontier
        frontier = QueueFrontier()
        frontier.add(node)

        # Start the loop
        while True:
            if frontier.is_empty():
                return NoSolution(explored)
            node = frontier.remove()

            successors = grid.get_neighbours(node.state)

            for succesor in successors:
                successors[succesor]

                new_state = successors[succesor]

                if new_state not in explored:
                    new_node = Node("", new_state, node.cost + grid.get_cost(new_state), parent = node, action=successors[succesor])
                    frontier.add(new_node)
                    explored[new_node.state] = True

                    if new_state == grid.end:
                        return Solution(new_node, explored)

        return NoSolution(explored)
