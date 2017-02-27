# ezpwdgen

Is a deterministic offline password generator that creates passwords that are
[easy to remember](https://xkcd.com/936/) by using a master password.

It does this using either the
[EFF word list](https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases)
or the Unicode
[Emoji Annotation keyword database](http://unicode.org/emoji/charts/emoji-annotations.html)
(Currently the Emoji one is hard coded).

This allows you to create unique passwords for various sites with out having to
share the same password and without storing the created passwords.

There are lots of pros and cons to this method. You can google around for that
but my opinion is that it is atleast far superior to the normal behavior of
people reusing passwords.

The algorithim used can easily be examined as it is just a python script. 
The script generates a secure hash (SHA-512 HMAC with 10000 iterations) and from that hash creates integers
which are then used to pick words from the word file (modulas the number of words in the file).

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
                        config file. Use - for stdin.
  -d, --gnupg           Experimental! Use GPG decrypt. Requires python-gnupg
                        module.
  -D, --nognupg         Disable GPG decrypt.
  -p PROFILE, --profile=PROFILE
                        profile
```

## Configuration

The configuration is space/tab delimited file in `~/.config/ezpwdgen/config`.

The format is:

```
# a comment
profile1   password1   optional_wordfile_sha256_checksum   optional_notes1
profile2   password2
```

The profiles basically allow for multiple master passwords.

The third column is the checksum of the word file. Use this if you are concerned
about the word file changing from version to version which would change the
predictability of the passwords.

When you run the command `ezpwdgen.py` if no profile is picked the first one in the config file is picked.

### Using GnuPGP

Some users may want to encrypt their configuration file with GnuPGP. 
While I recommend it `gpg` is nontrival for most.

Currently there are two options:

* Pipe the config file after it has been decrypted using `-c -`
* Use the experimental builtin GPG support with "-d" argument but this requires gpg-agent to be setup properly. 

For the first option there is a wrapping script that makes this easier called `ezpwdgengpg.sh`.
It will expect an encrypted config file in the following location `~/.config/ezpwdgen/config.gpg`

To create this file you can use the command 
`gpg -e -r [Your fingerprint or email] ~/.config/ezpwdgen/config` and then of 
course delete the unencrypted config file.


## Why create another password generator

Well there are lots deterministic password generators but they are either online
or do not use common words to create passwords.

There are also lots of nondeterministic password generators (using the OS secure
random) that create passwords with words but they are nondeterministic (aka no
master password).

There are also many password managers like
[pass](https://www.passwordstore.org/) and [keepass](http://keepass.info/).
While I have great respect for those tools they are more complicated, require
you to synchronize across machines and difficult to share passwords with other
people. Also for some reason many of the password managers still do not generate
easy to remember passwords. Consequently people copy and paste the generated
password over and over. The clipboard is an easy attack vector. Don't use it.

With deterministic password generators you only need to share the master
password and this program (and the words file) with someone else. Consequently
**this password generator is stateless and will never modify or save files!**

Finally (but yet again) this script urges you not to copy and paste passwords.

## What is with the Emoji word database

While I'm sure the EFF database is superior security wise (as well as it can be
used with out a computer) I prefer the passwords generated from the emoji word
database. The emoji annotations also provides a nifty way to potentially help
remember the passwords by showing emojis. Right now the program doesn't do this
but plans are to add this as many terminals (iterm) actually support printing
emojis.

The emoji annotations also allows for some interesting internationalization of
which the EFF database does not provide.

## Hey this site doesn't like long passwords or requires weird characters

You can make up little rules like truncating the password, capitalizing the
first word and suffixing or prefixing with some symbols. That is infact what the
notes section is for in the config file.

Truncating is pretty easy for most HTML forms. Just type the password till you
can't type anymore usually works.

By the way if you use a site that has a limit less than 32 characters for a
password I recommend complaining to them.

## Caveats

* Do not share your master passwords (the passwords in the config file) unless you want to share passwords with that entity.
* Do not share the config file. Store that safely like you would SSH private keys.
* **Do not copy and paste the generated password!** The clipboard on most operating systems is disturbingly insecure.
* Do not use this to create offline passwords. While this method is probably
  fine for online passwords as it is generally fairly difficult to brute force
  online passwords this method is probably not ideal for offline things.
* **I am not a security expert... please send PRs! Use this at your own risk!**
