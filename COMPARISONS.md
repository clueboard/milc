# Comparison with other solutions

Below is a list of the existing tools I have looked at and why I feel they
don't fill the same need as MILC.

Note: This list was compiled in 2018. In 2020 I edited the list to remove
dead projects but I not go searching for new projects. The time for justifying
MILC's existence has passed.

| Name | Argument Parsing | Config File | Logging | Subcommands | Subcommand Config |
|------|------------------|-------------|---------|-------------|-------------------|
| MILC | ✔ | ✔ | ✔ | ✔ | ✔ |
| [Argparse](#Argparse) | ✔ | ✖ | ✖ | ✔ | ✖ |
| ConfigParser | ✖ | ✔ | ✖ | ✔ | ✖ |
| logging | ✖ | ✖ | ✔ | ✖ | ✖ |
| [Cement](#Cement) | ✔ | ✔ | ✔ | ✔ | ✔ |
| [Cliar](#Cliar) | ✔ | ✖ | ✖ | ✔ | ✖ |
| [Click](#Click) | ✔ | ✖ | ✖ | ✔ | ✖ |
| [Clize](#Clize) | ✔ | ✖ | ✖ | ✔ | ✖ |
| [Cogs](#Cogs) | ✔ | ✖ | ✖ | ✔ | ✖ |
| [Defopt](#Defopt) | ✔ | ✖ | ✖ | ✔ | ✖ |
| [Docopt](#Docopt) | ✔ | ✖ | ✖ | ✔ | ✖ |
| [Fire](#Fire) | ✔ | ✖ | ✖ | ✔ | ✖ |
| [Plac](#Plac) | ✔ | ✖ | ✖ | ✔ | ✖ |

### Argparse

The built-in argparse module is amazing- MILC uses it under the hood. Using
it directly as an end-user is complicated and error-prone however. The common
patterns mean you end up putting the definition of CLI arguments in a
different place from the code that uses those arguments.

### Cement

<https://builtoncement.com/>

Cement is a very heavy MVC framework for building CLI tools. It includes all
the functionality MILC provides and then some. If you're looking for an
MVC framework for your tool this is the one to pick.

If you are looking for an MVC framework MILC probably isn't what you want.
Use Cement instead.

### Cliar

<https://moigagoo.github.io/cliar/>

This is an interesting library. The author makes some good points about
magic and DSL's. But it requires you to write a class for your CLI. Classes
are good, but not every tool should be a class.

Cliar does not support a configuration file or logging.

### Click

<https://github.com/pallets/click>

You'd have to be a fool or incredibly sure of yourself to compete against one
of Armin Ronacher's projects. :)

Click is great, and I borrowed the decorator concept from Flask before I saw
Click had done the same thing. It terms of how you use it there are a lot of
similarities between Click and MILC.

Where Click and MILC part ways is in the underlying implementation. MILC
uses the recommended and built-in Python modules whenever possible. Under the
hood MILC is just argparse, logging, ConfigParser, and other standard modules
abstracted just enough to make the right thing easy. Click on the other hand
uses optparser, which has been deprecated in favor of argparser, and handles
a lot of functionality itself rather than dispatching to included Python
modules.

MILC does not insist upon a UTF-8 environment for Python 3 the way Click
does. I understand Click's stance here but I'm hoping that the ecosystem has
developed enough by now to make it no longer necessary. Time will tell if
my opinion changes or not.

Whether you should use Click or MILC depends on the tradeoff you want to
make. Would you rather use the Python modules everyone's already familiar with
or dive into a world of custom code that attempts to make everything cleaner
overall? Do you want one cohesive system or do you want to pull together
disparate plugins and modules to build the functionality you need?

Click does not support a configuration file or logging out of the box, but
there are [plugins](https://github.com/click-contrib) you can get to add this
and other functionality to Click.

### Clize

<https://github.com/epsy/clize>

Clize has a nice approach with lots of mature and advanced functionality.

Clize uses function annotation to work, which may or may not fit with how you
work. It also has a lot of arbitrary restrictions due to annotations, for
example alt functions don't work with argument aliases.

Clize does not support a configuration file or logging.

### Cogs

<https://github.com/prometheusresearch/cogs>

Cogs seems interesting, but has its own dedicated CLI tool named `cogs`. You
don't create scripts directly but instead create Python functions that `cogs`
will call. This is not a paradigm that I want to use.

Cogs does not include config file support.

### defopt

<https://github.com/evanunderscore/defopt>

Defopt is a great tool for turning functions into CLIs. Had I found this
earlier I may not have written MILC at all. But I have written MILC, and
there's some things I'm still not sure about. For example, I don't see a way
to have script handle both subcommand and non-subcommand operation.

Defopt does not support a configuration file or logging.

### docopt

<https://github.com/docopt/docopt>

Docopt has a large following, and some interesting ideas. But if you are
someone who does not like the idea of using comments to define behavior you
will not enjoy working with docopt.

Docopt has poor error handling. You have to do your own argument validation,
and even when Docopt knows the passed arguments are invalid it does not return
a useful error message to the user.

Docopt does not support config files.

### Fire

<https://github.com/google/python-fire>

Fire is an interesting idea- turn any class into a CLI. Unfortunately this
is useful more as a tool for introspection than building a good CLI.

Fire does not support a configuration file or logging.

### Plac

<https://github.com/micheles/plac>

I like his idea about scaling down, and it's part of what drove me. But I
don't want to go without functionality to scale down. MILC's idea of scaling
down is working well for small programs.

Plac does not support a configuration file or logging.
