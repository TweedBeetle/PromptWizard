from aimo_opt.optimize_aimo import AMCProcessor


def test_extract_final_answer_with_code():
    """Test code block execution and answer extraction"""
    processor = AMCProcessor()

    # Test with valid Python code block
    response = '''
    Here's the solution:
    ```python
    x = 5 + 3
    print(x)
    ```
    '''
    assert processor.extract_final_answer(response) == "8"

    # Test with multiple print statements
    response = '''
    ```python
    print("intermediate")
    print(42)
    print("final:", 79)
    ```
    '''
    assert processor.extract_final_answer(response) == "79"

    # Test with computation
    response = '''
    ```python
    import math
    result = math.factorial(4)
    print(result)
    ```
    '''
    assert processor.extract_final_answer(response) == "24"

    # Test with invalid code
    response = '''
    ```python
    x = 1/0  # Division by zero error
    ```
    '''
    assert processor.extract_final_answer(response) == processor.INVALID_ANS

    # Test with non-numeric output
    response = '''
    ```python
    print("hello")
    ```
    '''
    assert processor.extract_final_answer(response) == processor.INVALID_ANS

    # Test with boxed answer
    response = r'\boxed{42}'
    assert processor.extract_final_answer(response) == "42"

    # Test with both code and boxed answer - should use code output
    response = '''
    ```python
    print(79)
    ```
    Final answer: \boxed{42}
    '''
    assert processor.extract_final_answer(response) == "79"

    # Test with no valid answer format
    response = "The answer is 42"
    assert processor.extract_final_answer(response) == processor.INVALID_ANS

    # Test with empty input
    assert processor.extract_final_answer("") == processor.INVALID_ANS
    assert processor.extract_final_answer(None) == processor.INVALID_ANS
