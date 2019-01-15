# Practice kubernetes SKAD 
## Question 1
Create a namespace called `ggckad-s0` in your cluster.
Run the following pods in this namespace.
		1. A pod called pod-a with a single container running the `kubegoldenguide/simple-http-server` image
		2. A pod called pod-b that has one container running the `kubegoldenguide/alpine-spin:1.0.0` image, and one container running `nginx:1.7.9`
Write down the output of `kubectl get pods` for the `ggckad-s0` namespace.

### Solution
Create a `namespace`
```
kubectl create namespace ggckad-s0	
```

Yaml file for the pod-a
``` 
apiVersion: v1
kind: Pod
metadata:
  name: pod-a
  namespace: ggckad-s0
spec:
  containers:
  - image: kubegoldenguide/simple-http-server
    name: container-a
```

Create the pod
```
kubectl create -f pod-a.yaml
```

verify
```
kubectl get pod --namespace  ggckad-s0
NAME    READY   STATUS    RESTARTS   AGE
pod-a   1/1     Running   0          16s
```


##  Question 2
All operations in this question should be performed in the `ggckad-s2` namespace.
Create a ConfigMap called app-config that contains the following two entries:
		1. 'connection_string' set to 'localhost:4096'
		2. 'external_url' set to 'google.com'
Run a pod called question-two-pod with a single container running the `kubegoldenguide/alpine-spin:1.0.0` image, and expose these configuration settings as environment variables inside the container.

### Solution 
Create a `namespace`
```
kubectl create namespace ggckad-s2 
```

Create a `configMap`
```
create configmap app-config --namespace ggckad-s2 --from-literal=connection_string=localhost:4096 --from-literal=external_url=google.com
```

yaml for pod 
```
apiVersion: v1
kind: Pod
metadata:
  name: question-two-pod
  namespace: ggckad-s2
spec:
  containers:
  - image: kubegoldenguide/alpine-spin:1.0.0
    name: container-a
    envFrom:
    - configMapRef:
        name: app-config
```

Create a pod and verify env
```
kubectl create -f question-two-pod.yaml
kubectl exec -ti question-two-pod --namespace ggckad-s2 printenv
HOSTNAME=question-two-pod
external_url=google.com
connection_string=localhost:4096
```


verify `configmap` 

```
kubectl get configmap --namespace ggckad-s2 -o yaml
apiVersion: v1
items:
- apiVersion: v1
  data:
    connection_string: localhost:4096
    external_url: google.com
  kind: ConfigMap
  metadata:
    creationTimestamp: "2019-01-15T06:07:05Z"
    name: app-config
    namespace: ggckad-s2
    resourceVersion: "2937324"
    selfLink: /api/v1/namespaces/ggckad-s2/configmaps/app-config
    uid: c8c9125c-188b-11e9-9149-000c29ec02d2
kind: List
```
