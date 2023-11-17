ssh-keygen -b 2048 -t rsa -f sshkey -q -N ""
HOME_DIR=$(eval echo "~${TEST_USER}")
SSH_DIR=$HOME_DIR/.ssh
sudo mkdir $SSH_DIR
sudo cp sshkey.pub $SSH_DIR/authorized_keys
sudo chown -R $TEST_USER $SSH_DIR
