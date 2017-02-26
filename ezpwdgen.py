#!/usr/bin/env python
import base64
import re
import imp
import sys
import os.path
from hashlib import pbkdf2_hmac
from optparse import OptionParser
from os.path import expanduser

class WordDB:
    def __init__(self, wordfile):
        self.filename = wordfile
        f = open(wordfile, 'r')
        self.lines = f.readlines()

    def getWord(self,i):
        return self.lines[i].strip()

    def __len__(self):
        return len(self.lines)

class EffWordDB(WordDB):
    def getWord(self,i):
        return re.split('\W+', self.lines[i])[1].strip()

class Profile:
    def __init__(self, profile, password):
        self.profile = profile
        self.password = password

notes = 'capitalize_and_suffix_with_@!1'
#wordfile= EffWordDB('eff_short_wordlist_2_0.txt')
wordfile= WordDB('emoji/emoji-words-2017-02-v4.txt')

def generateWord(master_password, domain, n):
    size = len(wordfile)
    #for x in range (0,4):
    nwords = 4
    data = pbkdf2_hmac('sha512',  master_password + '/' + domain, b'', 100000+n, dklen=nwords * 4)
    words = []
    for x in range(0,nwords):
        bs = data[x*4:((x+1)*4)]
        index = bytes_to_int(bs) % size
        word = wordfile.getWord(index)
        words.append(word)
    return { 'words': words,  'iteration': n }

def generateWords(profile, domain, iterations):
    for n in iterations:
        print str(generateWord(profile.password, domain, n))

def bytes_to_int(bytes):
      return int(bytes.encode('hex'), 16)

def decryptConfig(fname):
    print "Using gnupg to decrypt config"
    import gnupg
    crypt = gnupg.GPG(verbose=False, use_agent=True).decrypt_file(fname)
    if not crypt.ok:
        raise Exception(crypt.status + " ... HINT: gpg-agent needs to be working.")
    return str(crypt).split('\n')
 
def run():
    home = expanduser("~")
    parser = OptionParser(usage="usage: %prog [options] user@domain")
    # parser.add_option("-d", "--domain",
    #                   action="store", dest="domain",
    #                   help="domain")

    defaultConfig = home + '/.config/ezpwdgen/config'
    parser.add_option("-i", "--iteration", action="store", dest="iteration", default='1-3',
                      help="Iteration. Maybe a range with '-'. Default is 1-3.")
    parser.add_option("-c", "--config", action="store", dest="config", default=defaultConfig,
                      help="config file. Use - for stdin.")
    parser.add_option("-d", "--gnupg", action="store_true", dest="gpg", 
                      help="Experimental! Use GPG decrypt. Requires python-gnupg module.")
    parser.add_option("-D", "--nognupg", action="store_true", dest="disableGpg",
                      help="Disable GPG decrypt.")
    parser.add_option("-p", "--profile", action="store", dest="profile",
                      help="profile")


    options, args = parser.parse_args()
    if (not args):
        parser.error("domain argument required")

    if (not re.match('[^ ]+@.+\\..+', args[0])):
        parser.error("domain should be in user@domain.com format")

    hasGPG = False
    try:
        imp.find_module('gnupg')
        hasGPG = True
    except ImportError:
        hasGPG = False

    useGPG = False
    if options.config == "-":
        configFile = "-"
        useGPG = False
    # elif not options.disableGpg and os.path.isfile(options.config + ".gpg"):
    #     print "Found gpg encrypted config file."
    #     configFile = options.config + ".gpg"
    #     useGPG = True 
    else:
        configFile = options.config
        useGPG = not options.disableGpg and options.gpg

    if hasGPG and useGPG:
        config = decryptConfig(open(configFile,'rb'))
    elif not hasGPG and useGPG:
        parser.error("python-gnupg is not installed")
    else:
        if configFile == "-":
            stream = sys.stdin
        else:
            stream = open(configFile)
        config = stream.readlines()

    profiles = {}
    defaultProfile = None
    lineno = 0
    for line in config:
        lineno += 1
        cleanline = line.split('#')[0].strip()
        if not cleanline: continue
        p = re.split('\s+', cleanline)
        if len(p) < 2:
            parser.error("Profile is malformed in " + configFile + " on line: " + str(lineno))
        profile = Profile(p[0].strip(), p[1].strip())
        if (len(p) > 2):
            profile.notes = p[2]
        else:
            profile.notes = notes
        if not defaultProfile: defaultProfile = profile
        profiles[p[0]] = profile
    profile = None

    if options.profile and not profiles.has_key(options.profile):
        parser.error("Cannot find profile: " + options.profile)
    elif options.profile:
        profile = profiles[options.profile]
    else:
        profile = defaultProfile
    if not profile:
        parser.error("No profiles found in config")

    if not profile.password:
        parser.error("Profile malformed")

    print "Creating password with" \
        + "\n\tconfig file: " + configFile \
        + "\n\tprofile: " + profile.profile \
        + "\n\tdomain: " + args[0] \
        + "\n\tnotes: " + profile.notes \
        + "\n\titeration(s): " + str(options.iteration) 

    s = options.iteration.split('-')
    its = range(int(s[0]), int(s[-1]) + 1)
    generateWords(profile, args[0], its)
    print "Remember the password. Do not use copy and paste!"

if __name__ == "__main__":
    run()

