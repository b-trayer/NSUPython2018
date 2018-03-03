def is_prime(input_number):
    probe = 2
    while input_number % probe != 0:
        probe += 1
    return input_number == probe

input_number = int(input("print a number: "))
list = [1]
new_list = [i for i in range(2, input_number) if is_prime(i)]
list.extend(new_list)

print(list)
