

# 02.5
from random import randint
random_number = randint(1, 101)
print(random_number)

while random_number % 3 != 0 and random_number % 5 != 0:
    print("Random number is", random_number)
    random_number = randint(1, 101)

print("Random number is", random_number)
print(random_number % 3, "and", random_number % 5)


# 02.7
import random
numbers = [random.randint(1, 100) for i in range(10)]

for number in numbers:
    if number % 3 == 0 or number % 5 == 0:
        continue
    cubed = number ** 3
    if cubed > 1000:
        break
    print(cubed)