def factorial(n : int) -> int:
	if not n:
		return 1
	m = n - 1
	return factorial(m)

factorial(5)
x : int = factorial(10)

print(x, factorial(7))

i = 0
while i < 100:
	i : int
	if i % 7 == 0:
		z : float = factorial(i)
		z = z * z
	else:
		z : float = factorial(i)
		z = z * z * z
	
x = 2

print()
