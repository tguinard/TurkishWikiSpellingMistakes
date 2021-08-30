This project contains spelling mistake data extracted from Turkish Wikipedia

This dataset was developed as a part of my [master's thesis](https://digital.lib.washington.edu/researchworks/handle/1773/47616)

This data can be used under Creative Commons Attribution-ShareAlike. See [Wikipedia policy](https://en.wikipedia.org/wiki/Wikipedia:Reusing_Wikipedia_content) for details. 

## Data Format

The unpacked SpellingMistakes.tsv has the following fields
* Original word(s)
* Corrected word(s)
* Original left context
* Corrected left context
* Original right context
* Corrected right context
* Mistake Category
* Is original a word or nonword (according to [TRmorph](https://github.com/coltekin/TRmorph))

SpellingMistakesSample.tsv contains 100 random lines from the unzipped SpellingMistakes.tsv (so you can see what the data looks like before you decide to download)

The context is such that this string occurs in the original text (same logic works for corrected version):

    (Original left context) + " " + (Original word(s)) + " " + (Original right context)

Details for how the mistake category is computed is found in categorize.py
