# def multiply(*numbers):
#     total = 1
#     for number in numbers:
#         total *= number
#     return total


# print("start")
# print(multiply(1, 2, 3))
# print("finish")


def fizz_buzz(number: int):
    if (number % 3 == 0) and (number % 5 == 0):
        return "FizzBuzz"
    if number % 3 == 0:
        return "Fizz"

    if number % 5 == 0:
        return "Buzz"

    return number


print(fizz_buzz(15))
