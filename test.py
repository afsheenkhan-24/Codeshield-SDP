# Armstrong Number Checker

num = int(input("Enter a number: "))
n = num
power = len(str(num))
total = 0

while n > 0:
    digit = n % 10
    total += digit ** power
    n //= 10

if total == num:
    print("Armstrong Number")
else:
    print("Not an Armstrong Number")
