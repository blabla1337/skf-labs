#/bin/bash

adduser --disabled-password -u 1004 --gecos "" anne
echo 'anne:AqRtZ123!' | chpasswd
echo "anne ALL=(ALL) NOPASSWD: /usr/bin/vim" >> /etc/sudoers