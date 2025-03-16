import random
import universal_variables


def check_collision(person1, person2):
    """
    Checks if two people are colliding by comparing their positions.

    Args:
        person1: The first player object.
        person2: The second player object.

    Returns:
        bool: True if the players' positions (x, y) are the same, indicating a collision.
    """
    return (person1.x == person2.x) and (person1.y == person2.y)


def update_groups(people):
    """
    Updates the groups of players if they collide. Merges groups when two players
    collide and updates their statistics.

    Args:
        people: A list of all player objects to check for collisions and group updates.

    Returns:
        bool: True if any groups were merged; False otherwise.
    """
    for player1 in people:
        for player2 in people:
            # If the two players chosen are not the same person, and they are colliding
            if player1 != player2 and check_collision(player1, player2):
                # If the two players are not already part of the same group
                if player1.group != player2.group:
                    merged_group = player1.group + player2.group  # Merge player groups

                    # Update the longest run without meeting based on move counts
                    if player1.move_count < player2.move_count:
                        if player2.move_count > universal_variables.LONGEST_RUN_WITHOUT_MEETING:
                            universal_variables.LONGEST_RUN_WITHOUT_MEETING = player2.move_count
                    else:
                        if player1.move_count > universal_variables.LONGEST_RUN_WITHOUT_MEETING:
                            universal_variables.LONGEST_RUN_WITHOUT_MEETING = player1.move_count

                    player1.move_count = 0  # Reset move count for both players
                    player2.move_count = 0

                    # Make all players part of the new merged group
                    for players in merged_group:
                        players.group = merged_group  # Update references to the new merged group

                    return True  # Return True to indicate that a merge occurred


def move_groups(people, grid_width, grid_height):
    """
    Moves each group of players based on the chosen wandering strategy.

    Args:
        people: A list of all player objects whose groups will be moved.
        grid_width: The width of the grid.
        grid_height: The height of the grid.
    """
    if universal_variables.WANDERING_CHOICE == 'Random':
        move_groups_random(people, grid_width, grid_height)
    elif universal_variables.WANDERING_CHOICE == 'Random Valid':
        move_groups_random_valid(people, grid_width, grid_height)
    elif universal_variables.WANDERING_CHOICE == 'Biased Unexplored':
        move_groups_biased(people, grid_width, grid_height)
    else:
        print('Unrecognized universal_variables.WANDERING_CHOICE')


def move_groups_biased(people, grid_width, grid_height, memory_limit=5):
    """
    Moves each group on the grid, favoring unexplored directions.

    Args:
        people: A list of all player objects whose groups will be moved.
        grid_width: The width of the grid.
        grid_height: The height of the grid.
        memory_limit: The number of past positions to remember for the leader.
    """
    group_leaders = {}

    # Assign a leader to each group
    for person in people:
        if tuple(person.group) not in group_leaders:
            group_leaders[tuple(person.group)] = person  # Pick a leader for each group

    # Move each group based on its leader's direction
    for group, leader in group_leaders.items():
        possible_moves = [
            ('up', leader.x, leader.y - 1),
            ('down', leader.x, leader.y + 1),
            ('left', leader.x - 1, leader.y),
            ('right', leader.x + 1, leader.y)
        ]

        # Keep only valid moves within grid bounds
        valid_moves = []
        for direction, x, y in possible_moves:
            if 0 <= x < grid_width and 0 <= y < grid_height:
                valid_moves.append((direction, x, y))

        # Filter moves to avoid recently visited locations
        unexplored_moves = []
        print(leader.history)
        for direction, x, y in valid_moves:
            if (x, y) not in leader.history:
                unexplored_moves.append((direction, x, y))

        # Choose a direction based on unexplored locations, or move randomly if all are explored
        if unexplored_moves:
            direction, new_x, new_y = random.choice(unexplored_moves)
        else:
            direction, new_x, new_y = random.choice(valid_moves)  # If all are explored, move randomly

        # Move all members of the group
        for member in leader.group:
            member.x, member.y = new_x, new_y
            member.move_count += 1
            member.history.append((new_x, new_y))

            # Limit the size of the history list
            if len(member.history) > memory_limit:
                member.history.pop(0)


def move_groups_random_valid(people, grid_width, grid_height):
    """
    Moves each group on the grid based on valid random directions for the group leader.

    Args:
        people: A list of all player objects whose groups will be moved.
        grid_width: The width of the grid.
        grid_height: The height of the grid.
    """
    group_leaders = {}

    # Assign a leader to each group
    for person in people:
        if tuple(person.group) not in group_leaders:
            group_leaders[tuple(person.group)] = person  # Pick a leader for each group

    # Move each group based on its leader's direction
    for group, leader in group_leaders.items():
        direction = random.choice(['up', 'down', 'left', 'right'])  # Random direction
        new_x, new_y = leader.x, leader.y  # Start with the leader's current position

        # Determine the new position based on the direction
        if direction == 'up':
            if leader.y > 0:
                new_y -= 1
            else:
                new_y += 1
        elif direction == 'down':
            if leader.y < grid_height - 1:
                new_y += 1
            else:
                new_y -= 1
        elif direction == 'left':
            if leader.x > 0:
                new_x -= 1
            else:
                new_x += 1
        elif direction == 'right':
            if leader.x < grid_width - 1:
                new_x += 1
            else:
                new_x -= 1

        # Move all members of the group to the new position
        for member in leader.group:
            member.x, member.y = new_x, new_y  # Update position of each member in the group
            member.move_count += 1  # Increment move count for each group member


def move_groups_random(people, grid_width, grid_height):
    """
    Moves each group on the grid based on a random direction chosen for the group leader.

    Args:
        people: A list of all player objects whose groups will be moved.
        grid_width: The width of the grid.
        grid_height: The height of the grid.
    """
    group_leaders = {}

    # Assign a leader to each group
    for person in people:
        if tuple(person.group) not in group_leaders:
            group_leaders[tuple(person.group)] = person  # Pick a leader for each group

    # Move each group based on its leader's direction
    for group, leader in group_leaders.items():
        direction = random.choice(['up', 'down', 'left', 'right'])  # Random direction
        new_x, new_y = leader.x, leader.y  # Start with the leader's current position

        # Determine the new position based on the direction
        if direction == 'up' and leader.y > 0:
            new_y -= 1
        elif direction == 'down' and leader.y < grid_height - 1:
            new_y += 1
        elif direction == 'left' and leader.x > 0:
            new_x -= 1
        elif direction == 'right' and leader.x < grid_width - 1:
            new_x += 1

        # Move all members of the group to the new position
        for member in leader.group:
            member.x, member.y = new_x, new_y  # Update position of each member in the group
            member.move_count += 1  # Increment move count for each group member
