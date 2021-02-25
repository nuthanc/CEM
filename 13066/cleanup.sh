set -x
nohup juju destroy-model default --force -y &
tail -f nohup.out
