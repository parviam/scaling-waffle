def findPrimes(num):
    primes = [2]
    check = 3
    for x in range(num):
        isPrime = True
        for x in primes:
            if check % x == 0:
                isPrime = False
        if isPrime:
            primes.append(check)
            print(primes[-1])
        check += 1
    return primes

findPrimes(1000)
