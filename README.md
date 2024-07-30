# Simon's Congruence Pattern Mining Using Simon Tree

## Introduction
This repository is used to help implementing Simon's Congruence Pattern Mining problem using Simon Tree. The problem is given as following:  
> Given text $T$, integer $k$, alphabet $\Sigma$, get pattern $P$ that maximizes the following equation:
> $\lvert \lbrace (i,j) | T[i:j] \sim_k P \rbrace \rvert$

## Milestones
- ~~Implement Simon Tree Construction~~ (Done)
- Implement Constructing the S-connection (and solving $\rm MaxSimK$)
- Extra modifications to help solving the main problem
  - List of modifications are to be added

## Usage
### Getting Simon Tree of given string
Use the following command:  
```
python stree.py <your_string>
```

## Known issues
- `stree.py` script doesn't accept whitespace
- `stree.py` script prints indices in from-0 manner instead of from-1 manner
  - This is intended behaviour but may be changed in distant future
