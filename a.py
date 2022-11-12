import re
import json

class Eijiro:
    def __init__(self, r=0, i=0):
        self.real = r
        self.imag = i

    def get_data(self):
        print(f'{self.real}+{self.imag}j')

def add_data( base, level, forms, description, out ):
    a = {}
    a['base'] = base
    a['level'] = level
    a['forms'] = forms
    a['desc'] = description
    out.append( a )

    
def main():

    alldata = []
    
    source = open("EIJIRO-1448.TXT", encoding="cp932")
#    source = open("mini.txt", encoding="cp932")

    prev_word = ""
    prev_description = ""
    prev_level = 0
    infected_forms = []

    for line in source:
        m = re.match(r"^■(?P<word>[^\{]+) (?: \{(?P<tag>.+)\} )?: (?P<description>.+)$", line)
        word = m.group("word")
        tag = m.group("tag")
        if tag:
            description = f'{{{m.group("tag")}}} {m.group("description")}'
        else:
            description = m.group("description")

        m = re.search(r"【レベル】(?P<level>\d+)", line)
        if m and m.group("level"):
            level = int(m.group("level"))
        else:
            level = 0

        m = re.search(r"【変化】(?P<infected>.*?)[【\n]", line)
        if m:
            infected_forms = re.findall( r'[a-zA-Z]+', m.group('infected') )

        if (prev_word == word):
            prev_description += "\n" + description
            prev_level = max(prev_level, level)
        else:
            if (prev_level >= 1):
                infected_forms.insert( 0, prev_word )
                add_data( prev_word, prev_level, infected_forms, prev_description, alldata )

            prev_word = word
            prev_description = description
            prev_level = 0
            infected_forms = []

    if (prev_level >= 1):
        infected_forms.insert( 0, prev_word )
        add_data( prev_word, prev_level, infected_forms, prev_description, alldata )

    source.close()

    print( json.dumps( alldata ) )


if __name__ == '__main__':
    main()
