# n-body

## profiling

To see the most critical parts of the code, run following:
```commandline
python -m cProfile -s tottime main.py 500000
```

The top most functions reported show functions with which the program spent most of the time.
For more info see [cProfile](https://docs.python.org/3/library/profile.html)
