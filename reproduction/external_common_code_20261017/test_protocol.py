"""Checks scorer and layer handling with known-answer cases, without GPU dependencies."""
from audit_and_lexicon import entities,score,predict
assert entities(['O','B-S','I-S','B-K','O'])=={(1,3,'S'),(3,4,'K')}
assert entities(['B','I','O','B'])=={(0,2,'SPAN'),(3,4,'SPAN')}
assert entities(['I-S','I-S','I-K'])=={(0,2,'S'),(2,3,'K')}
assert score([{(0,2,'S')}],[{(0,1,'S')}])['f1']==0
assert score([{(0,2,'S')}],[{(0,2,'K')}])['f1']==0
assert score([{(0,2,'S')},set()],[{(0,2,'S')},{(1,2,'S')}])['f1']==2/3
assert predict(['a','b','c'],{'a':[(('a','b'),'S'),(('a',),'K')]})=={(0,2,'S')}
print('Seven known-answer span, type, BIO, negative-sentence, and lexical matching checks passed.')
