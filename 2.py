def is_prime(input_number):
    probe = 2
    while input_number % probe != 0:
        probe += 1
    return input_number == probe

input_number = int(input("print a number: "))
if is_prime(input_number):
    print ("prime")
else:
    print ("composite")