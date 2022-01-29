def findTwinPrimes(num):
    primes = [2]
    check = 3
    for x in range(num):
        isPrime = True
        for x in primes:
            if check % x == 0:
                isPrime = False
        if isPrime:
            primes.append(check)
            if primes[-2] + 2 == primes[-1]:
                print(primes[-2], primes[-1], sep = ",")
        check += 1
    return primes

findTwinPrimes(100000)
