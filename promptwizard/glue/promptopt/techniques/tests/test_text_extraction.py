import pytest
import re

from promptwizard.glue.promptopt.techniques.common_logic import DatasetSpecificProcessing


def test_text_delimiter_pattern():
    """Test the TEXT_DELIMITER_PATTERN regex pattern"""
    test_cases = [
        # Basic cases
        ("<START>test<END>", ["test"]),
        ("<START> test <END>", ["test"]),
        ("<START>\ntest\n<END>", ["test"]),

        # Multiple matches
        ("<START>test1<END><START>test2<END>", ["test1", "test2"]),

        # Empty content
        ("<START><END>", [""]),

        # No matches
        ("no tags here", []),

        # Whitespace handling
        ("<START>  spaced  <END>", ["spaced"]),

        # Multiline content
        ("<START>multiple\nlines\nhere<END>", ["multiple\nlines\nhere"]),

        # Real-world example
        ("<START>To solve this problem, apply mathematical reasoning...<END>",
         ["To solve this problem, apply mathematical reasoning..."]),
    ]

    for input_text, expected in test_cases:
        matches = re.findall(DatasetSpecificProcessing.TEXT_DELIMITER_PATTERN, input_text)
        assert matches == expected, f"Failed for input: {input_text}"


def test_answer_delimiter_pattern():
    """Test the ANSWER_DELIMITER_PATTERN regex pattern"""
    test_cases = [
        # Basic cases
        ("<ANS_START>42<ANS_END>", ["42"]),
        ("<ANS_START> 42 <ANS_END>", [" 42 "]),

        # Multiple answers
        ("<ANS_START>42<ANS_END><ANS_START>43<ANS_END>", ["42", "43"]),

        # Empty answer
        ("<ANS_START><ANS_END>", [""]),

        # No matches
        ("no tags here", []),

        # Whitespace handling
        ("<ANS_START>  spaced  <ANS_END>", ["  spaced  "]),

        # Multiline answers
        ("<ANS_START>line1\nline2<ANS_END>", ["line1\nline2"]),

        # Real-world example
        ("The answer is <ANS_START>42<ANS_END> because...", ["42"]),

        # Complex nested case
        ("Step 1: <ANS_START>First calculate x=5<ANS_END>\nStep 2: <ANS_START>Then y=10<ANS_END>",
         ["First calculate x=5", "Then y=10"])
    ]

    for input_text, expected in test_cases:
        matches = re.findall(DatasetSpecificProcessing.ANSWER_DELIMITER_PATTERN, input_text)
        assert matches == expected, f"Failed for input: {input_text}"


def test_text_delimiter_pattern_mutation():
    """Test that TEXT_DELIMITER_PATTERN_MUTATION matches TEXT_DELIMITER_PATTERN"""
    test_cases = [
        "<START>test<END>",
        "<START> test with spaces <END>",
        "<START>multiple\nlines\nhere<END>",
        "<START>test1<END><START>test2<END>"
    ]

    for input_text in test_cases:
        standard_matches = re.findall(DatasetSpecificProcessing.TEXT_DELIMITER_PATTERN, input_text)
        mutation_matches = re.findall(DatasetSpecificProcessing.TEXT_DELIMITER_PATTERN_MUTATION, input_text)
        assert standard_matches == mutation_matches, \
            f"Patterns produced different results for input: {input_text}"


def test_real_world_examples():
    """Test with real-world examples from the codebase"""
    examples = [
        # Example from critique_and_refine
        """Here are some suggestions:
        <START>To solve this mathematical problem efficiently, break it down into steps:
        1. First identify the key variables
        2. Apply the relevant formulas
        3. Calculate step by step
        4. Verify the answer matches constraints<END>
        """,

        # Example with answer format
        """The solution is:
        <ANS_START>The answer is 42 because:
        - Input value was 7
        - Multiplied by 6 
        - Therefore 7 * 6 = 42<ANS_END>
        """,

        # # Example of refined prompts
        # """Here are the refined prompts:
        #
        # <START> To solve this problem, apply your knowledge of number theory, Fibonacci numbers, and prime factors, and use mathematical techniques such as modular arithmetic and prime factorization to carefully analyze the given conditions and constraints. Break down the problem into smaller parts, systematically explore the possible values of n, and precisely calculate the required quantities to determine the number of prime factors of N, ensuring a rigorous and precise approach to reach an integer numerical answer. </END>
        #
        # <START> Using a systematic and rigorous approach, analyze the problem by breaking down the conditions and constraints into smaller parts, and apply your knowledge of number theory, Fibonacci numbers, and prime factors to determine the number of prime factors of N. Ensure that you precisely calculate the required quantities, consider the specific constraints and conditions, such as the requirement that n is a positive integer strictly less than 10, and use mathematical techniques such as modular arithmetic and prime factorization to reach an integer numerical answer. </END>
        #
        # <START> To determine the number of prime factors of N, carefully analyze the given conditions and constraints, and apply your knowledge of number theory, Fibonacci numbers, and prime factors. Use a systematic approach to break down the problem into smaller parts, precisely calculate the required quantities, and consider the specific constraints and conditions, ensuring a rigorous and precise approach to reach an integer numerical answer. Additionally, think creatively and consider alternative approaches, such as using modular arithmetic and prime factorization, to efficiently solve the problem. </END>
        #
        # However, I will provide only one as per your request:
        #
        # <START> To solve this problem, apply your knowledge of number theory, Fibonacci numbers, and prime factors, and use mathematical techniques such as modular arithmetic and prime factorization to carefully analyze the given conditions and constraints. Break down the problem into smaller parts, systematically explore the possible values of n, and precisely calculate the required quantities to determine the number of prime factors of N, ensuring a rigorous and precise approach to reach an integer numerical answer. </END>"""
    ]

    for example in examples:
        if "<START>" in example:
            matches = re.findall(DatasetSpecificProcessing.TEXT_DELIMITER_PATTERN, example)
            assert len(matches) > 0, "Failed to match START/END tags"
            assert all(len(m.strip()) > 0 for m in matches), "Empty matches found"

        if "<ANS_START>" in example:
            matches = re.findall(DatasetSpecificProcessing.ANSWER_DELIMITER_PATTERN, example)
            assert len(matches) > 0, "Failed to match ANS_START/ANS_END tags"
            assert all(len(m.strip()) > 0 for m in matches), "Empty matches found"
