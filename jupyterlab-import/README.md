## tree
```sh
.
├── util.ipynb
├── util.py
└── workdir
    └── main.ipynb
```

## util.py
```py
get_ipython().run_line_magic("run", "../util.ipynb")
```

## util.ipynb
```py
In [1]: import numpy as np
```

## workdir/main.ipynb
```py
In [1]: run ../util
In [2]: np.arange(5)
Out[2]: array([0, 1, 2, 3, 4])
```