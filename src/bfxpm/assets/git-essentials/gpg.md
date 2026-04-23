gpg --full-generate-key
gpg (GnuPG) 2.4.7; Copyright (C) 2024 g10 Code GmbH
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Please select what kind of key you want:
   (1) RSA and RSA
   (2) DSA and Elgamal
   (3) DSA (sign only)
   (4) RSA (sign only)
   (9) ECC (sign and encrypt) *default*
  (10) ECC (sign only)
  (14) Existing key from card
Your selection? 9
Please select which elliptic curve you want:
   (1) Curve 25519 *default*
   (4) NIST P-384
   (6) Brainpool P-256
Your selection? 1
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0) 0
Key does not expire at all
Is this correct? (y/N) y

GnuPG needs to construct a user ID to identify your key.

Real name: Jyotirmoy Das
Email address: jyotirmoy21@gmail.com
Comment: JD_GPG_KEY
You selected this USER-ID:
    "Jyotirmoy Das (JD_GPG_KEY) <jyotirmoy21@gmail.com>"

Change (N)ame, (C)omment, (E)mail or (O)kay/(Q)uit? O
We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.
We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.
gpg: revocation certificate stored as '/Users/jyoda68/.gnupg/openpgp-revocs.d/FAD2CF2493ED9626E3A209FBB83D2B03966FDC17.rev'
public and secret key created and signed.

pub   ed25519 2024-12-10 [SC]
      FAD2CF2493ED9626E3A209FBB83D2B03966FDC17
uid                      Jyotirmoy Das (JD_GPG_KEY) <jyotirmoy21@gmail.com>
sub   cv25519 2024-12-10 [E]

jyoda68@mac00563 ClustScanR % 


To anybody who is facing this issue on MacOS machines, try this:

brew uninstall gpg
brew install gpg2
brew install pinentry-mac (if needed)
gpg --full-generate-key Create a key by using an algorithm.
Get generated key by executing: gpg --list-keys
Set the key here git config --global user.signingkey <Key from your list>
git config --global gpg.program $(which gpg)
git config --global commit.gpgsign true
If you want to export your Key to GitHub then: gpg --armor --export <key> and add this key to GitHub at GPG keys: https://github.com/settings/keys (with START and END line included)
If the issue still exists:

test -r ~/.bash_profile && echo 'export GPG_TTY=$(tty)' >> ~/.bash_profile

echo 'export GPG_TTY=$(tty)' >> ~/.profile

If the issue still exists:

Install https://gpgtools.org and sign the key that you used by pressing Sign from the menu bar: Key->Sign

If the issue still exists:

Go to: ‎⁨your global .gitconfig file which in my case is at: ‎⁨/Users/gent/.gitconfig And modify the .gitconfig file (please make sure Email and Name are the same with the one that you have created while generating the Key):

[user]
    email = gent@youremail.com
    name = Gent
    signingkey = <YOURKEY>
[gpg]
    program = /usr/local/bin/gpg
[commit]
    gpsign = true
    gpgsign = true
[filter "lfs"]
    process = git-lfs filter-process
    required = true
    clean = git-lfs clean -- %f
    smudge = git-lfs smudge -- %f
[credential]
    helper = osxkeychain



jyotirmoy@z6g4:ShinyWGCNA$ gpg --list-keys
gpg: checking the trustdb
gpg: marginals needed: 3  completes needed: 1  trust model: pgp
gpg: depth: 0  valid:   1  signed:   0  trust: 0-, 0q, 0n, 0m, 0f, 1u
/home/jyotirmoy/.gnupg/pubring.kbx
----------------------------------
pub   rsa4096 2024-12-10 [SC]
      6C54098DC7AD2007C11E12CA23AA67160F4D76F2
uid           [ultimate] Jyotirmoy Das (JD_ubuntu_GPG) <jyotirmoy21@gmail.com>
sub   rsa4096 2024-12-10 [E]


export GPG_TTY=$(tty)

gpg --full-generate-key
gpg --list-keys
git config --global user.signingkey 312102971BD581B0F7B256BA8C2734E0D368E004
git config --global gpg.program $(which gpg)
git config --global commit.gpgsign true
git remote -v
git add .
git commit -S -m "updated"
git push