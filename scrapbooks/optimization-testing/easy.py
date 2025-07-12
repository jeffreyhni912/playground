"""
Two Sum 

Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.
 
"""

# class Solution:
#     def twoSum(self, nums: List[int], target: int) -> List[int]:
def twoSum(nums, target):
    nums = set(nums)
    n_map = {}
    
    for i, n in enumerate(nums):
        complement = target - n
        if complement in n_map:
            return [n_map[complement],i]
        n_map[n] = i
        print(n_map)
 
nums = [2,7,11,15]
target = 9

output = twoSum(nums, target)
print(output)