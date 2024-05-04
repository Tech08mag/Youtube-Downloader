# import pip for the installation
import pip

# load the content from the .txt file
with open('requirements.txt', 'r', encoding='utf8', ) as f:
    package = f.read()
    package = package.split()
    print(package)


def install(package):
        for n in package:
              pip.main(['install', n])

install(package)