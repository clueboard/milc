"""Sometimes you need to ask the user a question. MILC provides basic functions for collecting and validating user input. You can find these in the `milc.questions` module.
"""
from getpass import getpass

import milc
from .ansi import format_ansi


def yesno(prompt, *args, default=None, **kwargs):
    """Displays `prompt` to the user and gets a yes or no response.

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
    """
    if not args and kwargs:
        args = kwargs

    if 'no' in milc.cli.args and milc.cli.args.no:
        return False

    if 'yes' in milc.cli.args and milc.cli.args.yes:
        return True

    if not milc.cli.interactive:
        return False

    if default is None:
        prompt = prompt + ' [y/n] '
    elif default:
        prompt = prompt + ' [Y/n] '
    else:
        prompt = prompt + ' [y/N] '

    while True:
        answer = input(format_ansi(prompt % args))

        if not answer and default is not None:
            return default

        elif answer.lower() in ['y', 'yes']:
            return True

        elif answer.lower() in ['n', 'no']:
            return False


def password(prompt='Enter password:', *args, confirm=False, confirm_prompt='Confirm password:', confirm_limit=3, validate=None, **kwargs):
    """Securely receive a password from the user. Returns the password or None.

    | Argument | Description |
    |----------|-------------|
    | prompt | The prompt to present to the user. Can include ANSI and format strings like milc's `cli.echo()`. |
    | confirm | Prompt the user to type the password again and make sure they match. |
    | confirm_prompt | The prompt to present to the user. Can include ANSI and format strings like milc's `cli.echo()`. |
    | confirm_limit | Number of attempts to confirm before giving up. Default: 3 |
    | validate | This is an optional function that can be used to validate the password, EG to check complexity. It should return True or False and have the following signature:<br><br>`def function_name(answer):` |
    """
    if not milc.cli.interactive:
        return None

    if not args and kwargs:
        args = kwargs

    if prompt[-1] != ' ':
        prompt += ' '

    if confirm_prompt[-1] != ' ':
        confirm_prompt += ' '

    i = 0
    while not confirm_limit or i < confirm_limit:
        pw = getpass(format_ansi(prompt % args))

        if pw:
            if validate is not None and not validate(pw):
                continue

            elif confirm:
                if getpass(format_ansi(confirm_prompt % args)) == pw:
                    return pw
                else:
                    milc.cli.log.error('Passwords do not match!')

            else:
                return pw

            i += 1


def question(prompt, *args, default=None, confirm=False, answer_type=str, validate=None, **kwargs):
    """Allow the user to type in a free-form string to answer.

    | Argument | Description |
    |----------|-------------|
    | prompt | The prompt to present to the user. Can include ANSI and format strings like milc's `cli.echo()`. |
    | default | The value to return when the user doesn't enter any value. Use None to prompt until they enter a value. |
    | confirm | Present the user with a confirmation dialog before accepting their answer. |
    | answer_type | Specify a type function for the answer. Will re-prompt the user if the function raises any errors. Common choices here include int, float, and decimal.Decimal. |
    | validate | This is an optional function that can be used to validate the answer. It should return True or False and have the following signature:<br><br>`def function_name(answer, *args, **kwargs):` |
    """
    if not milc.cli.interactive:
        return default

    if default is not None:
        prompt = '%s [%s] ' % (prompt, default)
    elif prompt and prompt[-1] != ' ':
        prompt += ' '

    while True:
        answer = input(format_ansi(prompt % (args or kwargs)))

        if answer:
            if validate is not None and not validate(answer, *args, **kwargs):
                continue

            elif confirm:
                if yesno('Is the answer "%s" correct?', answer, default=True):
                    try:
                        return answer_type(answer)
                    except Exception as e:
                        milc.cli.log.error('Could not convert answer (%s) to type %s: %s', answer, answer_type.__name__, str(e))

            else:
                try:
                    return answer_type(answer)
                except Exception as e:
                    milc.cli.log.error('Could not convert answer (%s) to type %s: %s', answer, answer_type.__name__, str(e))

        elif default is not None:
            return default


def choice(heading, options, *args, default=None, confirm=False, prompt='Please enter your choice: ', **kwargs):
    """Present the user with a list of options and let them select one.

    Users can enter either the number or the text of their choice. This will return the value of the item they choose, not the numerical index.

    | Argument | Description |
    |----------|-------------|
    | heading | The text to place above the list of options. |
    | options | A sequence of items to choose from. |
    | default | The index of the item to return when the user doesn't enter any value. Use None to prompt until they enter a value. |
    | confirm | When True present the user with a confirmation dialog before accepting their answer. |
    | prompt | The prompt to present to the user. Can include color and format strings like milc's `cli.echo()`. |

    Users can enter either the number or the text of their choice.

    !!! warning
        This will return the value of the item they choose, not the numerical index.
    """
    if not args and kwargs:
        args = kwargs

    if not milc.cli.interactive:
        return default

    if prompt and default is not None:
        prompt = prompt + ' [%s] ' % (default + 1,)
    elif prompt[-1] != ' ':
        prompt += ' '

    while True:
        # Prompt for an answer.
        milc.cli.echo(heading % args)
        for i, option in enumerate(options, 1):
            milc.cli.echo('\t{fg_cyan}%d.{fg_reset} %s', i, option)

        answer = input(format_ansi(prompt))

        # If the user types in one of the options exactly use that
        if answer in options:
            return answer

        # Massage the answer into a valid integer
        if answer == '' and default is not None:
            answer = default
        else:
            try:
                answer = int(answer) - 1
            except Exception as e:
                milc.cli.log.error('Invalid choice: %s', answer)
                milc.cli.log.debug('Could not convert %s to int: %s: %s', answer, e.__class__.__name__, e)
                if milc.cli.config.general.verbose:
                    milc.cli.log.exception(e)
                continue

        # Validate the answer
        if answer >= len(options) or answer < 0:
            milc.cli.log.error('Invalid choice: %s', answer + 1)
            continue

        if confirm and not yesno('Is the answer "%s" correct?', answer + 1, default=True):
            continue

        # Return the answer they chose.
        return options[answer]
