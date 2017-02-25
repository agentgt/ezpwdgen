*ezpwdgen*

Is a deterministic offline password generator that creates passwords that are easy to remember.

It does this using either the EFF word list or the Unicode Emoji Annotation keyword database.

This allows you to create unique passwords for various sites with out having to share the same password and without storing the created passwords.

There are lots of pros and cons to this method. You can google around for that but my opinion is that it is far superior 
to the normal behavior of people reusing passwords.


The configuration is space/tab delimited file in `~/.config/ezpwdgen/config`.

The format is:

```
profile		password
```


When you run the command ezpwdgen.py if no profile is picked the first one in the config file is picked.
