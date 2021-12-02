from collections import Counter


def parse_range(input):
    start, end = input.split("-")
    return (int(start), int(end))


def is_valid_password(password):
    return (
        list(password) == sorted(password) and
        2 in Counter(password).values()
    )


def matching_passwords(start, end):
    possible_passwords = range(start, end + 1)
    return (p for p in possible_passwords if is_valid_password(str(p)))


def main():
    start, end = parse_range("359282-820401")
    print(len(list(matching_passwords(start, end))))


if __name__ == "__main__":
    main()
