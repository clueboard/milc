Changelog
=========


1.6.9 (2024-01-27)
------------------
- New release: 1.6.8 → 1.6.9. [Zach White]
- [ci] Updated API documentation. [Zach White]
- Document custom loggers. [Zach White]
- Add the ability to pass custom loggers. [Zach White]
- Publish docs before the python package. [Zach White]
- Minor: changelog update. [Zach White]


1.6.8 (2023-06-13)
------------------
- New release: 1.6.7 → 1.6.8. [Zach White]
- Minor: changelog update. [Zach White]


1.6.7 (2023-06-13)
------------------
- New release: 1.6.6 → 1.6.7. [Zach White]
- [ci] Updated API documentation. [Zach White]
- Upgrade all workflow versions. [Zach White]
- Upgrade workflows. [Zach White]
- Remove the trivial change. [Zach White]
- Fix the python version specification. [Zach White]
- Trivial change to kick off ci. [Zach White]
- Update to codeql 2. [Zach White]
- Remove python 3.6, add 3.10. [Zach White]
- Fix test. [Zach White]
- Fix during-initialization logging. [Zach White]
- Fix whitespace. [Zach White]
- Handle '--config-file=CONFIG_FILE' syntax (#66) [Ken Bingham, Zach
  White]

  * handle --config-file=CONFIG_FILE syntax

  * Update milc/milc.py
- Minor: changelog update. [Zach White]


1.6.6 (2022-03-27)
------------------
- New release: 1.6.5 → 1.6.6. [Zach White]
- [ci] Updated API documentation. [Zach White]
- Support --foo=bar options. Fixes #65. [Zach White]
- Fix the metadata documentation. [Zach White]
- Minor: changelog update. [Zach White]


1.6.5 (2021-09-19)
------------------
- New release: 1.6.4 → 1.6.5. [Zach White]
- Fix a bug in cli.config_source. [Zach White]

  Before this change arguments that weren't passed were incorrectly marked
  as `argument` instead of None.
- Minor: changelog update. [Zach White]


1.6.4 (2021-09-19)
------------------
- New release: 1.6.3 → 1.6.4. [Zach White]
- Change cli.echo to display ansi in passed vars too. [Zach White]
- Minor: changelog update. [Zach White]


