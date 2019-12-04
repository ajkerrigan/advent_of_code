def parse_range(input):
    start, end = input.split('-')
    return (int(start), int(end)) 

def is_valid_password(password):
    if list(password) != sorted(password):
        return False

    current_repeat_length = 1
    repeat_lengths = set()

    for i, char in enumerate(password[1:]):
        if char == password[i]:
            current_repeat_length += 1
        else:
            repeat_lengths.add(current_repeat_length)
            current_repeat_length = 1
    repeat_lengths.add(current_repeat_length)
    return 2 in repeat_lengths
        
def matching_passwords(start, end):
    possible_passwords = range(start, end+1)
    return (
        p for p in possible_passwords
        if is_valid_password(str(p))
    )

if __name__ == '__main__':
    start, end = parse_range('359282-820401')
    print(len(list(matching_passwords(start, end))))
