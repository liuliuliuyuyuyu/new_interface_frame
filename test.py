class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        for i in range(0, len(nums) - 1):
            for j in range(i + 1, len(nums)):
                print(j)
                if nums[i] + nums[j] == target:
                    List = [i, j]
                    return List


if __name__ == '__main__':
    print(Solution().twoSum(nums=[3,2,4],target=6))
