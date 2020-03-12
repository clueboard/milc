# Collecting User Input

Sometimes you need to ask the user a question. MILC provides basic functions for collecting and validating user input. You can find these in the `milc.questions` module.

## choice

Present the user with a list of options and let them select one. Users can enter either the number or the text of their choice. This will return the value of the item they choose, not the numerical index.

    def choice(heading, options, *args, default=None, confirm=False, prompt='Please enter your choice: ', **kwargs)

| Argument | Description |
|----------|-------------|
| `heading` | The text to place above the list of options. |
| `options` | A sequence of items to choose from. |
| `default` | The index of the item to return when the user doesn't enter any value. Use None to prompt until they enter a value. |
| `confirm` | When True present the user with a confirmation dialog before accepting their answer. |
| `prompt` | The prompt to present to the user. Can include color and format strings like milc's `cli.echo()`. |

## question

Allow the user to type in a free-form string to answer.

    question(prompt, *args, default=None, confirm=False, answer_type=str, validate=None, **kwargs)

| Argument | Description |
|----------|-------------|
| `prompt` | The prompt to present to the user. You can use [string formatting characters](https://docs.python.org/3/library/stdtypes.html#printf-style-string-formatting) here. |
| `default` | The value to return when the user doesn't enter any value. Use None to prompt until they enter a value. |
| `confirm` | Present the user with a confirmation dialog before accepting their answer. |
| `answer_type` | Specify a type function for the answer. Will re-prompt the user if the function raises any errors. Common choices here include `int`, `float`, and `decimal.Decimal`. |
| `validate` | This is an optional function that can be used to validate the answer. It should return True or False and have the following signature: <br><br>`def function_name(answer, *args, **kwargs)` |

## yesno

This function is useful for getting a boolean from the user. It will return True or False.

    yesno(prompt, *args, default=None, **kwargs)

| Argument | Description |
|----------|-------------|
| `prompt` | This text will be shown to the left of the cursor. You can use [string formatting characters](https://docs.python.org/3/library/stdtypes.html#printf-style-string-formatting) here.
| `default` | The value to return when the user doesn't enter any value. Use None to prompt until they enter a value.
| `args`/`kwargs` | These are used when doing string formatting on `prompt`.
