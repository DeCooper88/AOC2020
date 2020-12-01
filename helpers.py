def file_reader(file, output='one_string'):
    """
    Return contents file as variable.
    output:
        'one_string' = file content as 1 string
        'lines' = list of strings (one for every line)
        'commas' = list of file content split on ','
    """
    with open(file) as f:
        if output == 'one_string':
            content = f.read()
            return content.strip()
        elif output == 'lines':
            return [x.strip() for x in f.readlines()]
        elif output == 'commas':
            raw = f.read()
            return [x.strip() for x in raw.split(',')]


def translator(input_string, map_table):
    mapper = {ord(k): v for k, v in map_table.items()}
    translated_string = input_string.translate(mapper)
    return translated_string
