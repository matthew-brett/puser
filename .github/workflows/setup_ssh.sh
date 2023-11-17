ssh-keygen -b 2048 -t rsa -f sshkey -q -N ""
HOME_DIR=$(eval echo "~${TEST_USER}")
SSH_DIR=$HOME_DIR/.ssh
sudo mkdir $SSH_DIR
sudo cp sshkey.pub $SSH_DIR/authorized_keys
TEST_GROUP=$(id -gn $TEST_USER)
sudo chown -R ${TEST_USER}:${TEST_GROUP} $SSH_DIR
if [ "$RUNNER_OS" == "macOS" ]; then
    sudo /usr/sbin/dseditgroup -o edit -a ${TEST_USER} -t user com.apple.access_ssh
fi
