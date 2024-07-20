```python
def rprint(*args, color='blue', sep=' ', end='\n', flush=False):
    
    palette = ['black', 'red', 'green', 'yellow', 
               'blue', 'magenta', 'cyan', 'white']
    color = f'\033[3{palette.index(color)}m'
    RESET = "\033[0m"

    print(f'{color}{sep.join(args)}{RESET}', end=end, flush=flush)
    
rprint('hello') # blue 'hello'
rprint('hello', color='red') # red 'hello'
```


