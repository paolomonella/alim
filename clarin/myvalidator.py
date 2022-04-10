from validator import validate

if validate("path/to/file.xml", "path/to/scheme.xsd"):
    print('Valid! :)')
else:
    print('Not valid! :(')
