# Soap Sort

## Introduction

Soap Sort is a physics-based sorting algorithm inspired by the soap in the bathroom. For each sort step, we will select a person and a soap, and let them move towards each other. The person will push the soap, and the soap will push the person. The person and the soap will continue to move until they meet.

## Implementation Details

The implementation uses a simplified physics model with the following components:

- Energy parameter: Controls the overall energy in the system
- Beta parameter: Affects the relationship between element value and mass/acceleration
- Threshold parameter: Determines when the system is considered stable

The algorithm terminates when all velocities fall below the threshold, indicating that the elements have settled into their sorted positions.

## Example

```python
from soap_sort import soap_sort

arr = [1, 4, 3, 2, 6, 5, 7, 8]
sorted_arr = soap_sort(arr.copy(), energy=100, beta=1, threshold=1)
print(sorted_arr)

# Output:
# [1, 2, 3, 4, 5, 6, 7, 8]
```

## Acknowledgements

Thanks to GPT and Claude for helping me with the implementation.
