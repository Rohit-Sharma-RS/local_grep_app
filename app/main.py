import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!


def matcher(input_line, pattern):
    ptr1 = 0
    ptr2 = 0

    # Base cases
    if input_line == "" and pattern == "":
        return True
    elif input_line == "":
        return False
    elif pattern == "":
        return True

    for ptr1 in range(len(input_line)):
        if ptr2 + 1 < len(pattern) and pattern[ptr2:ptr2 + 2] == "\\d":
            if input_line[ptr1].isdigit():
                return matcher(input_line[ptr1 + 1:], pattern[ptr2 + 2:])
            else:
                continue
        elif ptr2 + 1 < len(pattern) and pattern[ptr2:ptr2 + 2] == "\\w":
            if input_line[ptr1].isalnum():
                return matcher(input_line[ptr1 + 1:], pattern[ptr2 + 2:])
            else:
                continue
        elif ptr2 + 1 < len(pattern) and pattern[ptr2 + 1] == '+':
            if pattern[ptr2] == '\\' and ptr2 + 2 < len(pattern):
                if pattern[ptr2 + 2] == 'd':
                    while ptr1 < len(input_line) and input_line[ptr1].isdigit():
                        if matcher(input_line[ptr1:], pattern[ptr2 + 3:]):
                            return True
                        ptr1 += 1
                elif pattern[ptr2 + 2] == 'w':
                    while ptr1 < len(input_line) and input_line[ptr1].isalnum():
                        if matcher(input_line[ptr1:], pattern[ptr2 + 3:]):
                            return True
                        ptr1 += 1
            else:
                while ptr1 < len(input_line) and input_line[ptr1] == pattern[ptr2]:
                    if matcher(input_line[ptr1:], pattern[ptr2 + 2:]):
                        return True
                    ptr1 += 1
        elif ptr2 < len(pattern) and input_line[ptr1] == pattern[ptr2]:
            return matcher(input_line[ptr1 + 1:], pattern[ptr2 + 1:])
        else:
            continue

    # If we reach here, check if the pattern is exhausted
    return ptr2 == len(pattern)


def match_pattern(input_line, pattern):
    if len(pattern) == 1:
        return pattern in input_line
    elif pattern=='\\d':
        return any(c.isdigit() for c in input_line)
    elif pattern == '\\w':
        return any(c.isalnum() for c in input_line)
    elif pattern.startswith('[') and pattern.endswith(']'):
        if pattern[1] == '^':
            return all(c not in pattern[2:-1] for c in input_line)
        return any(c in pattern[1:-1] for c in input_line)
    elif pattern.startswith('^'):
        return input_line.startswith(   pattern[1:])
    elif pattern.endswith('$'):
        return input_line.endswith(pattern[:-1])
    elif '?' in pattern:
        c = pattern.index('?')
        pre_question = pattern[:c-1]
        optional_char = pattern[c-1]
        post_question = pattern[c+1:]

        # Check both possibilities: with or without the optional character
        if (pre_question + optional_char + post_question) in input_line or (pre_question + post_question) in input_line:
            return True
    else:       
        return matcher(input_line, pattern)


def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
