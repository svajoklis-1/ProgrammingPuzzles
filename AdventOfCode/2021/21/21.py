from abc import abstractmethod
from dataclasses import dataclass
import sys
import argparse

from typing import TextIO

INFINITY = 9223372036854775805

sys.path.append('../../../')


class Die:
    number_of_rolls: int

    @abstractmethod
    def roll(self):
        pass


class DeterministicDie(Die):
    next_value: int
    max_value: int
    number_of_rolls: int

    def __init__(self):
        self.next_value = 1
        self.max_value = 100
        self.number_of_rolls = 0

    def roll(self):
        self.number_of_rolls += 1
        result = self.next_value
        self.next_value = self.next_value + 1
        if self.next_value > 100:
            self.next_value = 1
        return result


class Player:
    position: int
    score: int
    times_won: int

    def __init__(self, starting_position: int):
        self.position = starting_position
        self.score = 0
        self.times_won = 0

    def __str__(self):
        return f'Player(position={self.position}, score={self.score}, times_won={self.times_won})'

    def __repr__(self):
        return self.__str__()


class DiracDiceGame:
    players: list[Player]
    current_player: int
    die: Die
    done: bool

    def __init__(self, die: Die, starting_positions: list[int]):
        self.players = []
        for starting_position in starting_positions:
            self.players.append(Player(starting_position))

        self.current_player = 0

        self.die = die

        self.done = False

    def make_move(self):
        assert not self.done, "Attempting to make a move on a completed game"

        values = []

        for _i in range(3):
            values.append(self.die.roll())
        value_sum = sum(values)

        player = self.players[self.current_player]
        player.position = (player.position + value_sum - 1) % 10 + 1
        player.score += player.position
        if player.score >= 1000:
            self.done = True
        self.current_player = (self.current_player + 1) % len(self.players)


def part_one(in_file: TextIO, out_file: TextIO):
    starting_positions = []
    for line in in_file:
        line = line.strip()
        if not line:
            break
        position = int(line.split(" ")[-1])
        starting_positions.append(position)
    die = DeterministicDie()
    game = DiracDiceGame(die, starting_positions)
    while not game.done:
        game.make_move()

    min_score = min([p.score for p in game.players])
    out_file.write(str(min_score * game.die.number_of_rolls))


won_iterations = 0


def play_round(players: list[Player], active_player: int, rolls: list[int], roll_value: int, number_of_occurrences: list[int], score: int):
    global won_iterations

    p = players[active_player]
    p.position = (p.position - 1 + roll_value) % 10 + 1
    p.score += p.position
    if p.score >= 21:
        p.times_won += score
        won_iterations += 1
        if won_iterations > 1_000_000:
            print(f'Player {active_player + 1} won {p.times_won} times')
            won_iterations = 0
    else:
        next_active_player = 0 if active_player == 1 else 1
        for roll in rolls:
            play_round(players, next_active_player, rolls, roll,
                       number_of_occurrences, score * number_of_occurrences[roll])
    p.score -= p.position
    p.position = (p.position - 1 - roll_value) % 10 + 1


def part_two(in_file: TextIO, out_file: TextIO):
    starting_positions = []
    for line in in_file:
        line = line.strip()
        if not line:
            break
        position = int(line.split(" ")[-1])
        starting_positions.append(position)

    players = [Player(starting_position) for starting_position in starting_positions]

    possible_rolls = []
    for a in [1, 2, 3]:
        for b in [1, 2, 3]:
            for c in [1, 2, 3]:
                possible_rolls.append(a + b + c)

    max_roll = max(possible_rolls)
    number_of_occurrences = [0] * (max_roll + 1)
    for roll in possible_rolls:
        number_of_occurrences[roll] += 1

    unique_rolls = []
    for roll in possible_rolls:
        if roll not in unique_rolls:
            unique_rolls.append(roll)

    for roll in unique_rolls:
        play_round(players, 0, unique_rolls, roll, number_of_occurrences, 1 * number_of_occurrences[roll])

    print(players)
    out_file.write(str(max([players[0].times_won, players[1].times_won])))


def main(file_name: str, part: str):
    with open(f'{file_name}.in', 'r', encoding='utf-8') as in_file:
        with open(f'{file_name}.{part}.out', 'w', encoding='utf-8') as out_file:
            match part:
                case 'one':
                    part_one(in_file, out_file)
                case 'two':
                    part_two(in_file, out_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Puzzle 16')
    parser.add_argument('--part', choices=['one', 'two'], required=True)
    parser.add_argument('in_file')
    args = parser.parse_args()

    main(args.in_file, args.part)
