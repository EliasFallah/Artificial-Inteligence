cities = [
    'Arad', 'Bucharest', 'Craiova', 'Drobeta', 'Eforie', 'Fagaras',
    'Giurgiu', 'Hirsova', 'Iasi', 'Lugoj', 'Mehadia', 'Neamt',
    'Oradea', 'Pitesti', 'Rimnicu Vilcea', 'Sibiu', 'Timisoara',
    'Urziceni', 'Vaslui', 'Zerind'
]

romania_matrix = [
# Arad     Buc     Craiova Drob    Eforie Fagar  Giurgiu Hirso  Iasi   Lugoj  Meha   Neamt  Orad   Pit    R.Vil  Sibiu  Timi   Urzi   Vasl   Zerind
 [   0,     0,      0,      0,      0,     0,    0,      0,     0,       0,     0,     0,     0,     0,     0,     140,   118,    0,     0,     75],  # Arad
 [   0,     0,      0,      0,      0,     211,   90,     0,     0,      0,     0,     0,     0,    101,    0,      0,     0,     85,    0,      0],  # Bucharest
 [   0,     0,      0,     120,     0,     0,     0,      0,     0,      0,     0,     0,     0,    138,   146,     0,     0,     0,     0,      0],  # Craiova
 [   0,     0,     120,     0,      0,     0,     0,      0,     0,      0,    75,     0,     0,     0,     0,      0,     0,     0,     0,      0],  # Drobeta
 [   0,     0,      0,      0,      0,     0,     0,     86,     0,      0,     0,     0,     0,     0,     0,      0,     0,     0,     0,      0],  # Eforie
 [   0,    211,     0,      0,      0,     0,     0,      0,     0,      0,     0,     0,     0,     0,     0,     99,     0,     0,     0,      0],  # Fagaras
 [   0,    90,      0,      0,      0,     0,     0,      0,     0,      0,     0,     0,     0,     0,     0,      0,     0,     0,     0,      0],  # Giurgiu
 [   0,     0,      0,      0,     86,     0,     0,      0,     0,      0,     0,     0,     0,     0,     0,      0,     0,    98,     0,      0],  # Hirsova
 [   0,     0,      0,      0,      0,     0,     0,      0,     0,      0,     0,    87,     0,     0,     0,      0,     0,     0,    92,      0],  # Iasi
 [   0,     0,      0,      0,      0,     0,     0,      0,     0,      0,    70,     0,     0,     0,     0,      0,   111,     0,     0,      0],  # Lugoj
 [   0,     0,      0,     75,      0,     0,     0,      0,     0,     70,     0,     0,     0,     0,     0,      0,     0,     0,     0,      0],  # Mehadia
 [   0,     0,      0,      0,      0,     0,     0,      0,    87,      0,     0,     0,     0,     0,     0,      0,     0,     0,     0,      0],  # Neamt
 [   0,     0,      0,      0,      0,     0,     0,      0,     0,      0,     0,     0,     0,     0,     0,     151,    0,     0,     0,     71],  # Oradea
 [   0,    101,   138,      0,      0,     0,     0,      0,     0,      0,     0,     0,     0,     0,    97,      0,     0,     0,     0,      0],  # Pitesti
 [   0,     0,    146,      0,      0,     0,     0,      0,     0,      0,     0,     0,     0,    97,     0,     80,     0,     0,     0,      0],  # Rimnicu Vilcea
 [ 140,     0,      0,      0,      0,    99,     0,      0,     0,      0,     0,     0,   151,     0,    80,      0,     0,     0,     0,      0],  # Sibiu
 [ 118,     0,      0,      0,      0,     0,     0,      0,     0,    111,     0,     0,     0,     0,     0,      0,     0,     0,     0,      0],  # Timisoara
 [   0,    85,      0,      0,      0,     0,     0,     98,     0,      0,     0,     0,     0,     0,     0,      0,     0,     0,   142,      0],  # Urziceni
 [   0,     0,      0,      0,      0,     0,     0,      0,    92,      0,     0,     0,     0,     0,     0,      0,     0,   142,     0,      0],  # Vaslui
 [  75,     0,      0,      0,      0,     0,     0,      0,     0,      0,     0,     0,    71,     0,     0,      0,     0,     0,     0,      0]   # Zerind
]

from collections import deque


def bfs(matrix, cities, start, goal):
    start = cities.index(start)
    goal = cities.index(goal)
    visited = set()
    queue = deque([(start, [cities[start]])])

    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path

        visited.add(current)

        for neighbor in range(len(matrix[current])):
            if matrix[current][neighbor] > 0 and neighbor not in visited:
                queue.append((neighbor, path + [cities[neighbor]]))

    return None

#get user input for start and goal cities
startCity = input("Enter start city: ")
while startCity not in cities:
    print("Invalid city. Please try again.")
    startCity = input("Enter start city: ")

goalCity = input("Enter goal city: ")
while goalCity not in cities:
    print("Invalid city. Please try again.")
    goalCity = input("Enter goal city: ")

# Find the path using BFS
path = bfs(romania_matrix, cities, startCity, goalCity)

# Print the path if found
if path:
    for city in path:
        print(city, end=" -> ")
    print("Goal Reached!")
else:
    print("No path found.")