1.6.3 (2021-09-04)
------------------
- New release: 1.6.2 → 1.6.3. [Zach White]
- [ci] Updated API documentation. [Zach White]
- More robust detection for passed arguments (#44) [Zach White]
- Minor: changelog update. [Zach White]


1.6.2 (2021-08-23)
------------------
- New release: 1.6.1 → 1.6.2. [Zach White]
- Add the ability to highlight values below a threshold (#43) [Zach
  White]

  * add support for high and low thresholds

  * update sparklines documentation

  * update the sparkline api docs
- Minor: changelog update. [Zach White]


1.6.1 (2021-08-23)
------------------
- New release: 1.6.0 → 1.6.1. [Zach White]
- [ci] Updated API documentation. [Zach White]
- Change highlight_color to threshold_color before anyone starts using
  it. [Zach White]
- Fix test. [Zach White]
- Change highlight_color to threshold_color before anyone starts using
  it. [Zach White]
- Fix the fetch depth for python-publish. [Zach White]
- Minor: changelog update. [Zach White]


1.6.0 (2021-08-23)
------------------
- New release: 1.5.0 → 1.6.0. [Zach White]
- [ci] Updated API documentation. [Zach White]
- Fix indent. [Zach White]
- Remove vestiges of docsify. [Zach White]
- Update old link. [Zach White]
- Add breaking changes for 1.6.0. [Zach White]
- Go back to working fetch-depth. [Zach White]
- Fix the name for ref and fetch-depth. [Zach White]
- Change the git strategy. [Zach White]
- Put fetch_depth under width. [Zach White]
- Fetch_depth: 0 so that we have gh-pages. [Zach White]
- Adjust paths for triggering workflows. [Zach White]
- Configure git. [Zach White]
- Switch our documentation to mkdocs material (#42) [Zach White]

  * initial version of docs using mkdocs material

  * tweak the visual look

  * CSS tweaks

  * remove _summar

  * font tweak

  * update README to reflect mkdocs

  * workflows to update documentation

  * add site to .gitignore
- Support for displaying sparklines (#41) [Zach White]

  * Add support for displaying sparklines

  * regenerate api docs

  * tweak the script docstring

  * improve corner case handling

  * improve and document whitespace

  * Add the ability to color sparklines to indicate positive and negative numbers

  * add the ability to highlight values over a particular threshold

  * add unit tests for sparkline

  * fix a bug found by the unit tests

  * generate docs

  * clarify int vs number

  * add sparklines to the TOC
- Regenerate changelog. [Zach White]
- Minor: changelog update. [Zach White]


1.5.0 (2021-08-10)
------------------

New
~~~
- Add release changelog. [Zach White]
- Add a cli.config_dir. [Zach White]
- Add deprecation to arguments and commands (#39) [Fyrebright]
- Perform CodeQL analysis on all PRs. [Zach White]

Fix
~~~
- Fix `choice()` default handling (#40) [Ryan]

Other
~~~~~
- New release: 1.4.2 → 1.5.0. [Zach White]
- [ci] Updated API documentation. [Zach White]
- Add 1.5.0 to breaking changes. [Zach White]
- Minor: update docs. [Zach White]


1.4.2 (2021-05-27)
------------------
- New release: 1.4.1 → 1.4.2. [Zach White]
- [ci] Updated API documentation. [Zach White]
- Make the config subcommand more resiliant. [Zach White]
- Make questions more robust. [Zach White]
- Fix how we use stdin on python 3.6. [Zach White]
- Remove the milc.questions unit tests. [Zach White]

  It would be better if these were in place, but they don't work in github
  actions (reproducable locally with `ci-tests | cat`) and we have
  coverage of the same code in the test_script_question.py integration
  test.
- Fix one last test for windows. [Zach White]
- Improve our log_file check. [Zach White]
- Use a tempfile for testing --log-file. [Zach White]

  Turns out that /dev/stdout doesn't work on windows. Use a tempfile
  instead so that our CI tests work on all platforms.
- Improve ci tests for windows. [Zach White]
- Ci: show result.stdout/stderr when an assertion fails. [Zach White]
- Move the comparisons to its own file. [Zach White]


1.4.1 (2021-05-24)
------------------
- New release: 1.4.0 → 1.4.1. [Zach White]
- Setup: add missing dependencies (#36) [francisco souza, francisco
  souza]

  * setup: add missing dependencies

  Alternatively, we could make setup.py read from requirements.txt for
  dependencies.

  IMO, a better option is to always keep setup.py up-to-date with
  library dependencies and add `-e .` to requirements-dev.txt.

  * Add -e . to requirements.txt
- Fix the author logic to match 1.3.0 (#37) [Zach White]
- Ensure ci_tests actually fail. [Zach White]


1.4.0 (2021-05-23)
------------------
- New release: 1.3.0 → 1.4.0. [Zach White]
- Improve the docs in preparation for 1.4.0. [Zach White]
- Update docs. [Zach White]
- Work around a bug with input on windows (#34) [Zach White]
- Add support for securely collecting passwords. (#32) [Zach White]

  * Only ask questions if we are an interactive process

  * add tests for the question script

  * add a breaking changes entry

  * typo

  * first pass at implementing #1

  * Second pass

  * make flake8 happy

  * get the tests working correctly
- Basic spinner support (#33) [Erovia <Erovia@users.noreply.github.com>
  Co-authored-by: Erovia <Erovia@users.noreply.github.com>, Zach White]

  * basic spinner support

  * update readme

  * add a spinner for QMK

  * Apply suggestions from code review
- Only ask questions if we are an interactive process (#30) [Zach White]

  * Only ask questions if we are an interactive process

  * add tests for the question script

  * tweak color

  * add a breaking changes entry

  * typo

  * make ci happy
- Allow config values to be set by attribute (#31) [Zach White]
- Eliminate the need to use environment variables for metadata (#29)
  [Zach White]

  * Eliminate the need to use environment variables for metadata

  * properly handle dashes in subcommands

  * correctly handle subcommands and arguments with dashes

  * fix automatic app name detection

  * add a warning about importing set_metadata and cli

  * update docs

  * yapf

  * fix the description for config --all
- Improve the config command (#28) [Zach White]

  * The config command now filters out configuration that has not been set

  * tweak

  * remove print

  * typo

  * sort the config before printing it
- Script to show the available ANSI colors. [Zach White]


1.3.0 (2021-03-28)
------------------
- New release: 1.2.1 → 1.3.0. [Zach White]
- [ci] Updated API documentation. [Zach White]
- Add argcomplete to the summary. [Zach White]
- Flesh out the argcomplete support. [Zach White]
- Support for setting the version number. [Zach White]

  fixes #14
- Overhaul how ansi/unicode are supported. [Zach White]

  fixes #26
- Misc cleanups. [Zach White]


1.2.1 (2021-03-28)
------------------
- New release: 1.2.0 → 1.2.1. [Zach White]
- Update python-publish.yml. [Zach White]
- Create python-publish.yml. [Zach White]
- Improve generate_docs. [Zach White]

  We now automatically update the _summary.md and commit changes if requested.


1.2.0 (2021-03-24)
------------------
- New release: 1.1.0 → 1.2.0. [Zach White]
- Document the new version 1.2.0. [Zach White]
- Adjust ci_tests. [Zach White]
- Bump supported python versions. [Zach White]
- Change the order of tests. [Zach White]
- Resolve config file paths. [Zach White]
- Add more integration tests. [Zach White]
- Fix handling of store_boolean (#25) [Joel Challis]


1.1.0 (2021-01-23)
------------------
- New release: 1.0.13 → 1.1.0. [Zach White]


1.0.13 (2021-01-23)
-------------------
- New release: 1.0.12 → 1.0.13. [Zach White]
- Add breaking changes. [Zach White]
- Add the ability to bump major and minor versions too. [Zach White]
- Improve default value handling (#24) [Zach White]

  * improve default value handling

  * small optimization


1.0.12 (2021-01-02)
-------------------
- New release: 1.0.11 → 1.0.12. [Zach White]
- Generated API documentation. [Zach White]
- Add version parameter to constructor. [Zed Chance]


1.0.11 (2021-01-02)
-------------------
- New release: 1.0.10 → 1.0.11. [Zach White]
- Don't pass both universal_newlines and text. [Zach White]


1.0.10 (2020-10-25)
-------------------
- New release: 1.0.9 → 1.0.10. [skullY]
- Generated API documentation. [skullY]
- Fix cli.print_help() and cli.print_usage() [skullY]


1.0.9 (2020-10-22)
------------------
- New release: 1.0.8 → 1.0.9. [skullY]
- Generated API documentation. [skullY]
- Don't install tests together with package. [s-ol]
- Questions.yesno: always add a y/n prompt (#19) [Zach White]
- Typo fix. [skullY]
- Improve cli.run docs. [skullY]
- Document and improve cli.run. [skullY]


1.0.8 (2020-10-07)
------------------
- New release: 1.0.7 → 1.0.8. [skullY]
- Update API docs. [skullY]
- Add pydoc-markdown to requirements-release.txt. [skullY]
- Make yapf happy. [skullY]
- Temporarily import format_ansi for qmk. [skullY]
- Improve log file handling. Add tests. (#17) [Zach White]
- Generated API documentation. [skullY]
- Improve ANSI support and --no-color (#16) [Zach White]

  * support --no-color for cli.echo and support emojis when --no-color is used

  * tweak when levelname gets stripped of ansi
- Add --log-file-level option to set file loggging level from CLI.
  [Cédric Tissières]
- Set logging level for file accordingly to console level. [Cédric
  Tissières]


1.0.7 (2020-04-29)
------------------
- New release: 1.0.6 → 1.0.7. [skullY]
- Enable space in config values. fixes #10. [skullY]


1.0.6 (2020-04-29)
------------------
- New release: 1.0.5 → 1.0.6. [skullY]
- Generated API documentation. [skullY]
- Add the ability to selectively save config options. [skullY]


1.0.5 (2020-04-29)
------------------
- New release: 1.0.4 → 1.0.5. [skullY]
- Fix the get_argument_name call. fixes #7. [skullY]


1.0.4 (2020-04-15)
------------------
- New release: 1.0.3 → 1.0.4. [skullY]
- Make arg_only subcommand specific. [skullY]
- Fix setting config values for store_true and store_false. [skullY]


1.0.3 (2020-03-30)
------------------
- New release: 1.0.2 → 1.0.3. [skullY]
- Generated API documentation. [skullY]
- Fix configuration handling. [Erovia]
- Cleanup a couple QMK references. [skullY]
- Add tests for milc.questions. [skullY]
- Add tests for milc.configuration. [skullY]
- Add a test for milc.ansi. [skullY]
- Add tests for milc/__init__.py. [skullY]
- Install dev requirements from requirements-dev.txt. [skullY]
- Write some tests for attrdict. [skullY]


1.0.2 (2020-03-24)
------------------
- New release: 1.0.1 → 1.0.2. [skullY]
- Fix typos and selling mistakes. [skullY]
- Add EMOJI_LOGLEVELS to the main milc module. [skullY]


1.0.1 (2020-03-24)
------------------
- New release: 1.0.0 → 1.0.1. [skullY]
- Do not check docs if no changes. [skullY]
- More release fixing. [skullY]
- Fix doc generation. [skullY]
- Fixup the release script. [skullY]
- Enhance the ci test. [skullY]
- Add missing quotes. [skullY]
- Fix the release script. [skullY]
- Temporarily put requirements.txt back. [skullY]


1.0.0 (2020-03-24)
------------------
- Release infrastructure. [skullY]
- Add some documentation to the scripts. [skullY]
- Add a contributing section. [skullY]
- Enhance the workflows. [skullY]
- Add windows and caching to CI. [skullY]
- Add missing addirs. [skullY]
- Setup CI. [skullydazed]
- Add a script to run ci tests. [skullY]
- Yapf. [skullY]
- Add generated api docs. [skullY]
- Clean up the sidebar. [skullY]
- Yapfify. [skullY]
- Add flake8 and yapf configs. [skullY]
- Remove the link. [skullY]
- Make the question.md formatting nicer. [skullY]
- Remove qmk references. [skullY]
- Fix the chart. [skullY]
- Add some missing docs. [skullY]
- Polish some rough edges. [skullY]
- Print->cli.echo. [skullY]
- Remove unused getting_started.md. [skullY]
- Fix up the examples in the tutorial. [skullY]
- Update the example in the tutorial. [skullY]
- Add note about cli.config.general. [skullY]
- Add backtics around None. [skullY]
- Add configuration to the sidebar. [skullY]
- Document configuration, make cli.args an attrdict. [skullY]
- Create CNAME. [skullydazed]
- Delete CNAME. [skullydazed]
- Create CNAME. [skullydazed]
- Disable jekyll. [skullY]
- Flesh out the MILC documentation. [skullY]
- Allow programs to override app_name and app_author. [skullY]
- Rearrange the docs and add docsify. [skullY]
- Break milc up into pieces. [skullY]
- Sync with qmk_firmware and fix a couple bugs. [skullY]
- Cleanup. [skullY]
- Update screenshots. [skullY]
- Refactor the API to require descriptions. [skullY]
- Cleanup a bit and add some documentation. [skullY]
- Add cli.print() [skullY]
- Cleanup for first github push. [skullY]
- Add a flake8 config and fixup flake8 errors. [skullY]
- Add a .gitignore. [skullY]
- Add support for store_boolean arguments. [skullY]
- Add support for reading and writing config files. [skullY]
- Add spinner support. [skullY]
- Fix a typo. [skullY]
- Make the printed log level output colored icons instead of text.
  [skullY]
- Add ANSI support to CLIM. [skullY]
- Minor tweak. [skullY]
- Add an RLock for thread safety. [skullY]
- Add support for both printed and file logs. [skullY]
- Flesh out the module's docstring. [skullY]
- Strip whitespace. [skullY]
- Add a documentation stub. [skullY]
- Add argument decorator, flesh out docs. [skullY]
- Small cleanup. [skullY]
- Barebones skeleton for the qmk cli. [skullY]


