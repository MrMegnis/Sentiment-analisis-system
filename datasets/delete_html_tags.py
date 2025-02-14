import re


def remove_html_tags(line):
    return re.sub(r'<[^>]+>', '', line)


with open("output.txt", 'w+', encoding="utf-8") as n:
    with open("input.txt", 'r+', encoding="utf-8") as f:
        for line in f.readlines():
            ln = remove_html_tags(line)

            # delete "=" for Google tables, which it substitutes before +
            if '=' == ln[0]:
                ln = ln[1:]

            n.write(ln)
