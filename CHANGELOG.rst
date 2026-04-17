Changelog
=========


1.11.0 (2026-04-17)
-------------------
- New release: 1.10.0 → 1.11.0. [Zach White]
- Remove python 3.8 support. [Zach White]
- Fix pygments requirement for 3.8. [Zach White]
- Add uv.lock to bumpversion. [Zach White]
- Add args_passed property to MILCInterface (#87) [Copilot, skullydazed]
- Minor: changelog update. [Zach White]


1.10.0 (2026-03-29)
-------------------
- New release: 1.9.1 → 1.10.0. [Zach White]
- [ci] Updated API documentation. [Zach White]
- Fix multiple bugs found in library review (#2) [Claude Sonnet 4.6,
  Zach White]

  - _sparkline.py: handle all-non-numeric input gracefully (use min/max
    default=None + early return); replace `if spark_int > 7` with min()
    to stay within complexity limit
  - milc.py: fix IndexError when --config-file is last argv token; fix
    spinner() format string crash when called with no args; fix KeyError
    in _handle_deprecated() when help= is omitted; fix __exit__()
    absorbing KeyboardInterrupt (now exits cleanly); correct
    _config_store_true/false type annotations from Sequence to List;
    remove @lru_cache from find_config_file() to prevent self reference leak
  - questions.py: catch EOFError in all input functions (yesno, password,
    _question, choice); fix password() infinite loop when validate always
    returns False
  - subcommand/config.py: fix ValueError on config tokens with multiple =
    signs (split with maxsplit=1); fix KeyError when deleting non-existent
    config option
- Fix LogRecord mutation corrupting multi-handler output in
  MILCFormatter. [Claude Sonnet 4.6, Zach White]

  LogRecord objects are shared across all handlers. MILCFormatter.format()
  was mutating record.levelname in place, causing the second handler (e.g.,
  file handler) to receive an already-modified ANSI/emoji string instead of
  the original level name. Fix by operating on a shallow copy of the record
  so the original is never modified.
- Fix exception safety, format string bug, and type annotation issues
  found in library review (#84) [Copilot, skullydazed]

  * Initial plan

  * Fix _save_config_file exception safety, format string bug in questions, type annotation in sparkline, and typos
- Bump nltk from 3.9.1 to 3.9.4 (#83) [dependabot[bot], dependabot[bot]]

  Bumps [nltk](https://github.com/nltk/nltk) from 3.9.1 to 3.9.4.
  - [Changelog](https://github.com/nltk/nltk/blob/develop/ChangeLog)
  - [Commits](https://github.com/nltk/nltk/compare/3.9.1...3.9.4)

  ---
  updated-dependencies:
  - dependency-name: nltk
    dependency-version: 3.9.4
    dependency-type: indirect
  ...
- Bump tornado from 6.4.2 to 6.5.5 (#82) [dependabot[bot],
  dependabot[bot]]

  Bumps [tornado](https://github.com/tornadoweb/tornado) from 6.4.2 to 6.5.5.
  - [Changelog](https://github.com/tornadoweb/tornado/blob/master/docs/releases.rst)
  - [Commits](https://github.com/tornadoweb/tornado/compare/v6.4.2...v6.5.5)

  ---
  updated-dependencies:
  - dependency-name: tornado
    dependency-version: 6.5.5
    dependency-type: indirect
  ...
- Bump urllib3 from 2.2.3 to 2.6.3 (#80) [dependabot[bot],
  dependabot[bot]]

  Bumps [urllib3](https://github.com/urllib3/urllib3) from 2.2.3 to 2.6.3.
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.2.3...2.6.3)

  ---
  updated-dependencies:
  - dependency-name: urllib3
    dependency-version: 2.6.3
    dependency-type: indirect
  ...
- Bump black from 23.12.1 to 26.3.1 (#79) [dependabot[bot],
  dependabot[bot]]

  Bumps [black](https://github.com/psf/black) from 23.12.1 to 26.3.1.
  - [Release notes](https://github.com/psf/black/releases)
  - [Changelog](https://github.com/psf/black/blob/main/CHANGES.md)
  - [Commits](https://github.com/psf/black/compare/23.12.1...26.3.1)

  ---
  updated-dependencies:
  - dependency-name: black
    dependency-version: 26.3.1
    dependency-type: indirect
  ...
- Bump pymdown-extensions from 10.15 to 10.16.1 (#81) [dependabot[bot],
  dependabot[bot]]

  Bumps [pymdown-extensions](https://github.com/facelessuser/pymdown-extensions) from 10.15 to 10.16.1.
  - [Release notes](https://github.com/facelessuser/pymdown-extensions/releases)
  - [Commits](https://github.com/facelessuser/pymdown-extensions/compare/10.15...10.16.1)

  ---
  updated-dependencies:
  - dependency-name: pymdown-extensions
    dependency-version: 10.16.1
    dependency-type: indirect
  ...
- Track uv.lock for reproducible CI. [Claude Sonnet 4.6, Zach White]

  uv.lock was gitignored, causing setup-uv's cache to never invalidate
  (no matching file for its cache-dependency-glob). Committing it gives
  CI a stable, reproducible dev environment and fixes the cache warning.

  Does not affect downstream users — uv.lock is ignored by pip and only
  used by uv sync during development and CI.
- Remove obsolete Python 3.6 stdin=None workaround. [Claude Sonnet 4.6,
  Zach White]

  Introduced in 30fb0eb to fix a Python 3.6 subprocess.run behavior.
  In Python 3.8+ (now the minimum), stdin=None is identical to omitting
  stdin entirely — both inherit the parent's stdin. Dead code that
  misleads readers into thinking there's a meaningful edge case.
- Fix confirm_prompt ignoring kwargs in password() [Claude Sonnet 4.6,
  Zach White]

  The confirm prompt used args directly, raising TypeError if the caller
  formatted the original prompt with kwargs instead. Mirror the same
  args or kwargs pattern used for the main prompt.
- Initialize spinner_obj to None to prevent potential NameError. [Claude
  Sonnet 4.6, Zach White]

  spinner_obj was only defined inside the if-block, making the
  spinner=spinner_name or spinner_obj expression fragile if spinner_name
  is ever falsy without entering that block.
- Remove unreachable assert in _sparkline.py. [Claude Sonnet 4.6, Zach
  White]

  The assert after the min/max assignments can never be False: min() and
  max() either assign a value or raise ValueError on empty input. Dead code
  that misleads readers into thinking it is a real guard.
- Replace assert with ValueError in handle_store_boolean. [Claude Sonnet
  4.6, Zach White]

  assert is stripped by python -O and gives an unhelpful AssertionError.
  Raises ValueError with a clear message instead, and moves the check before
  add_argument calls so the first flag isn't registered before the error fires.
- Fix broken __exit__ error handling. [Claude Sonnet 4.6, Zach White]

  Four issues in MILC.__exit__:
  - isinstance(SystemExit(), exc_type) is semantically inverted; use issubclass
  - print(exc_type) emits unhelpful class repr with no message
  - logging.exception() outside an except block captures no traceback
  - exit() is a REPL convenience wrapper; use sys.exit()
- Switch AttrDict from UserDict to MutableMapping with private _data
  store. [Claude Sonnet 4.6, Zach White]

  UserDict uses self.data as its backing store, making 'data' a reserved key
  for attribute access — a problem for a CLI library where --data is a likely
  argument name. MutableMapping lets us own the internal store name (_data),
  eliminating the reserved-key hazard entirely.

  Key implementation notes:
  - __contains__ is overridden to check _data directly, bypassing
    MutableMapping's default which calls self[key] and would cause infinite
    recursion in ConfigurationSection.__getitem__
  - __getattr__ delegates to self.__getitem__ (not _data directly) so
    subclass overrides like Configuration's auto-creation are respected
  - ConfigurationSection.__setattr__ simplified: non-_ keys write only to
    _data; _-prefixed internal state goes to object.__setattr__
  - ConfigurationSection.__getattr__ now delegates to __getitem__ rather
    than only checking _parent['user'], fixing attribute access for values
    set via bracket notation
- Rewrite AttrDict using collections.UserDict to fix stale attribute
  bug. [Claude Sonnet 4.6, Zach White]

  __setitem__ was writing keys to both self._data and self.__dict__, but
  __delitem__ only removed from _data, leaving stale values accessible via
  attribute access. Switching to UserDict eliminates the dual-storage pattern
  entirely — UserDict manages its own self.data backing store and provides all
  dict protocol methods, so __getattr__ is the only override needed.

  Also adds test_AttrDict_delete to cover this case.
- Fix Windows CI hang by using stdin pipe instead of DEVNULL. [Claude
  Sonnet 4.6, Zach White]

  On Windows CI with ConPTY, nul device can report isatty()==True, causing
  cli.interactive=True and question loops to hang. Always using input= ensures
  stdin is a real pipe, which never reports isatty()==True on any platform.
- Fix Windows CI hang by closing stdin for subprocess calls. [Claude
  Sonnet 4.6, Zach White]
- Migrate from nose2 to pytest. [Claude Sonnet 4.6, Zach White]
- Fix Windows CI test failures on native Windows runners. [Claude Sonnet
  4.6, Zach White]

  - Scope milc.run() shell wrapping to msys2 only (MSYSTEM env var check),
    since cmd.exe does not support the -c flag used previously
  - Replace cli.run() in test helper with subprocess.run directly, using
    sys.executable so tests always use the correct venv Python
  - Add PYTHONUTF8=1 and encoding='utf-8' for correct Unicode handling
    across all Python versions on Windows
  - Replace '/dev/null' with os.devnull in test_script_example.py
  - Use sys.executable throughout all test_script_* files
- Fixup tests on windows. [Zach White]
- Migrate from mypy to ty for type checking. [Claude Sonnet 4.6, Zach
  White]

  Replace mypy with ty in dev dependencies and ci_tests. Fix all 23
  diagnostics ty surfaces: add TypeGuard to is_number, remove the
  Python-3-era threading try/except, replace mypy-specific
  type: ignore[rule] comments with blanket ignores or proper fixes,
  use getattr for __name__ on Callable types, fix a latent logic bug
  in the subparser metavar ternary, and cast sparkline arithmetic to
  float to avoid mixed-type operator errors.
- Fix windows CI. [Zach White]
- Make the ci_tests automatically fix what it can. [Zach White]
- Ignore N999 for test files. [Claude Sonnet 4.6, Zach White]

  Test files use CamelCase in their names to mirror the class under test
  (e.g. test_configuration_Configuration.py). Suppress the ruff N999
  module-naming violation for tests/**
- Don't commit uv.lock for library package. [Claude Sonnet 4.6, Zach
  White]

  Libraries should resolve fresh against unpinned deps rather than
  pinning to a lockfile. Add uv.lock to .gitignore and drop --frozen
  from CI.
- Migrate to uv for dependency management. [Claude Sonnet 4.6, Zach
  White]

  Replace pip + requirements files with uv. Deps consolidated into
  [dependency-groups] in pyproject.toml (PEP 735). CI workflows updated
  to use astral-sh/setup-uv@v5 with a frozen lockfile. uv.lock committed
  for reproducible installs across all Python/OS matrix combinations.
- Add isort support via ruff I ruleset, fix import ordering. [Claude
  Sonnet 4.6, Zach White]
- Migrate from setup.py/setup.cfg to pyproject.toml, replace flake8 with
  ruff. [Claude Sonnet 4.6, Zach White]

  - Add pyproject.toml with all package metadata, tool config (ruff, yapf, mypy)
  - Delete setup.py; strip setup.cfg to bumpversion sections only
  - Replace flake8 with ruff in requirements-dev.txt and ci_tests
  - Update python-publish.yml to use python -m build instead of setup.py
  - Add build to requirements-release.txt
  - Bump minimum Python from 3.7 (EOL) to 3.8 to match CI reality
- Type _subparsers as Optional[_SubParsersAction] [Claude Sonnet 4.6,
  Zach White]

  Replace Optional[Any] and its FIXME comment with the concrete private
  argparse type, imported under TYPE_CHECKING to avoid runtime coupling.
  Suppress the one index check on the metavar formatting line where mypy
  cannot prove the str invariant that holds at runtime.
- Clarify confirm_limit=0 sentinel in password loop. [Claude Sonnet 4.6,
  Zach White]

  Replace `not confirm_limit` with `confirm_limit == 0` so the intent is
  explicit: 0 means no limit. The previous form would treat any falsy
  value the same way.
- Implement NO_COLOR standard support (#78) [Copilot, skullydazed]

  * Initial plan

  * Implement NO_COLOR standard support (issue #77)
- Update README: Python 3.8+, add venv setup instructions. [Claude
  Sonnet 4.6, Zach White]

  Bump the stated minimum Python version from 3.7 to 3.8 to match the
  CI matrix. Add a dev environment setup block to the Contributing
  section so contributors know to activate their venv before running
  ci_tests.
- Fix mypy errors in handle_store_boolean. [Claude Sonnet 4.6, Zach
  White]

  Add _arg_parser assignment to SubparserWrapper.__init__ so both MILC
  and SubparserWrapper satisfy the union type without the getattr hack.
  Assert disabled_args is not None before unpacking to satisfy the
  variadic argument type check.
- Update CI to Python 3.8-3.14, fix runs-on matrix bug. [Claude Sonnet
  4.6, Zach White]

  Drop EOL 3.7, add 3.14 to the test matrix. Update single-version pins
  in devel_docs and python-publish workflows to 3.14. Fix ci.yml runs-on
  hardcoded to ubuntu-22.04 — it now uses ${{ matrix.os }} so Windows
  jobs actually run on Windows.
- Type handle_store_boolean self param as MILC | SubparserWrapper.
  [Claude Sonnet 4.6, Zach White]

  Replaces the `self: Any` hack with an explicit union type, using a
  TYPE_CHECKING guard to import MILC without introducing a circular import.
- Fix arg deduplication. [Zach White]
- Fix KeyError when SHELL env var is not set on Windows. [Claude Sonnet
  4.6, Zach White]

  Use os.environ.get('SHELL', 'cmd.exe') instead of os.environ['SHELL']
  to avoid crashes on Windows/MSYS2 where SHELL may not be defined.
- Add AI contribution docs. [Zach White]
- More typing (#76) [Pablo Martínez]

  * some more typing improvements

  * make comment more readable, do not leak defaults in `@overload`

  * move `@overload`, try and word the comment better

  * move things around
- Move where spark_int gets cast to int. [Zach White]
- Mypy. [Zach White]
- Fix a divide by zero bug. [Zach White]
- Fix location of typing marker (#75) [Pablo Martínez]
- Bump python version for devel docs job. [Zach White]
- Improve type hint for decorators (#74) [Pablo Martínez]
- Minor: changelog update. [Zach White]


1.9.1 (2025-01-25)
------------------
- New release: 1.9.0 → 1.9.1. [Zach White]
- Let's try 3.10. [Zach White]
- Make cli.echo more robust. [Zach White]
- Move from python 3.7 to latest. [Zach White]
- Fix the `milc.cli.subcommand_name` property value (#73) [Sergey
  Vlasov]

  The implementation of the `subcommand_name` property in `MILCInterface`
  was wrong (it actually returned the `_subcommand` function object
  instead of the subcommand name).
- Mypy. [Zach White]
- Flake8. [Zach White]
- Mypy. [Zach White]
- Style update. [Zach White]
- Properly (I hope) fix CI. [Zach White]
- Style update. [Zach White]
- Fix windows too. [Zach White]
- Style update. [Zach White]
- Update the python version support. [Zach White]
- Minor: changelog update. [Zach White]


1.9.0 (2024-09-24)
------------------
- New release: 1.8.0 → 1.9.0. [Zach White]
- [ci] Updated API documentation. [Zach White]
- Document change to platformdirs. [Zach White]
- Replace deprecated appdirs with platformdirs fork (#72) [Alexandre
  Detiste]
- Add some properties clients are using to MILCInterface. [Zach White]
- Fix typing. [Zach White]
- Preserve name, author, version, and logger in case cli.milc_options()
  is called multiple times. [Zach White]
- Use an interface so we don't have to replace the milc.cli object.
  [Zach White]
- Minor: changelog update. [Zach White]


1.8.0 (2024-02-04)
------------------
- New release: 1.7.0 → 1.8.0. [Zach White]
- [ci] Updated API documentation. [Zach White]
- Update the breaking changes log. [Zach White]
- Improve how custom loggers work. [Zach White]
- Minor updates for setup.py and setup.cfg. [Zach White]
- Bump codeql to v3. [Zach White]
- Minor: changelog update. [Zach White]


1.7.0 (2024-01-29)
------------------
- New release: 1.6.10 → 1.7.0. [Zach White]
- [ci] Updated API documentation. [Zach White]
- Remove unneeded type ignore. [Zach White]
- Fix typing for 3.7. [Zach White]
- Fixup requirements. [Zach White]
- Turn max_complexity down to 12. [Zach White]
- Small doc updates. [Zach White]
- Fix python version. [Zach White]
- Update ci and expand the python versions. [Zach White]
- Increase ci coverage. [Zach White]
- Add type hints to milc (now we'll never have a bug again!) [Zach
  White]
- Make it possible to instantiate MILC directly. [Zach White]
- Minor: changelog update. [Zach White]


1.6.10 (2024-01-27)
-------------------
- New release: 1.6.9 → 1.6.10. [Zach White]
- Switch to api token auth. [Zach White]
- Minor: changelog update. [Zach White]


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


