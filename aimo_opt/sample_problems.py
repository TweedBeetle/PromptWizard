import os
from dataclasses import dataclass
from typing import List
import json


@dataclass
class MathProblem:
    problem_statement: str
    solution: int


aimo_sample_problems: List[MathProblem] = [
    MathProblem(
        problem_statement="Three airline companies operate flights from Dodola island. Each company has a different schedule of "
                          "departures. The first company departs every 100 days, the second every 120 days and the third every "
                          "150 days. What is the greatest positive integer d for which it is true that there will be d consecutive "
                          "days without a flight from Dodola island, regardless of the departure times of the various airlines?",
        solution=79
    ),
    MathProblem(
        problem_statement="Let ABC be a triangle with BC = 108, CA = 126, and AB = 39. Point X lies on segment AC such that BX "
                          "bisects ∠CBA. Let ω be the circumcircle of triangle ABX. Let Y be a point on ω different from X such "
                          "that CX = CY. Line XY meets BC at E. The length of the segment BE can be written as n/m, where m and n "
                          "are coprime positive integers. Find m + n.",
        solution=751
    ),
    MathProblem(
        problem_statement="Triangle ABC has side length AB = 120 and circumradius R = 100. Let D be the foot of the perpendicular "
                          "from C to the line AB. What is the greatest possible length of segment CD?",
        solution=180
    ),
    MathProblem(
        problem_statement="Find the three-digit number n such that writing any other three-digit number 102024 times in a row and "
                          "102024 + 2 times in a row results in two numbers divisible by n.",
        solution=143
    ),
    MathProblem(
        problem_statement="Alice writes all positive integers from 1 to n on the board for some positive integer n ≥ 11. "
                          "Bob then erases ten of them. The mean of the remaining numbers is 3000/37. The sum of the numbers Bob "
                          "erased is S. What is the remainder when n × S is divided by 997?",
        solution=902
    ),
    MathProblem(
        problem_statement="For a positive integer n, let S(n) denote the sum of the digits of n in base 10. "
                          "Compute S(S(1) + S(2) + · · · + S(N )) with N = 10100 − 2.",
        solution=891
    ),
    MathProblem(
        problem_statement="The Fibonacci numbers are defined as follows: F0 = 0, F1 = 1, and Fn+1 = Fn + Fn−1 for n ≥ 1. "
                          "There are N positive integers n strictly less than 10 such that n2 + (n + 1)2 is a multiple of 5 "
                          "but Fn2−1 + Fn2 is not. How many prime factors does N have, counted with multiplicity?",
        solution=201
    ),
    MathProblem(
        problem_statement="For positive integers x1, . . . , xn define G(x1, . . . , xn) to be the sum of their n(n−1)/2 pairwise "
                          "greatest common divisors. We say that an integer n ≥ 2 is artificial if there exist n different positive "
                          "integers a1, ..., an such that a1 + · · · + an = G(a1, . . . , an) + 1. Find the sum of all artificial "
                          "integers m in the range 2 ≤ m ≤ 40.",
        solution=810
    ),
    MathProblem(
        problem_statement="We call a sequence a1, a2, . . . of non-negative integers delightful if there exists a positive integer N such that for all n > N, an = 0, and for all i ≥ 1, ai counts the number of multiples of i in a1, a2, . . . , aN. How many delightful sequences of non-negative integers are there?",
        solution=3
    ),
    MathProblem(
        problem_statement="Fred and George take part in a tennis tournament with 4046 other players. In each round, the players are paired into 2024 matches. How many ways are there to arrange the first round such that Fred and George do not have to play each other? (Two arrangements for the first round are different if there is a player with a different opponent in the two arrangements.)",
        solution=250
    ),
]


def save_problems_jsonl(problems: List[MathProblem], output_file: str) -> None:
    """Save math problems as JSONL file with question and answer keys."""
    import json
    with open(output_file, 'w') as f:
        for prob in problems:
            json_line = {
                'question': prob.problem_statement,
                'answer': str(prob.solution)  # Convert to string for consistency
            }
            f.write(json.dumps(json_line) + '\n')


if __name__ == '__main__':
    # Create data directory if it doesn't exist
    if not os.path.exists('opt_data'):
        os.makedirs('opt_data')

    # Save problems as JSONL
    save_problems_jsonl(aimo_sample_problems, 'opt_data/sample_problems.jsonl')
    print(f"Saved {len(aimo_sample_problems)} problems to opt_data/sample_problems.jsonl")
