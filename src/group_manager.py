import random

from src import universal_variables


class GroupManager:
    @staticmethod
    def check_collision(person1, person2):
        return (person1.x == person2.x) and (person1.y == person2.y)

    @staticmethod
    def update_groups(people):
        for player1 in people:
            for player2 in people:
                # If the two players chosen are not the same person, and they are colliding
                if player1 != player2 and GroupManager.check_collision(player1, player2):
                    # If the two players are not already part of the same group
                    if player1.group != player2.group:
                        merged_group = player1.group + player2.group  # Merge player groups

                        if player1.move_count < player2.move_count:
                            if player2.move_count > universal_variables.LONGEST_RUN_WITHOUT_MEETING:
                                universal_variables.LONGEST_RUN_WITHOUT_MEETING = player2.move_count
                        else:
                            if player1.move_count > universal_variables.LONGEST_RUN_WITHOUT_MEETING:
                                universal_variables.LONGEST_RUN_WITHOUT_MEETING = player1.move_count

                        player1.move_count = 0
                        player2.move_count = 0

                        # Make all players part of the new merged group
                        for players in merged_group:
                            players.group = merged_group  # Update references

                        return True

    @staticmethod
    def move_groups(people, grid_width, grid_height):
        group_leaders = {}

        for person in people:
            if tuple(person.group) not in group_leaders:
                group_leaders[tuple(person.group)] = person  # Pick a leader for each group

        for group, leader in group_leaders.items():
            direction = random.choice(['up', 'down', 'left', 'right'])
            new_x, new_y = leader.x, leader.y

            if direction == 'up' and leader.y > 0:
                new_y -= 1
            elif direction == 'down' and leader.y < grid_height - 1:
                new_y += 1
            elif direction == 'left' and leader.x > 0:
                new_x -= 1
            elif direction == 'right' and leader.x < grid_width - 1:
                new_x += 1

            for member in leader.group:
                member.x, member.y = new_x, new_y  # Move entire group
                member.move_count += 1
