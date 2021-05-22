#!/usr/bin/python3

# Author: Ron Haber
# Date: 22.5.2021
# A test script to check any scripts for usability

import Game.pong_class as pc

new_pong = pc.pong_class(num_of_users=4)
new_pong.execute_game()