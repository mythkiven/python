# coding: utf-8
"""
原生HTTP头转换为python dct形式
"""

def main():
    with open("text", "r") as f:
        for line in f:
            s = line.split(": ")
            s = list(map(lambda x: x.strip(), s))
            fmt = '"{key}": "{value}",'
            result = fmt.format(key=s[0], value=s[1])
            print(result)

if __name__ == '__main__':
    main()
