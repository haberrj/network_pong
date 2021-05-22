# network_pong

This module is designed to work between a server and several clients (up to 4).

# Server Side Instructions

The Backend/server.py script should be run on the server machine using the following command:
    python server.py -i "IP Address" -p PORT_#

# Client Side Instructions 

The client should run main.py on their machine using the following command:
    python main.py -i "IP Address" -p PORT_#

Once the connection has been established, a confirmation will be printed to the console, as well as the user number
that the user has been assigned.

# Gameplay
If the user is assigned either User 1 or User they must use the Up-Arrow-Key and Down-Arrow-Key for vertical movement.
In the case the user is assigned either User 3 or User 4, they must use the Right-Arrow-Key and the Left-Arrow-Key for horizontal movement.

There will be a score displayed beside each user's paddle. (Currently the score counts negative to show the number of points against that user)

# To Do's / Incomplete

Due to the nature of the task being only meant for a day's work there were two things that I didn't have time to debug and fully fix.
1. The scoring system:
    - As mentioned above, the scoring system isn't ideal since it only counts how many points have been scored on a user. Ideally, I would
        calculated the last paddle to touch the ball and give them the point. I would implement this by keeping a ticker as to which paddle touched
        the ball last and then assign them the point accordingly. For this I ran out of time and figured it was something minor that didn't really
        affect base functionality.
2. Leaving and re-entering the game:
    - Once a player leaves the game, at the moment their user slot will remain unfilled until the server script is reset. This was something I was
    implementing towards the end and ran out of time to finish it properly. I would have implemented it by introducing an array that gradually filled
    up the indices (setting to 1) and once a player had left, the index would free up (set to 0) and would be possible to fill up again. This would
    allow the user to take any unfilled position, rather than just the last one in the set. I had almost implemented it fully, but ran out of time while I was debugging.

# Requirements
- Tested with Ubuntu 20.04 but it should work on both MacOS and Windows 10
- Python 3.5 and above
    - For packages see requirements.txt
