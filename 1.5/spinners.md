# Spinners

Spinners let you tell the user that something is happening while you're processing. There are 3 basic ways to use a spinner:

* Instantiating a spinner and then using `.start()` and `.stop()` on your object.
* Using a context manager (`with cli.spinner(...):`)
* Decorate a function (`@cli.spinner(...)`)

For full details see the [`cli.spinner` api reference](api_milc.md#spinner).

### Adding a Spinner

If you'd like to create your own spinner animation you can do that. First you should define a dictionary with two keys, `interval` and `frames`:

```python
my_spinner = {
    'interval': 100,  # How many ms to display each frame
    'frames': ['-', '\\', '|', '/']
}
```

You can use this in one of two ways- by passing it directly to `cli.spinner()` or by adding it to the list of available spinners using `cli.add_spinner()`.

### Example: Using a custom spinner directly

```python
my_spinner = {
    'interval': 100,  # How many ms to display each frame
    'frames': ['-', '\\', '|', '/']
}

with cli.spinner(text='Loading', spinner=my_spinner):
    time.sleep(10)
```

### Example: Adding a custom spinner

```python
my_spinner = {
    'interval': 100,  # How many ms to display each frame
    'frames': ['-', '\\', '|', '/']
}
cli.add_spinner('my_twirl', my_spinner)

with cli.spinner(text='Loading', spinner='my_twirl'):
    time.sleep(10)
```

### Example: Instantiating a Spinner

```python
spinner = cli.spinner(text='Loading', spinner='dots')
spinner.start()

# Do something here

spinner.stop()
```

### Example: Using a Context Manager

```python
with cli.spinner(text='Loading', spinner='dots'):
    # Do something here
```

### Example: Decorating a Function

```python
@cli.spinner(text='Loading', spinner='dots')
def long_running_function():
    # Do something here
```
