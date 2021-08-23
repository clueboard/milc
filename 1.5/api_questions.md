<a name="questions"></a>

# questions

Sometimes you need to ask the user a question. MILC provides basic functions for collecting and validating user input. You can find these in the `milc.questions` module.

<a name="questions.yesno"></a>

#### yesno

```python
yesno(prompt, *args, *, default=None, **kwargs)
```

Displays `prompt` to the user and gets a yes or no response.

Returns `True` for a yes and `False` for a no.

| Argument | Description |
|----------|-------------|
| prompt | The prompt to present to the user. Can include ANSI and format strings like milc's `cli.echo()`. |
| default | Whether to default to a Yes or No when the user presses enter.<br><br>None- force the user to enter Y or N<br>True- Default to yes<br>False- Default to no |

If you add `--yes` and `--no` arguments to your program the user can answer questions by passing command line flags.

```python
@cli.argument('-y', '--yes', action='store_true', arg_only=True, help='Answer yes to all questions.')
@cli.argument('-n', '--no', action='store_true', arg_only=True, help='Answer no to all questions.')
```

<a name="questions.password"></a>

#### password

```python
password(prompt='Enter password:', *args, *, confirm=False, confirm_prompt='Confirm password:', confirm_limit=3, validate=None, **kwargs)
```

Securely receive a password from the user. Returns the password or None.

| Argument | Description |
|----------|-------------|
| prompt | The prompt to present to the user. Can include ANSI and format strings like milc's `cli.echo()`. |
| confirm | Prompt the user to type the password again and make sure they match. |
| confirm_prompt | The prompt to present to the user. Can include ANSI and format strings like milc's `cli.echo()`. |
| confirm_limit | Number of attempts to confirm before giving up. Default: 3 |
| validate | This is an optional function that can be used to validate the password, EG to check complexity. It should return True or False and have the following signature:<br><br>`def function_name(answer):` |

<a name="questions.question"></a>

#### question

```python
question(prompt, *args, *, default=None, confirm=False, answer_type=str, validate=None, **kwargs)
```

Allow the user to type in a free-form string to answer.

| Argument | Description |
|----------|-------------|
| prompt | The prompt to present to the user. Can include ANSI and format strings like milc's `cli.echo()`. |
| default | The value to return when the user doesn't enter any value. Use None to prompt until they enter a value. |
| confirm | Present the user with a confirmation dialog before accepting their answer. |
| answer_type | Specify a type function for the answer. Will re-prompt the user if the function raises any errors. Common choices here include int, float, and decimal.Decimal. |
| validate | This is an optional function that can be used to validate the answer. It should return True or False and have the following signature:<br><br>`def function_name(answer, *args, **kwargs):` |

<a name="questions.choice"></a>

#### choice

```python
choice(heading, options, *args, *, default=None, confirm=False, prompt='Please enter your choice: ', **kwargs)
```

Present the user with a list of options and let them select one.

Users can enter either the number or the text of their choice. This will return the value of the item they choose, not the numerical index.

| Argument | Description |
|----------|-------------|
| heading | The text to place above the list of options. |
| options | A sequence of items to choose from. |
| default | The index of the item to return when the user doesn't enter any value. Use None to prompt until they enter a value. |
| confirm | When True present the user with a confirmation dialog before accepting their answer. |
| prompt | The prompt to present to the user. Can include color and format strings like milc's `cli.echo()`. |

Users can enter either the number or the text of their choice.

!> This will return the value of the item they choose, not the numerical index.

