from typing import Callable, List, Tuple, Union

def apply_operation(operations: List[Tuple[Callable, Tuple]]) -> List[Union[int, str]]:
    results = [operation(*params) for operation, params in operations]
    return results

# Example functions with different signatures
def add(x: int, y: int) -> int:
    return x + y

def multiply(x: int, y: int) -> int:
    return x * y

def concat_strings(x: str, y: str) -> str:
    return x + y

# Using the apply_operation function with different operations and parameters
operations_and_params = [
    (add, (3, 5)),
    (multiply, (2, 3)),
    (concat_strings, ("Hello", "World"))
]

results = apply_operation(operations_and_params)

for i in range(2,4):
    print(i)