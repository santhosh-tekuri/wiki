#Docker-Swarm

[Swarm](https://github.com/docker/swarm/) is a Docker-native clustering system. It is a simple tool which controls a cluster of Docker hosts and exposes it as a single virtual host. It uses Standard Docker API as its frontend, so tools like [fig](http://www.fig.sh/) etc, can talk to swarm.

Swarm requires docker daemon version 1.4.0 or above.

##Installation
~~~~
$ apt-get install golang // on mac: brew install go
$ mkdir ~/swarm
$ export GOPATH=~/swarm
$ go get -u github.com/docker/swarm
~~~~

##Discovery
It is a mechanism swarm uses in order to maintain the status of the cluster. 
* it maintains a list of Docker nodes that should be part of the cluster
* health-checks each one and keeps track of the nodes that are in and out of the cluster

Swarm has multiple discovery services.
~~~~
swarm manage -H <listeningIP:listeningPort> <discovery>
~~~~

TLS must be enabled explicitly:
~~~~
--tlsverify --tlscert=<certfile> --tlskey=<keyfile>
~~~~

to enable client authentication:
~~~~
--tlscacert <cacertfile>
~~~~

the remotes should provide certificate signed by the CA given here  
Swarm certificates must be generated with `extendedKeyUsage = clientAuth,serverAuth`. [how?](http://thomaskrehbiel.com/post/how_to_create_and_manage_certificates_with_openssl) [script?](http://technolo-g.com/generate-ssl-for-docker-swarm/)

types of discovery services supported are:
* `<addr1>,<addr2>` static list of ips
* `file://path/to/file`  each line in file is docker host address
* `zk://<addr1>,<addr2>/<path>` zookeeper ensemble
* `consul://<addr1>,<addr2>/path`
* `etcd://<addr1><addr2>/path`
* `token:<token>` hosted token based discovery. use `swarm create` to create token

here `<addr>` means `ip:port`

except static list and file, for remaining you should run swarm agent on each docker host
~~~~
swarm join --addr <ip:port> <discovery>
~~~~

now use docker client with swarm:
~~~~
docker -H <swarmIp:swarmport> ...
~~~~

## Filters

### Port:
As expected, swarm does not any two containers with the same static port mapping to be started on the same host

### Healthy:
As expected, swarm prevents the scheduling of containers on unhealthy nodes

### Constraint:
each docker is started with a set of labels:
~~~~
docker -d \
  --label storage=ssd \
  --label zone=external \
  --label tier=data \
  -H 0.0.0.0:2375
~~~~

few standard set of constraints are available by default.
~~~~
storagedriver
executiondriver
kernelversion
operatingsystem
~~~~
values of these constraints can be seen from `docker info`

while staring container, specify filters to be matched:
~~~~
docker run -d -P \
    -e constraint:storage==ssd \
    -e constraint:zone==external \
    -t nginx
~~~~

### Affinity:
to start mysql on same host where ngnix container running:
~~~~
-e affinity:container==nginx
~~~~

to start container only on a node that already contains the image:
~~~~
-e affinity:image==nginx
~~~~
This negates the need to wait for an image to be pulled in the background before starting a container

## Expression Syntax
~~~~
<key><operator><value>
~~~~

`key`: must conform the alpha-numeric pattern, with the leading alphabet or underscore  
`operator`: `==` or `!=`  
`value`: must be one of following
* An alpha-numeric string, dots, hyphens, and underscores
* A globbing pattern, ex: `abc*`
* A regular expression in the form of `/go-regexp/`
  * `/node[12]/` matches `node1` and `node2`
  * `/node\d/` will match `node` followed by single digit
  * `/foo\[bar\]/` will match `foo[bar]`
  * `/(?i)node1/` will match node `node1` case-insensitive

what about `constrant:node==node1`?

## Strategies
Once Swarm has narrowed the host list down to a set that matches the above filters, it then schedules the container on one of the nodes, using a strategy:
### Random: 
Randomly distribute containers across available backends.
###Binpacking: 
Fill up a node with containers and then move to the next. This mode has the increased complexity of having to assign static resource amounts to each container at runtime. This means setting a limit on a container’s memory and cpu which may or may not seem OK. I personally like letting the containers fight amongst themselves to see who gets the resources. :abcd:

https://www.youtube.com/v/EC25ARhZ5bI

[part1](http://technolo-g.com/intro-to-docker-swarm-pt1-overview/)
[part2](http://technolo-g.com/intro-to-docker-swarm-pt2-config-options-requirements/)
[part3](http://technolo-g.com/intro-to-docker-swarm-pt3-example-architechture/)
