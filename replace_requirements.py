txt = ''
# requirements.txt 의 == 를 >= 로 replace
with open("requirements.txt", 'r', encoding='utf-16') as file:
    lines = file.readlines()
    for l in lines:
        txt += f'{l.replace("==",">=")}'

with open("requirements.txt",'w',encoding='utf-16') as file:
    file.write(txt)
