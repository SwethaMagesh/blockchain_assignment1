FAKE NEWS APP


### TO generate news in a json file
```
 python generate_news.py --items 100
```

### To run a simulation
```
python main.py -N 50 -p 0.5 -q 0.1

```

### Features

1. Anyone is allowed to request the DApp for fact-checking a news article or item.
2. Anyone is allowed to register on the DApp as a fact-checker.
3. The fact-checkers can vote to say whether the news item is fake or not. The vote could be
 binary (0 or 1) or it could be a number over a range, say 1- 10, to indicate how truthful the
 news is (a higher number could imply that the voter thinks the news is more truthful).
4. The DApp considers all votes and outputs a single number indicating the fakeness or
 truthfulness of the news.

 (1) Sybil attack: A malicious person can create multiple identities and vote to skew the result in
any direction
(2) Method to evaluate or re-evaluate the trustworthiness of voters: The Dapp should evaluate
how trustworthy different voters are based on how they vote. Note that someone might game
the system to get a higher trustworthy rating. A method that is more robust to such gaming of
the system, is preferable.
(3) The opinions of more trustworthy voters should be given more weight. However, we must
keep in mind that someone may be more trustworthy for certain types of news and not others.
For example, someone may give excellent opinions about news related to Physics but is not
so trustworthy on topics related to Politics or Economics.
(4) Rational voters are to be incentivised to participate and vote truthfully to the best of their
ability.
(5) Uploading a news item: Some efficient method should be used to identify a news item (which
is to be evaluated) in the Dapp.
(6) Bootstrapping: If the Dapp does not have any trustworthy rating of different initial voters, then
how to get started with fact-checking news?