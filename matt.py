import sys

def main(argv, stock, cash):
    if len(argv) < 1:
        return 0
    else:
        today = len(argv) - 1
        if (argv[today] > argv[today - 1]):
            return 0
        elif (argv[today] < argv[today - 1]):
            return 0
        else:
            return 0

if __name__ == "__main__":
    main(sys.argv, stock, cash)