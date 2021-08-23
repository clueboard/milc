# Breaking Changes

This is a list of breaking changes that have been made to MILC. If your script stops working after a minor or major version upgrade this document will tell you how to fix it.

# Version 1.6.0

* Added support for [Sparklines](sparklines.md)
* Moved documentation to [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
  * Latest release documentation can always be found here: <https://milc.clueboard.co/latest>
  * Latest in development documentation can always be found here: <https://milc.clueboard.co/devel>
  * Legacy docsify documentation for MILC 1.5.0 can be found here: <https://milc.clueboard.co/1.5.0>

# Version 1.5.0

* Added `cli.config_dir` to find the location of the config directory.
* [Arguments](argument_parsing.md#deprecated), [commands](api_milc.md#entrypoint), and [subcommands](api_milc.md#add_subcommand) can now be marked as deprecated.

# Version 1.4.0

* The `config` subcommand now filters out configuration that has not been explicitly set. The new `--all` flag will allow you to see all possible configuration options and their default values.
* Setting program metadata through environment variables has been deprecated. In its place is the new `set_metadata()` function. See [Metadata](metadata.md) for more detail.
* MILC now tracks whether a script is running interactively or not with `cli.interactive`. You can pass `--interactive` to force a script into interactive mode even when stdout is not a TTY. `milc.questions` will always return the default answer when running non-interactively, unless `--yes` or `--no` are passed.

# Version 1.3.0

* You can now set the program version number with `os.environ['MILC_APP_VERSION'] = '1.2.3'`
* New global arguments: --unicode and --no-unicode
* ANSIFormatter, ANSIStrippingFormatter, ANSIEmojiLoglevelFormatter, and ANSIStrippingEmojiLoglevelFormatter have been removed in favor of `format_ansi()` being color aware. The new `MILCFormatter` is being used in its place.

# Version 1.2.0

* The config file is now resolved to the actual file which should avoid overwriting symlinks. <https://github.com/qmk/qmk_cli/issues/43>

# Version 1.1.0

* Configuration: 0 and 1 are now considered integers, not boolean

# Version 1.0.0

Initial Version
