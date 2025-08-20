# virtual-train-route-planner

Virtual Train Route Planner

A Python program that simulates a virtual train route planner with support for:

Linear routes (using doubly linked lists)

Loop routes (using circular linked lists)

Real-time negative stations (stations that are temporarily unavailable and must be avoided)

 Features

Doubly Linked List for Linear Routes
Allows forward and backward navigation between stations.

Circular Linked List for Loop Routes
Supports circular/loop lines where the last station connects back to the first.

Real-Time Station Availability
Stations can be marked as negative (unavailable) at runtime, and the planner will automatically avoid them.

Shortest Path on Circular Routes
Chooses the shortest valid path (clockwise or counter-clockwise) on loop routes.

Dynamic Route Updates
Add or remove stations during runtime.

 How It Runs

Clone or download the repository.

Run the script with Python 3:

python virtual_train_route_planner.py


The demo will:

Create a linear line (Red Line) and a circular line (Loop Line)

Plan routes between stations

Mark stations as negative and re-plan paths

Show dynamic station edits in action

 Sample Output

When you run the script, you will see something like this:

Linear A2->A5: ['A2', 'A3', 'A4', 'A5']
A2->A5 with A4 NEG: None
A2->A5 restored: ['A2', 'A3', 'A4', 'A5']
Circular C6->C3: ['C6', 'C1', 'C2', 'C3']
C6->C3 with C2 NEG: ['C6', 'C5', 'C4', 'C3']

 Example Explanation

First route shows a normal path from A2 to A5.

When station A4 is marked NEGATIVE, no valid path exists.

Once A4 is restored, the path works again.

On the circular line, the planner chooses the shortest path (C6 → C1 → C2 → C3).

If C2 is negative, it instead goes the other way (C6 → C5 → C4 → C3).
