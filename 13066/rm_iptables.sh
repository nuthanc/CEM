iptables -D DOCKER
iptables -D DOCKER-ISOLATION-STAGE-1 -i docker0 ! -o docker0 -j DOCKER-ISOLATION-STAGE-2
iptables -D DOCKER-ISOLATION-STAGE-1 -j RETURN
iptables -D DOCKER-ISOLATION-STAGE-2 -o docker0 -j DROP
iptables -D DOCKER-ISOLATION-STAGE-2 -j RETURN
iptables -D DOCKER-USER -j RETURN
iptables -D FORWARD -j DOCKER-USER
iptables -D FORWARD -j DOCKER-ISOLATION-STAGE-1
iptables -D FORWARD -i docker0 -o docker0 -j ACCEPT
iptables -D FORWARD -o docker0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
iptables -D FORWARD -i docker0 ! -o docker0 -j ACCEPT
iptables -D  FORWARD -o docker0 -j DOCKER
iptables -X DOCKER-USER
iptables -X DOCKER-ISOLATION-STAGE-1
iptables -X DOCKER-ISOLATION-STAGE-2
iptables -X DOCKER

/sbin/iptables -t nat -A POSTROUTING -o eno1 -j MASQUERADE
/sbin/iptables -A FORWARD -i eno1 -o br1 -m state --state RELATED,ESTABLISHED -j ACCEPT
/sbin/iptables -A FORWARD -i br1 -o eno1 -j ACCEPT
sudo sysctl -w net.ipv4.ip_forward=1
