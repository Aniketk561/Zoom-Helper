n = int(input("Enter a number : "))

try:
    try:
        print("try")
        print(x)
    except:
        print("except")
        print("ex done")
    finally:
        print("finally")
finally:
    print("elif success")
    print(n+1)