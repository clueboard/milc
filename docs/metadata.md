# MILC Metadata

There is some information that MILC needs before you import the module. You can set os environment variables to provide this information.

## Version Number

You can set the application's version number with the `MILC_APP_VERSION` environment variable.

    os.environ['MILC_APP_VERSION'] = '1.2.3'

## Application Name and Author Name

You can set the application's name and author name, which are used when determining the configuration file location, with `MILC_APP_NAME` and `MILC_AUTHOR_NAME`.

    os.environ['MILC_APP_NAME'] = 'Florzelbop'
    os.environ['MILC_AUTHOR_NAME'] = 'Jane Doe'
