# Argument (Tab) Completion Support

MILC supports argument completion out of the box using [argcomplete](). Getting argument completion to actually work can be a little fiddly, this page attempts to help you with that.

## Prerequisites

Before argument completion will work your program must be registered with your shell. The most compatible way to do so is this:

    eval "$(register-python-argcomplete my-program)"

If you have a new enough shell (EG bash 4.2 or later, zsh, fish) you can instead rely on [`activate-global-python-argcomplete`](https://github.com/kislyuk/argcomplete#activating-global-completion), but in my experience that mechanism is fragile and easily broken.

## Using Tab Completion

After running the command above you should be able to type the name of your program, type a partial flag name, and tab complete the rest. For many simple programs this is all you need.

## Adding Custom Completions

In some cases you need to give argcomplete a custom list of completions. For example, if you want to complete hostnames out of a configuration file. You can specify this by setting `completer` in your argument decorator. You can use either [callable or readline-style completers](https://kislyuk.github.io/argcomplete/#specifying-completers) when you specify that.

For example, to use an `EnvironCompleter` for an argument:

    def EnvironCompleter(**kwargs):
        return os.environ

    @cli.argument('-e', '--env', completer=EnvironCompleter, help='Environment Variable')
    @cli.entrypoint('My cool program')
    def my_program(cli):
        pass
