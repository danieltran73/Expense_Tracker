def test(total, used):
    return total - used

def main():
    total = int(input("Total: "))
    used = str(input("Used: "))

    print(test(total, used))

main()