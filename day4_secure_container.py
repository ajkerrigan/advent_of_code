def parse_range(input):
    start, end = input.split('-')
    return (int(start), int(end)) 

def is_valid_password(password):
    repeated_digit = False
    always_increase = True
    prev_char = None
    for char in list(str(password)):
        if prev_char and int(char) < int(prev_char):
            always_increase = False
            break
        elif char == prev_char:
            repeated_digit = True
        prev_char = char
    return (repeated_digit and always_increase)
        
def matching_passwords(start, end):
    possible_passwords = range(start, end+1)
    return (
        p for p in possible_passwords
        if is_valid_password(p)
    )

if __name__ == '__main__':
    start, end = parse_range('359282-820401')
    print(len(list(matching_passwords(start, end))))
