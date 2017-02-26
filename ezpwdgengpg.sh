#!/usr/bin/env bash
gpg -q -d ~/.config/ezpwdgen/config.gpg | ./ezpwdgen.py -c - $@
