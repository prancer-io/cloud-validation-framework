Update the parser, lexer and token files for changes in comparator.g4 file. 
cd <clonedir>/src/processor/comparison/comparisonantlr
Install antlr tools
pip install antlr4-tools
Generate the files
antlr4 -Dlanguage=Python3 comparator.g4
Commit and push the files to thee branch.
git add comparatorLexer.py comparatorListener.py comparatorParser.py
git commit -m "Updated parser and lexer generated files for 4.13.0 version"
git push origin <branchname>


