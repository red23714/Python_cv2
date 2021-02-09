input = open("txt.txt", 'r')
output = open("txt.txt", 'a')
for i in input:
    for j in i:
        if j == ',':
            output.write('Hello world!\n')
            break

input.close()
output.close()
