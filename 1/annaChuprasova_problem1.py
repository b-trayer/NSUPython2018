def function(input_number):
    result = []
    current_number = input_number
    probe = 2
    while current_number > 1:
        if current_number % probe != 0:
            probe += 1
        else:
            current_number /= probe
            result.append(probe)
    return result

def make_a_list_nested(input_list):
    result = []
    power = 1
    for i in range(len(input_list)-1):
        if input_list[i] == input_list[i+1]:
            power +=1
        else:
            list = [input_list[i], power]
            result.append(list)
            power = 1

    list = [max(input_list), power]
    result.append(list)
    print (result)

input_number = int (input("print a number: "))
make_a_list_nested (function(input_number))

