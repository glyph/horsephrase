# Horsephrase

Horsephrase is a human-readable password generator.

[XKCD makes some good points about password entropy](http://xkcd.com/936/), and
I thought I'd create a tool to help follow that advice.  It has been updated
somewhat from the XKCD strip's guidance.  For example, "a thousand guesses per
second" is an extremely low number; `horsephrase` instead assumes attackers can
perform a trillion guesses per second.

## When To Use Horsephrase

For as many of your passwords as possible, you do *not* want to try to
creatively, or randomly, come up with new ones.  You cannot possibly remember
all the passwords a normal person needs to use. You should be using a password
manager, such as [Dashlane](https://www.dashlane.com),
[LastPass](https://lastpass.com), [KeePass](http://keepass.info) or
[1Password](https://agilebits.com/onepassword).

For *most* of your passwords, you should just be using your password manager's
"generate" function to generate passwords which are long, totally random line
noise that you could not possibly remember and could not easily communicate
without copying and pasting.

However, ultimately you need a *few* passwords you can remember and possibly
pronounce:

1. an unlock code for your phone, which you have to type in
2. a login password for your local computer
3. a master password for that password manager
4. WiFi passwords which need to be frequently shared via analog means, since
   the device they're being typed into isn't on the network yet
5. the password to certain online accounts, such as app stores, which may be
   necessary to access new devices or get access to the account that lets you
   install your password manager of choice onto a device.

For *these* passwords, `horsephrase` can come in handy.

## How To Use Horsephrase

You can generate a new password by simply typing:

```console
$ horsephrase generate
```

at a command prompt.

You can customize `horsephrase` a little by supplying your own word list and
choosing how many words to use; see `horsephrase --help` for details.  To
estimate how long it would take an attacker to guess, if they could guess a
trillion times a second, based on your current word list and word count, you
can use the `estimate` command instead, and it will print out a human-readable
time interval where an attacker will have guessed your password.  You should
probably rotate your password significantly more often than this, since your
passwords can be compromised in ways other than simply guessing.  The default
configuration of `horsephrase` should be good enough that you don't need to
tweak it much:

```console
$ horsephrase estimate
116 years, 20 weeks, 1 day, 21 hours, 13 minutes, and 30 seconds
```

## Technical Note

Just so you know, `horsephrase` uses Python's `SystemRandom` API, which pulls
entropy from `/dev/urandom`, which is
[the correct way to do it](http://sockpuppet.org/blog/2014/02/25/safely-generate-random-numbers/).
