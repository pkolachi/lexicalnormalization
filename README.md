## Multilingual Lexical Normalization

This is the repository belonging to the shared task on multilingual lexical normalization at WNUT 2021. More info can be found on [noisy-text.github.io/2021/multi-lexnorm.html](noisy-text.github.io/2021/multi-lexnorm.html)

This repository contains all data pre-processed in the same format:

```
Most	most
social	social
pple	people
r	are
troublesome	troublesome

```

Some of the languages include annotation for word splits and merges. When a
word is split, the normalization column include a white-space character, and
with a merge the normalization is only included for the first word:

```
if      If
i       i
have    have
a       a
head    headache
ache
tomorro tomorrow
ima     i'm going to
be      be
pissed  pissed

```

To read this data properly in python3, do not use `.strip().split()`, but use `.strip('\n').split('\t')` instead.

contents:

* data: contains the data per language. Note that development data is only included for the larger sets, for the smaller ones we suggest to use k-fold.
* scripts: baseline and evaluation scripts.

For any problems with the data (annotation), please post on  https://groups.google.com/u/2/g/multilexnorm.

