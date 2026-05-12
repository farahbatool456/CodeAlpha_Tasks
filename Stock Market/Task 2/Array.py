#Different Methods in Array

from array import array

num_d = array('d',[5.4,78.9,6.43,23.23])  # Double: typecode 'd'
num_u = array('u',['a','b','c','d'])      # Unicode Char: typecode 'u'
print(num_d)
print(num_u)




arr = array('i', [10, 20, 30, 40])

#Append()
arr.append(600)

# Access[]
print("Element at index 2:", arr[2])

# Insert()
arr.insert(1, 15)
print("After Insertion:", arr)

# Delete()
arr.remove(30)
print("After Deletion:", arr)

#Pop()
print("Pop the index[2]: ",arr.pop(2))
print(arr)

# Search()
print("Index of 40:", arr.index(40))


#Buffer_info()
print(arr.buffer_info())


#tolist()
print(arr.tolist())


# Traverse
for val in arr:
    print(val)


#Problem 1
from array import * 

num = array('i',[34,67,32,456,77,43])

newarr = array(num.typecode , (a for a in num))

for e in newarr:
    print(e)











#Problem 1
#Reverse The Array
# def reverse_arr(arr):
#     start,end = 0, len(arr)-1

#     while start < end:
#         arr[start],arr[end] = arr[end],arr[start]
#         start += 1
#         end -=1
#     return arr  

# print(reverse_arr([575,4564,3,5332,456,3566,43,3455,355]))

#Problem 2
#Find Min and Max Num

# def find_min_max(arr):
#     if not arr:
#         return None,None
#     min = max = arr[0]

#     for num in arr[1:]:
#         if min < num:
#             min = num
#         if max > num:
#             max = num    

#     return min , max  

# print(find_min_max([23,67,34,45,34,23]))

      