# Kubernetes CKA Class First class
#kubernetes-cka
 

# Create a namespaces
To get all namespaces and manage it follow the steps 
``` 
kubectl  get namespaces
kubectl create namespace  bakulya

```

![](README/Screen%20Shot%202018-12-02%20at%2010.22.44%20AM.png)


# Node 
To get all nodes and see on yaml versions follow the steps. If you would like to get `json` version just change `yaml` to `json`.

```
kubectl get nodes
kubectl get nodes fs-secondnode
kubectl get nodes fs-secondnode -o yaml
```
![](README/Screen%20Shot%202018-12-02%20at%2010.27.02%20AM.png)

# Run the pods or create a pod.
Pods are groups of containers. We will create a pod and get to inside the pods (container)
```
kubectl get pods
kubectl run -i -t centos --image=centos
```
![](README/Screen%20Shot%202018-12-02%20at%2010.30.16%20AM.png)

## Log in to the pod 
In this example we log out from pod and then log in back to pods. 
```
exit
kubectl get pods # to get name of the pod
kubectl attach -i -t centos-7474788896-gt78z
```

![](README/Screen%20Shot%202018-12-02%20at%2010.34.33%20AM.png)
# Understanding the ephemeral on pod(containers)
Whenever you log in to pod or container if you create or modified something. It will deleted and reverted back by default  version. Example follow the steps 

```
kubectl get pods
kubectl attach -i -t centos-7474788896-gt78z
yum install net-tools -y 
ifconfig
exit
# when ever we exit kubernteds will recreate the pod
kubectl attach -i -t centos-7474788896-gt78z
ifconfig # result bash: ifconfig: command not found
```
Get list of pods and log in to pod then install the net tools.
![](README/Screen%20Shot%202018-12-02%20at%2010.41.28%20AM.png)
Make sure ifconfig is installed and exited 
![](README/Screen%20Shot%202018-12-02%20at%2010.41.43%20AM.png)
Log in back to the pod and try to run `ifconfig` 
![](README/Screen%20Shot%202018-12-02%20at%2010.42.16%20AM.png)

# Create pod from yaml file.
We will create a pod call centos  from yaml file. Example file looks like this
```
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: centos
  name: centos-pod
spec:
  containers:
  - image: centos
    name: centos
    stdin: true
    tty: true
```

Now we can create a pod running command 
`kubectl apply -f centos.yaml`

# Scheduling the pods per nodes 
In this example we will create a pod on one of our nodes. Our pod will run on node `fs-node`
```
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: centos
  name: centos-pod
spec:
  nodeSelector:
    kubernetes.io/hostname: fs-node
  containers:
  - image: centos
    name: centos
    stdin: true
    tty: true
```

