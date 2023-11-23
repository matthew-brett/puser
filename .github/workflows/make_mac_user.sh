#!/bin/sh
if [ $# -lt 2 ];then
    echo "Need at least username and userid"
    echo "e.g. $(basename $0) auser 504 20 \"Example user\""
    echo "Show users / ids with"
    echo "dscacheutil -q user | grep -A 3 -B 2 -e uid:\ 5'[0-9][0-9]'"
    # https://apple.stackexchange.com/questions/29874/how-can-i-list-all-user-accounts-in-the-terminal#29877
    exit 1
fi
username=$1
userid=$2
usergroup=${3:-20}
userfullname=$4
echo $username, $userid, $usergroup, $userfullname

. /etc/rc.common
dscl . create /Users/$username
dscl . create /Users/$username RealName "$userfullname"
dscl . create /Users/$username UniqueID $userid
dscl . create /Users/$username PrimaryGroupID $usergroup
dscl . create /Users/$username UserShell /bin/bash
dscl . create /Users/$username NFSHomeDirectory /Users/$username
cp -R /System/Library/User\ Template/English.lproj /Users/$username
chown -R $username:staff /Users/$username
# Give ssh access: https://superuser.com/a/958774
sudo dseditgroup -o edit -t user -a $username com.apple.access_ssh

