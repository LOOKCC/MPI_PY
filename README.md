# Simple MPI In Python

## Installation
Install mpi4py in your conda environment.
```
pip install mpi4py
```

## Usage
First, define your function. And then
```
(-n for the number of process)
exec -n 5 python xxx.py
```

## Method
A simple Map-Reduce implementation used MPI.

## Warning
When I use it, I found that if your function is I/O consumed, Then your processes may be at D state(which you can use htop to have a look).
D means your process is waiting for I/O. So you need a lower n parameter or just ues a higher performance computer. 
