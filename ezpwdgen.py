#!/usr/bin/env python
import base64
import re
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

suffix = '@!1'
#wordfile= EffWordDB('eff_short_wordlist_2_0.txt')
wordfile= WordDB('emoji/emoji-words-2017-02-v4.txt')

def generate(master_password, domain, n):
    password = base64.b64encode(pbkdf2_hmac('sha256',  master_password + '/' + domain, b'', 100000+n, dklen=16))[0:16].decode() + suffix
    return password

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
    return { 'words': words, 'pwd': ''.join(words).capitalize() + suffix, 'iteration': n }

def generateWords(profile, domain, iterations):
    for n in iterations:
        print str(generateWord(profile.password, domain, n))

def bytes_to_int(bytes):
      return int(bytes.encode('hex'), 16)


def run():
    home = expanduser("~")
    parser = OptionParser(usage="usage: %prog [options] user@domain")
    # parser.add_option("-d", "--domain",
    #                   action="store", dest="domain",
    #                   help="domain")

    parser.add_option("-i", "--iteration", action="store", dest="iteration", default='1-3',
                      help="iteration")
    parser.add_option("-c", "--config", action="store", dest="config", default=home + '/.config/ezpwdgen/config',
                      help="config file")
    parser.add_option("-p", "--profile", action="store", dest="profile",
                      help="profile")


    options, args = parser.parse_args()
    if (not args):
        parser.error("domain argument required")

    if (not re.match('[^ ]+@.+\\..+', args[0])):
        parser.error("domain should be in user@domain.com format")

    config = open(options.config).readlines()
    profiles = {}
    defaultProfile = None
    for line in config:
        p = re.split('\s+', line.strip())
        if len(p) < 2:
            parser.error("Profile is malformed in " + options.config)
        profile = Profile(p[0].strip(), p[1].strip())
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
        + "\n\tconfig file: " + options.config \
        + "\n\tprofile: " + profile.profile \
        + "\n\tdomain: " + args[0] \
        + "\n\titeration(s): " + str(options.iteration) 

    s = options.iteration.split('-')
    its = range(int(s[0]), int(s[-1]) + 1)
    generateWords(profile, args[0], its)

if __name__ == "__main__":
    run()

