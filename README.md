# prisoners-dilemma-python-GA
Searching prisoner's dilemma solution by genetic algorithm

Prisonr's dilemma
=================
0 is cooperate, 1 is defect, below table shows the reward function to me.

|  <center></center> |  <center>Oppenent-Cooperate (0)</center> |  <center>Oppenent-Defect (1)</center> |
|:--------|:--------:|:--------:|
|**Me-Cooperate (0)** | <center>3</center> |<center>0</center> |
|**Me-Defect (1)** | <center>5</center> |<center>1</center> |

Goal
----

Find the maximum strategy to get maximum rewards (fitness).

Genetic Algorithm (GA)
======================

Encoding
--------

Use 64-bits chronosmes and 6-bits history.

64-bits is my strategy (0 or 1) what I suggest in next turn.

6-bits save the history of three previous matches. (C_m3 C_o3 C_m2 C_o2 C_m1 C_o1)
