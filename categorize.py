from unidecode import unidecode
from collections import Counter
from fastDamerauLevenshtein import damerauLevenshtein

def equalspace(s1, s2):
    if s1.count(' ') != s2.count(' '):
        return False
    return True
    
def subdist(a, b):
    if len(a) != len(b):
        return float('inf')
    return sum(aa != bb for aa, bb in zip(a, b))
    
def turklower(s):
    return s.replace('I', 'ı').replace('İ', 'i').lower()
    
#rule-based categorizer
def getCategory(atok, btok):
    norma, normb = unidecode(atok).lower(), unidecode(btok).lower()
    asciia, asciib = unidecode(atok), unidecode(btok)
    lowa, lowb = turklower(atok), turklower(btok)
    if lowa == lowb:
        return 'capital'
    if asciia == asciib:
        return 'ascii'
    if norma == normb:
        return 'ascii-capital'
    if norma.replace("'", "") == normb.replace("'", ""):
        if atok.replace("'", "") == btok.replace("'", ""):
            return 'punct'
        if lowa.replace("'", "") == lowb.replace("'", ""):
            return 'punct-capital'
        if asciia.replace("'", "") == asciib.replace("'", ""):
            return 'punct-ascii'
        return 'punct-ascii-capital'
    if norma.replace(" ", "") == normb.replace(" ", ""):
        if atok.replace(" ", "") == btok.replace(" ", ""):
            if atok.replace(' ', '') == btok:
                return 'space:merge'
            if btok.replace(' ', '') == atok:
                return 'space:split'
            return 'space:mix'
        if lowa.replace(" ", "") == lowb.replace(" ", ""):
            if lowa.replace(' ', '') == lowb:
                return 'space:merge-capital'
            if lowb.replace(' ', '') == lowa:
                return 'space:split-capital'
            return 'space:mix-capital'
        if asciia.replace(" ", "") == asciib.replace(" ", ""):
            if asciia.replace(' ', '') == asciib:
                return 'space:merge-ascii'
            if asciib.replace(' ', '') == asciia:
                return 'space:split-ascii'
            return 'space:mix-ascii'
        return 'space-ascii-capital'
    if norma.replace("'", '').replace(' ', '') == normb.replace("'", '').replace(' ', ''):
        if atok.replace("'", '').replace(" ", "") == btok.replace("'", '').replace(" ", ""):
            return 'punct-space'
        if lowa.replace("'", '').replace(" ", "") == lowb.replace("'", '').replace(" ", ""):
            return 'punct-space-capital'
        if asciia.replace("'", '').replace(" ", "") == asciib.replace("'", '').replace(" ", ""):
            return 'punct-space-ascii'
        return 'punct-space-ascii-capital'
    if not equalspace(atok, btok):
        return 'space-other'
    if damerauLevenshtein(norma, normb, similarity=False) <= 3:
        if Counter(norma) == Counter(normb):
            if Counter(atok) == Counter(btok):
                return 'noise:jumble'
            if Counter(lowa) == Counter(lowb):
                return 'noise:jumble-capital'
            if Counter(asciia) == Counter(asciib):
                return 'noise:jumble-ascii'
            return 'noise:jumble-capital-ascii'
        if subdist(norma, normb) <= 3 and subdist(norma, normb) == damerauLevenshtein(norma, normb, similarity=False):
            if subdist(atok, btok) <= 3:
                return 'noise:sub'
            if subdist(lowa, lowb) <= 3:
                return 'noise:sub-capital'
            if subdist(asciia, asciib) <= 3:
                return 'noise:sub-ascii'
            return 'noise:sub-capital-ascii'
        if len(atok) - len(btok) == damerauLevenshtein(norma, normb, similarity=False):
            if len(atok) - len(btok) == damerauLevenshtein(atok, btok, similarity=False):
                return 'noise:insert'
            if len(atok) - len(btok) == damerauLevenshtein(lowa, lowb, similarity=False):
                return 'noise:insert-capital'
            if len(atok) - len(btok) == damerauLevenshtein(asciia, asciib, similarity=False):
                return 'noise:insert-ascii'
            return 'noise:insert-capital-ascii'
        if len(btok) - len(atok) == damerauLevenshtein(norma, normb, similarity=False):
            if len(btok) - len(atok) == damerauLevenshtein(atok, btok, similarity=False):
                return 'noise:delete'
            if len(btok) - len(atok) == damerauLevenshtein(lowa, lowb, similarity=False):
                return 'noise:delete-capital'
            if len(btok) - len(atok) == damerauLevenshtein(asciia, asciib, similarity=False):
                return 'noise:delete-ascii'
            return 'noise:delete-capital-ascii'
        if damerauLevenshtein(atok, btok, similarity=False) <= 3:
            return 'noise:other'
        if damerauLevenshtein(lowa, lowb, similarity=False) <= 3:
            return 'noise:other-capital'
        if damerauLevenshtein(asciia, asciib, similarity=False) <= 3:
            return 'noise:other-ascii'
    return 'far_apart'
    
if __name__ == '__main__':
    for line in open('SpellingMistakes.tsv', encoding='utf-8'):
        fields = line.split('\t')
        print(getCategory(fields[0], fields[1]))
