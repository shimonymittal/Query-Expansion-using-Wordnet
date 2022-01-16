# Query-Expansion-using-Wordnet
Query expansion is the idea where, “users give additional input on query words or phrases,
possibly suggesting additional query terms"1. Furthermore,
highlight the matching keywords. A good example can be below.
eg.
User query: cancer
PubMed query: ("neoplasms"[TIAB] NOT Medline[SB]) OR "neoplasms"[MeSHTerms] OR cancer[TextWord]

Note the figure, how the term cancer is expanded into neoplasms based on a certain
domain. For this task, implement synonym query expansion using WordNet

Reference:

1https://nlp.stanford.edu/IR-book/html/htmledition/query-expansion-1.html
A theoretical reference to the IR text book
https://nlp.stanford.edu/IR-book/html/htmledition/relevance-feedback-and-query-expansion1.html
