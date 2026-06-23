# fibonacci.py
#
# Find the nth Fibonacci number using recursion.
#

def fib(n):

   if n == 0:    # simple case 1
      result = 0
   elif n == 1:  # simple case 2
      result = 1
   else:         # recursive case
      result = fib(n-2) + fib(n-1)

   return result

# now, let's test it
for i in range(10):
   print("fib(" + str(i) + ") =", fib(i))