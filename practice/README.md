# Practice kubernetes SKAD 
## Question 1
Create a namespace called `ggckad-s0` in your cluster.
Run the following pods in this namespace.
		1. A pod called pod-a with a single container running the `kubegoldenguide/simple-http-server` image
		2. A pod called pod-b that has one container running the `kubegoldenguide/alpine-spin:1.0.0` image, and one container running `nginx:1.7.9`
Write down the output of `kubectl get pods` for the `ggckad-s0` namespace.

### Solution
[Communicate Between Containers in the Same Pod Using a Shared Volume - Kubernetes](https://kubernetes.io/docs/tasks/access-application-cluster/communicate-containers-same-pod-shared-volume/)
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
[Configure a Pod to Use a ConfigMap - Kubernetes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/)

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


## Question 3
All operations in this question should be performed in the `ggckad-s2` namespace. Create a pod that has two containers. Both containers should run the `kubegoldenguide/alpine-spin:1.0.0` image. The first container should run as user ID 1000, and the second container with user ID 2000. Both containers should use file system group ID 3000.

### Solution
[Configure a Security Context for a Pod or Container - Kubernetes](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)
verify the namespace exists 
```
kubeclt get namespace ggckad-s2 -o yaml
apiVersion: v1
kind: Namespace
metadata:
  creationTimestamp: "2019-01-15T06:03:41Z"
  name: ggckad-s2
  resourceVersion: "2937014"
  selfLink: /api/v1/namespaces/ggckad-s2
  uid: 4effc8bb-188b-11e9-9149-000c29ec02d2
spec:
  finalizers:
  - kubernetes
```

Yaml file for pod 
```
apiVersion: v1
kind: Pod
metadata:
  name: question-3
  namespace: ggckad-s2
spec:
  securityContext:
    runAsGroup: 3000
  containers:
  - image: kubegoldenguide/alpine-spin:1.0.0
    name: container-a
    securityContext:
      runAsUser: 1000
  - image: kubegoldenguide/alpine-spin:1.0.0
    name: container-b
    securityContext:
      runAsUser: 2000
```

Create a pod with securityContext
```
kubectl create -f question3.yaml
```

## Question 4
All operations in this question should be performed in the `ggckad-s4` namespace. This question will require you to create a pod that runs the image `kubegoldenguide/question-thirteen`. This image is in the main Docker repository at hub.docker.com. 

This image is a web server that has a health endpoint served at '/health' that returns a 200 status code response when the application is healthy. The application typically takes sixty seconds to start. Create a pod called question-four-pod to run this application, making sure to define liveness and readiness probes that use this health endpoint.


### Solution
[Configure Liveness and Readiness Probes - Kubernetes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/)

Create namespace  `ggckad-s4`

```
kubectl create namespace ggckad-s4
```

Yaml file for the pod 
```
apiVersion: v1
kind: Pod
metadata:
  name: question-four
  namespace: ggckad-s4
spec:
  containers:
  - name: liveness-readiness
    image: kubegoldenguide/question-thirteen
    livenessProbe:
      initialDelaySeconds: 16
      periodSeconds: 10
      httpGet:
        path: /health
        port: 80
    readinessProbe:
      httpGet:
        path: /health
        port: 80
```

Create the pod 
```
kubectl create -f liveness.yaml
kubectl get pods --namespace ggckad-s4
NAME            READY   STATUS    RESTARTS   AGE
question-four   0/1     Running   0          31s
```


## Question 5 

A Pod is running on the cluster but it is not responding.
The desired behavior is to have `Kubernetes` restart the pod when an endpoint returns an HTTP 500 on the `/healthz` endpoint. The service, liveness-http, should never send traffic to the Pod while it is failing. Please complete the following:
		1. The application has an endpoint, /started, that will indicate if it can accept traffic by returning an HTTP 200. If the endpoint returns an HTTP 500, the application has not yet finished initialization
		2. The application has another endpoint `/healthz` that will indicate if the application is still working as expected by returning an HTTP 200. If the endpoint returns an HTTP 500 the application is no longer responsive
		3. Configure the liveness-http Pod provided to use these endpoints
		4. The probes should use port 8080


