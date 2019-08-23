def get_pts_int(str):
    result = 0
    if str == '-':
        result = 0
    else:
        result = int(str, 10)
    return result
def get_eng_name(str):
    result = ''
    str = str.upper()
    for x in range(0, len(str)):
        ch = str[x].upper()
        if ch == 'Á' or ch == 'Â' or ch == 'À' or ch == 'Å' or ch == 'Ã' or ch == 'Ä' or ch == 'Ă':
            ch = 'A'
        if ch == 'Ç' or ch == 'Ć' or  ch == 'Č':
            ch = 'C'
        if ch == 'É' or ch == 'Ê' or ch == 'È' or ch == 'Ë' or ch == 'Ē' or ch == 'Ę':
            ch = 'E'
        if ch == 'Í' or ch == 'Î' or ch == 'Ì' or ch == 'Ï' or ch == 'İ':
            ch = 'I'
        if ch == 'Ñ' or ch == 'Ń':
            ch = 'N'
        if ch == 'Ó' or ch == 'Ô' or ch == 'Ò' or ch == 'Ø' or ch == 'Õ' or ch == 'Ö':
            ch = 'O'
        if ch == 'Š' or ch == 'Ś' or ch == 'Ș':
            ch = 'S'
        if ch == 'Ř':
            ch = 'R'
        if ch == 'Ð':			
            ch = 'D'
        if ch == 'Ú' or ch == 'Ü' or ch == 'Ů':
            ch = 'U'
        if ch == 'Ý':
            ch = 'Y'
        if ch == 'Ž' or ch == 'Ż':
            ch = 'Z'
        result += ch
    return result

def get_formatted_name(str):
    pos = str.index(' ')
    surname = str[:pos-1]
    familyname = str[pos+1:]
    tstr = familyname + ' ' + surname[0] + '.'
    tstr = tstr.upper()
    result = ''
    for x in range(0, len(tstr)):
        ch = tstr[x]
        if ch == 'Á' or ch == 'Â' or ch == 'À' or ch == 'Å' or ch == 'Ã' or ch == 'Ä' or ch == 'Ă':
            ch = 'A'
        if ch == 'Ç' or ch == 'Ć' or  ch == 'Č':
            ch = 'C'
        if ch == 'É' or ch == 'Ê' or ch == 'È' or ch == 'Ë' or ch == 'Ē' or ch == 'Ę':
            ch = 'E'
        if ch == 'Í' or ch == 'Î' or ch == 'Ì' or ch == 'Ï' or ch == 'İ':
            ch = 'I'
        if ch == 'Ñ' or ch == 'Ń':
            ch = 'N'
        if ch == 'Ó' or ch == 'Ô' or ch == 'Ò' or ch == 'Ø' or ch == 'Õ' or ch == 'Ö':
            ch = 'O'
        if ch == 'Š' or ch == 'Ś' or ch == 'Ș':
            ch = 'S'
        if ch == 'Ř':
            ch = 'R'
        if ch == 'Ð':			
            ch = 'D'
        if ch == 'Ú' or ch == 'Ü' or ch == 'Ů':
            ch = 'U'
        if ch == 'Ý':
            ch = 'Y'
        if ch == 'Ž' or ch == 'Ż':
            ch = 'Z'
        result += ch
    return result
