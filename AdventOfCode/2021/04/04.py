import argparse


NUM_CELLS = 25
NUM_SIDE = 5


class Ticket:
    def __init__(self, numbers):
        self.numbers = numbers
        self.marked = [False for i in range(NUM_CELLS)]
        self.won = False

    def is_winning(self):
        # rows
        for i in range(NUM_SIDE):
            count_r = 0
            count_c = 0
            for j in range(NUM_SIDE):
                count_r += 1 if self.marked[i * NUM_SIDE + j] else 0
                count_c += 1 if self.marked[j * NUM_SIDE + i] else 0

            if count_r == NUM_SIDE or count_c == NUM_SIDE:
                return True

        return False

    def mark(self, number):
        for i in range(NUM_CELLS):
            if self.numbers[i] == number:
                self.marked[i] = True
                break

    def get_unmarked_sum(self):
        winning_sum = 0
        for i in range(NUM_CELLS):
            if not self.marked[i]:
                winning_sum += self.numbers[i]

        return winning_sum


def read_tickets(in_file):
    tickets = []
    for line in in_file:
        line = line.strip()
        if len(line) == 0:
            continue

        ticket = [line]
        for i in range(4):
            ticket.append(in_file.readline())

        ticket = [[int(n) for n in l.strip().split(' ') if len(n) > 0] for l in ticket]
        ticket_nums = []
        for line in ticket:
            ticket_nums += line

        tickets.append(Ticket(ticket_nums))

    return tickets


def read_game_numbers(in_file):
    return [int(n) for n in in_file.readline().strip().split(',')]


def part_one(in_file_name):
    in_file = open(in_file_name, 'r')
    game_numbers = read_game_numbers(in_file)
    tickets = read_tickets(in_file)

    winning_ticket: Ticket = None
    winning_num = None
    for num in game_numbers:
        for ticket in tickets:
            ticket.mark(num)
            if ticket.is_winning():
                winning_ticket = ticket
                winning_num = num
                break

        if winning_ticket:
            break

    winning_sum = winning_ticket.get_unmarked_sum()
    print(winning_sum)
    print(winning_num)


def part_two(in_file_name):
    in_file = open(in_file_name, 'r')
    game_numbers = read_game_numbers(in_file)
    tickets = read_tickets(in_file)

    last_winning_ticket: Ticket = None
    last_winning_num = None
    for num in game_numbers:
        for ticket in tickets:
            if ticket.won:
                continue
            ticket.mark(num)
            if ticket.is_winning():
                ticket.won = True
                last_winning_ticket = ticket
                last_winning_num = num

    last_winning_sum = last_winning_ticket.get_unmarked_sum()
    print(last_winning_sum)
    print(last_winning_num)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Puzzle 04')
    parser.add_argument('--part', choices=['one', 'two'], required=True)
    parser.add_argument('in_file')
    args = parser.parse_args()

    match args.part:
        case 'one':
            part_one(args.in_file)
        case 'two':
            part_two(args.in_file)
