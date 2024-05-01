# import pip for the installation
import pip

# f = open('requirements.txt','r')
# f = f.read()
# print(f)

with open('test.txt', 'r', encoding='utf8', ) as f:
    contents = f.read()
    print(contents)