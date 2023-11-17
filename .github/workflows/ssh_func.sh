function ssh_user {
    ssh -o StrictHostKeyChecking=no -i sshkey $TEST_USER@localhost ${SHELL_NAME} -c $@
}
