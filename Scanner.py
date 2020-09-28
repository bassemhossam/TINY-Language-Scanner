filepath=input()
tinycode = open(filepath, "r")
code = tinycode.read()
tiny_dict = {
    "reserved_words": (
                "if", "then", "else",
                "repeat", "read", "write",
                "until", "end"),
    "symbols": ("/", ":=", "+", "-", "^", "*", "=", "<", ">","(",")")
}
# function that takes a token and return the token + its id


def id_token(token):

    if len(token)>0:
        if token in tiny_dict["reserved_words"]:
            return token+",Reserved Word"
        elif token in tiny_dict["symbols"]:
            return token+",Symbol"
        # in case no spaces were left between operations
        for operator in tiny_dict["symbols"]:
            operator_index = token.find(operator)
            if operator_index == 0:
                return operator+",Symbol\r\n"+id_token(token[operator_index+len(operator):])
            elif operator_index == len(token)-1:
                return id_token(token[0:operator_index]) + "\r\n" + operator + ",Symbol"
            elif operator_index > 0:
                return id_token(token[0:operator_index])+"\r\n"+operator+",Symbol\r\n"+id_token(token[operator_index+len(operator):])

        if token[0].isdigit():
            return token+",Number"
        else:
            return token+",Identifier"
    else:
        return ""


# getting rid of comment contents first
begin = 0
braces_count = code.count("{")

for i in range(1, braces_count+1):
    comment_start = code.find('{', begin)
    begin = comment_start+1
    comment_end = code.find('}', comment_start)
    code = code[0:comment_start]+code[comment_end+1:]

code_split_semicolon = code.split(";")
output = open("ScannerOutput.txt", "wb")
for line in code_split_semicolon:
    if len(line) > 0:
        split_line = line.split()
        for token in split_line:
            if len(token) > 0:
                output.write(bytes(id_token(token)+"\r\n", 'UTF-8'))
        if line != code_split_semicolon[-1]:
            output.write(bytes(";,symbol\r\n", 'UTF-8'))

