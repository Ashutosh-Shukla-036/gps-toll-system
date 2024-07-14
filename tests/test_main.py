import unittest
from main import dijkstra, calculate_toll, create_graph

class TestDijkstra(unittest.TestCase):
    def test_dijkstra(self):
        # Create the graph
        G = create_graph()

        # Define the expected paths and cost based on the graph structure
        expected_paths = [
            ['Mumbai', 'Bangalore', 'Chennai', 'Kanpur', 'Nagpur', 'Bhopal'],
            ['Mumbai', 'Delhi', 'Chennai', 'Kanpur', 'Nagpur', 'Bhopal'],
            ['Mumbai', 'Ahmedabad', 'Chennai', 'Kolkata', 'Pune', 'Bhopal']
        ]
        expected_cost = 17  # Adjusted based on your graph weights

        # Run Dijkstra's algorithm
        path, cost = dijkstra(G, 'Mumbai', 'Bhopal')

        # Assert the cost
        self.assertEqual(cost, expected_cost, f"Expected cost: {expected_cost}, but got: {cost}")

        # Assert the path is one of the expected paths
        self.assertIn(path, expected_paths, f"Expected path to be one of {expected_paths}, but got: {path}")

        # Calculate toll and assert the expected toll
        toll = calculate_toll(path, G)
        expected_toll = expected_cost * 0.5  # Assuming toll rate per km is 0.5
        self.assertEqual(toll, expected_toll, f"Expected toll: {expected_toll}, but got: {toll}")

if __name__ == '__main__':
    unittest.main()
