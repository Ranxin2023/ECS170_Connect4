from copy import deepcopy
import numpy as np

line_num = 0

class ArrTest:
	def __init__(self):
		self.arr=[[1,2,1] for i in range(3)]

	def getArr(self):
		return self.arr


def recur(depth):
	if depth == 0:
		#print("depth is:{}".format(depth))
		return
	global line_num
	for i in range(7):
		print("depth is:{} {}".format(depth, line_num))
		line_num += 1
		recur(depth-1)
def func2(value):
	if value ==0:
		return
	print(value)
def test():
	test_class = ArrTest()
	ori_arr = deepcopy(test_class.getArr())
	shallow_arr = test_class.arr
	test_class.arr[0][0] = 4
	print("arr after changing:{}".format(test_class.getArr()))
	print("deepcopy arr:{}".format(ori_arr))
	print("shallow copy arr:{}".format(shallow_arr))
	#test_class.arr[0][0] = 1
	test_class.arr = ori_arr
	print("arr restore:{}".format(test_class.getArr()))
	arr = np.zeros((6,7)).astype('int32')
	print("np arr is: {}".format(arr))
	arr2 = (np.ones(7) * (5)).astype('int32')
	print("np arr2 is: {}".format(arr2))
	#recur(4)
	#print("recur finished")
	func2(0)
	func2(1)

test()