import sys

def main(argv, stock, cash):
    if len(argv) < 50:
        return 0
    else:
        today = len(argv) - 1
        if (argv[today] > argv[today - 1]):
            return 1
        elif (argv[today] < argv[today - 1]):
            return -1
        else:
            return 0


if __name__ == "__main__":
    main(sys.argv, stock, cash)
