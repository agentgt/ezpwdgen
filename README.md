# ezpwdgen

Is a deterministic offline password generator that creates passwords that are [easy to remember](https://xkcd.com/936/).

It does this using either the [EFF word list](https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases) or the Unicode [Emoji Annotation keyword database](http://unicode.org/emoji/charts/emoji-annotations.html).

This allows you to create unique passwords for various sites with out having to share the same password and without storing the created passwords.

There are lots of pros and cons to this method. You can google around for that but my opinion is that it is atleast far superior to the normal behavior of people reusing passwords.

## Requirements

Python 2.7 and a Unix-like OS (macOS and Linux). I haven't tested on Windows and it probably doesn't work.

## Usage

```
Usage: ezpwdgen.py [options] user@domain

Options:
  -h, --help            show this help message and exit
  -i ITERATION, --iteration=ITERATION
                        iteration
  -c CONFIG, --config=CONFIG
                        config file
  -p PROFILE, --profile=PROFILE
                        profile
```

## Configuration

The configuration is space/tab delimited file in `~/.config/ezpwdgen/config`.

The format is:

```
profile1		password1
profile2    password2
```

The profiles basically allow for multiple passwords.



When you run the command `ezpwdgen.py` if no profile is picked the first one in the config file is picked.

## Why create another password generator

Well there are lots deterministic password generators but they are either online or do not use common words to create passwords.

There are also lots of nondeterministic password generators (using the OS secure random) that create passwords with words but they are nondeterministic (aka no master password).

## Caveat

**I am not a security expert... please send PRs! Use this at your own risk!**

Do not use this to create offline passwords. While this method is probably fine for online passwords as it is generally fairly difficult to brute force online passwords this method is probably not ideal for offline things.
