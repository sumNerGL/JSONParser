def ensure(condition, message):
    if not condition:
        print('*** 测试失败:', message)
    else:
        print('*** 测试成功')


def string_element(s):
    r = '"'
    ec = False
    for i, e in enumerate(s[1:]):
        r += e
        if ec:
            ec = False
            continue
        elif e == '\\':
            ec = True
        elif e == '"':
            break
    return r


def cut_blank(s):
    r = s
    start = True
    end = True
    blank_tokens = ' \n'
    if len(r) == 0:
        start = False
        end = False

    while start:
        if r[0] in blank_tokens:
            r = r[1:]
        else:
            start = False
    while end:
        if r[-1] in blank_tokens:
            r = r[:-1]
        else:
            end = False
    return r


def common_element(s):
    r = ''
    end_tokens = ']},:'
    if s[0] == '"':
        r = string_element(s)
        return r
    for i, e in enumerate(s):
        if e in end_tokens:
            r = s[:i]
            r = cut_blank(r)
            break
    return r


def fomatted_element(s):
    r = s
    num = '-0123456789'
    if r[0] in num:
        if '.' in r:
            return float(r)
        else:
            return int(r)
    elif r[0] == '"':
        r = r[1:-1]
        return r
    elif r == 'true':
        return True
    elif r == 'false':
        return False
    elif r == 'null':
        return None
    else:
        return r


def tokenizer(s):
    l = []
    count = 0
    tokens = '{}[],:'
    blank_tokens = ' \n'
    for i, e in enumerate(s):
        if count > 0:
            count -= 1
            continue
        elif e in blank_tokens:
            continue
        elif e in tokens:
            l.append(e)
        elif e == ' ':
            pass
        else:
            token = common_element(s[i:])
            count = len(token) - 1
            token = fomatted_element(token)
            l.append(token)
    return l


def list_element(l):
    r = []
    count = 0
    self_count = 0
    for i, e in enumerate(l):
        self_count += 1
        if count > 0:
            count -= 1
            continue
        if e == ']':
            break
        else:
            token, child_count = parser(l[i:])
            r.append(token)
            count += child_count
            if l[i+child_count+1] == ',':
                count += 1
    return r, self_count


def dict_element(l):
    r = {}
    count = 0
    self_count = 0
    for i, e in enumerate(l):
        self_count += 1
        if count > 0:
            count -= 1
            continue
        if e == '}':
            break
        else:
            k = e
            v, child_count = parser(l[i+2:])
            r[k] = v
            count += child_count + 2
            if l[i+count+1] == ',':
                count += 1
    return r, self_count


def parser(l):
    c = 0
    if l[0] == '{':
        r, child_count = dict_element(l[1:])
        c = child_count
        pass
    elif l[0] == '[':
        r, child_count = list_element(l[1:])
        c = child_count
    else:
        r = l[0]
    return r, c


def tree(s):
    l = tokenizer(s)
    r, c = parser(l)
    return r


def t_common_element():
    s1 = '''"employees": [
{ "firstName":"John" , "lastName":"Doe" },
{ "firstName":"Anna" , "lastName":"Smith" }
'''
    s2 = '123 , "lastName":"Smith" }'

    ensure(common_element(s1) == '"employees"', 'common_element 测试1')
    ensure(common_element(s2) == '123', 'common_element 测试2')


def t_tokenizer():
    s1 = '''{
"employees": [
{ "firstName":-12.34 , "lastName":null },
{ "firstName":true , "lastName":["Smith", 123] }
]
}'''


def t_tree():
    s1 = '''{
"employees": [
{ "firstName":-12.34 , "lastName":null },
{ "firstName":true , "lastName":["Smith", 123] }
]
}'''
    # s1 = '''{"employees": [{ "firstName":-12.34 , "lastName":null }]}'''
    print('字符串：', s1)
    print('>>>')
    print(tokenizer(s1))
    print('>>>')
    print('结果：', tree(s1))

    s2 = '''{
   "achievement" : [ "ach1", "ach2", "ach3" ],
   "age" : 23,
   "name" : "Tsybius",
   "partner" : {
      "partner_age" : 21,
      "partner_name" : "Galatea",
      "partner_sex_is_male" : false
   },
   "sex_is_male" : true
}'''
    print('\n\n')
    print('字符串：', s2)
    print('>>>')
    print(tokenizer(s2))
    print('>>>')
    print('结果：', tree(s2))


def t():
    pass
    # t_common_element()
    # t_tokenizer()
    t_tree()

t()
