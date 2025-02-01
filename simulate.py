from abc import ABC, abstractmethod
import random
from typing import List, Set
import math
import csv


class Phase:
    def __init__(
        self,
        superstars: Set[int],
        first_prize_winners: Set[int],
        second_prize_winners: Set[int],
    ):
        self.superstars: Set[int] = superstars
        self.first_prize_winners: Set[int] = first_prize_winners
        self.second_prize_winners: Set[int] = second_prize_winners


class Environment:
    def __init__(self):
        self.phases: List[Phase] = []
        self.total_phases = 7
        self.superstar_player_quotas = [2, 2, 2, 3, 3, 3, 7]
        self.all_superstars = set()
        self.all_first_prize_winners = set()

    def get_current_phase_idx(self):
        return len(self.phases)

    def add_phase(self, phase: Phase):
        self.phases.append(phase)
        self.all_superstars.update(phase.superstars)
        self.all_first_prize_winners.update(phase.first_prize_winners)

    def find_is_already_superstar(self, id):
        return id in self.all_superstars

    def find_is_already_first_prize_winner(self, id):
        return id in self.all_first_prize_winners


class Agent(ABC):
    def __init__(self, id: int, env: Environment):
        self.id: int = id
        self.num_jades: int = 0
        self.env: Environment = env

    @abstractmethod
    def decide_should_gamble(self):
        pass


class ColdFeetAgent(Agent):
    def decide_should_gamble(self):
        return False


class ReachForTheStarsAgent(Agent):
    def decide_should_gamble(self):
        return not env.find_is_already_superstar(self.id)


class FirstPrizeEnjoyerAgent(Agent):
    def decide_should_gamble(self):
        return not env.find_is_already_first_prize_winner(self.id)


class LatecomerAgent(Agent):
    def __init__(self, id: int, env: Environment, starting_phase_idx: float = 3):
        super().__init__(id, env)
        self.starting_phase_idx = starting_phase_idx

    def decide_should_gamble(self):
        should_gamble = self.env.get_current_phase_idx() >= self.starting_phase_idx
        return should_gamble


class QuitterAgent(Agent):

    def __init__(
        self,
        id: int,
        env: Environment,
        initial_risk: float = 1,
        risk_adjustment_factor: float = 0.8,
    ):
        super().__init__(id, env)
        self.initial_risk: float = initial_risk
        self.risk_adjustment_factor: float = risk_adjustment_factor

    def decide_should_gamble(self):
        risk = (
            self.initial_risk
            * self.risk_adjustment_factor ** self.env.get_current_phase_idx()
        )
        should_gamble = random.uniform(0, 1) < risk
        return should_gamble


class RandoNoobAgent(Agent):
    def __init__(self, id, env: Environment, initial_risk: float = 0.5):
        super().__init__(id, env)
        self.initial_risk: float = initial_risk

    def decide_should_gamble(self):
        should_gamble = random.uniform(0, 1) < self.initial_risk
        return should_gamble


def set_up_random_scenario(total_players: int):
    env = Environment()
    players = []
    for i in range(total_players):
        x = random.randint(0, 5)
        if x == 0:
            players.append(ColdFeetAgent(id=i, env=env))
        elif x == 1:
            players.append(ReachForTheStarsAgent(id=i, env=env))
        elif x == 2:
            players.append(FirstPrizeEnjoyerAgent(id=i, env=env))
        elif x == 3:
            players.append(LatecomerAgent(id=i, env=env))
        elif x == 4:
            players.append(QuitterAgent(id=i, env=env))
        elif x == 5:
            players.append(RandoNoobAgent(id=i, env=env))
    return env, players


if __name__ == "__main__":
    total_players = 5000000

    # Setup
    print("Setting up simulation...")
    env, players = set_up_random_scenario(total_players)

    # Run simulation
    for idx in range(env.total_phases):
        print(f"Processing phase={idx}...")
        gambling_player_ids = []
        for player in players:
            should_gamble = player.decide_should_gamble()
            if should_gamble:
                gambling_player_ids.append(player.id)

        # Find superstars
        print("Finding superstars...")
        superstars = []
        superstar_quota = env.superstar_player_quotas[env.get_current_phase_idx()]
        if len(gambling_player_ids) >= superstar_quota:
            while True:
                superstars = set(
                    random.sample(
                        gambling_player_ids,
                        env.superstar_player_quotas[env.get_current_phase_idx()],
                    )
                )
                is_valid_draw = not any(
                    [env.find_is_already_superstar(id) for id in superstars]
                )
                if is_valid_draw:
                    break
        remaining_player_ids = [
            id for id in gambling_player_ids if id not in superstars
        ]

        # Find 1st prize
        print("Finding first prize winners...")
        first_prize_player_quota = math.floor(len(remaining_player_ids) * 0.1)
        first_prize_winners = set(
            random.sample(remaining_player_ids, first_prize_player_quota)
        )

        # Find 2nd prize winners
        print("Finding second prize winners...")
        second_prize_winners = set(
            [id for id in remaining_player_ids if id not in first_prize_winners]
        )

        print("Generating phase...")
        phase = Phase(
            superstars,
            first_prize_winners,
            second_prize_winners,
        )
        env.add_phase(phase)

        # Award jades
        for player in players:
            if player.id in phase.superstars:
                player.num_jades += 500000
            elif player.id in phase.first_prize_winners:
                player.num_jades += 600
            elif player.id in phase.second_prize_winners:
                player.num_jades += 50
            else:
                player.num_jades += 100

    print("Writing results...")
    with open("results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(["id", "agent_type", "num_jades"])
        for player in players:
            writer.writerow([player.id, player.__class__.__name__, player.num_jades])

    print("Done!")
