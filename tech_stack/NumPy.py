import numpy as np
# ram,shyam,hanuman =  1,12,42
# arr = np.array(["ram","shyam","hanuman"])   # array creation
# print(arr,type(arr))
# print(arr[1])     # array indexing 


# ara = [1,212,"xcv",243123,34,23434,]
# array = np.array([1,2,3,4,5,6])
# print(array[0:5]*12)      # array slicing and vectorizaiton at the same time



# ary = np.array([12,21,34,54,65,6,7234,2356,4,34,5626,2134]).reshape(4,3)     # numpy array reshaping

# print(ary)


# NumPy array properties 
matrix = np.array([[1,2,4],[23,45,6],[234.45,134,123],["alkdf","lasdfj",23.34]])
print(matrix.shape)
print(matrix.ndim)
print(matrix.dtype)


# NumPy boolean indexing
profit_n_loss = np.array([1200.23,1111,23,-123,231,-123,124,-1112])
profit = profit_n_loss[profit_n_loss>0]
print(profit)
print(profit.astype(int))    # ! this one is important 


prices = np.array([100, 102, 98, 105, 97])
positive_days = prices[prices > 100]
print(positive_days)   # [102, 105]


# broadcasting
matrix = np.array([[1,2,3],[10,12,123]])
vector = np.array([10,12,1222])
print(vector + matrix)

print(matrix*vector)

matrix = np.array([12,12,12,12])
vector = np.array([0,1,2,3])

print(matrix+vector,matrix-vector,matrix*vector)


roi = np.array([1,0.12,-1.23,1.5,2.25,4,7,12])
print(np.mean(roi))
print(np.std(roi))    # std - standard deviation (it has a fomula) --  VOLATILITY
print(np.sum(roi))



# HOMEWORK
# Q1: Create an array of your last 5 trade profits: [500, -200, 150, 300, -50]
# Q2: Print the total number of trades (size)
# Q3: Get only the last 3 profits using slicing
# Q4: Add a flat ₹10 brokerage deduction to every profit using vectorized subtraction
# Q5: Create a 2D array representing 3 days of prices for 2 stocks, then print only Stock 2's full price column