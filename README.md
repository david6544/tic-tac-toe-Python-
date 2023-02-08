- This project is tic-tac-toe, based in the terminal, with an unbeatable AI as an opponent, utilising the minimax algorithm for computation, with optimisation provided by alpha-beta pruning, There is also a robot with precomputed moves, cached which is slightly faster than the optimized minimax.


Installing

```shell
$ cd tic-tac-toe/
$ python -m venv venv/
$ source venv/bin/activate
(venv) $ python -m pip install library/
```


Game Front Ends

```shell
$ cd tic-tac-toe/frontends/
(venv) $ python -m console
```

You can optionally set one or both players to a human player (`human`), a computer player making random moves (`random`), or an unbeatable minimax computer player (`minimax`), as well as change the starting player:

To change which version of the minimax you play against, modify the last line in engine/players.py, to see the difference in calculation speed

```shell
(venv) $ python -m console -X minimax -O random --starting O
```

