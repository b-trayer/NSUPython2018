import math

input_number = int(input("print a number: "))
list = [True] * input_number

for i in range(2, int(math.sqrt(input_number))):
	for j in range(i * 2, input_number, i):
		list[j] = False

result = [i for i in range(2, input_number) if list[i]]

print(result)