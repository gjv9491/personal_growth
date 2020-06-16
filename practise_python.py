import os

#Write a function that returns the elements on odd positions (0 based) in a list

def solution(input):
    return [number for number in input if (input.index(number) % 2) != 0]

assert solution([0,1,2,3,4,5]) == [1,3,5]
assert solution([1,-1,2,-2]) == [-1, -2]

#Write a function that returns cummulative sum of elements in a list
def solution(input):
    sum_list=[]
    for number in input:
        if len(sum_list) != 0:
            sum_list.append(sum_list[-1] + number)
        else:
            sum_list.append(number)
    return(sum_list)

assert solution([1,1,1]) == [1,2,3]
assert solution([1,-1,3]) == [1,0,3]

#one example
def Cumulative(lists):
    cu_list = []
    length = len(lists)
    cu_list = [sum(lists[0:x:1]) for x in range(0, length + 1)]
    return cu_list[1:]


# Driver Code
#lists = [10, 20, 30, 40, 50]
#print(Cumulative(lists))


#Write a function that takes numbers and returns a list of digits
def solution(input):
    return [int(item) for item in str(input)]

assert solution(123) == [1,2,3]
assert solution(400) == [4,0,0]

#Write a centered avaerage of an array
def solution(input):
    middle_index = len(input)/2
    int_value=int(middle_index)
    if middle_index.is_integer():
        return int((input[int_value]+input[int_value-1])/2)
    else:
        return (input[int(middle_index - .5)])

assert solution([1,2,3,4,100]) == 3
assert solution([1,1,5,5,10,8,7]) == 5
assert solution([-10, -4, -2, -4, -2, 0]) == -3


#Write a function that returns largest number in a list
def solution(input):
    val=0
    for item in input:
        if item > val:
            val=item
    return val

print(solution([0,10,2,3,14,5,6,7]))

#min occurance
def singleNumber(self, nums):
    track = {}
    for item in nums:
        if item not in track.keys():
            track[item] = 0
        else:
            track[item] += 1
    return [k for k, v in track.items() if v == 0][0]


#max occurenace
def solution(input):
    d = {}
    for i in input:
        if i not in d.keys():
            d[i] = 0
        else:
            d[i] += 1
    result = max(d.items(), key=lambda x: x[1])
    return ("value  {} repeats {} time".format(result[0],result[1]))

print(solution([1,2,45,55,5,4,4,4,4,4,4,5456,56,6,7,67]))


def solution(input):
    help_lst=[]
    for item in input:
        if len(help_lst) != 0 and item==None:
            help_lst.append(help_lst[-1])
        else:
            help_lst.append(item)
    return(help_lst)

assert solution([None,None,1,None,2,None,3, None]) == [None, None, 1, 1, 2, 2, 3, 3]
#solution([None,8,None])