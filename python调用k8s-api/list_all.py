import urllib3
import yaml
from kubernetes import client,config
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ListAll:
    def __init__(self,config_file):
        config.load_kube_config(config_file)
        self.api = client.CoreV1Api()
        self.apis = client.AppsV1Api()

    def ListPods(self):
        v1 = self.api
        pod_list = v1.list_namespaced_pod("kube-system")
        for pod in pod_list.items:
            print(f"kube-system namespace Pod is:{pod.metadata.name}")
        return " "

    def ListDep(self):
        v1 = self.apis
        dep_list = v1.list_namespaced_deployment("kube-system")
        for dep in dep_list.items:
            print(f"kube-system namespaces Deployment is:{dep.metadata.name}")
        return " "

    def ListSvc(self):
        v1 = self.api
        svc_list = v1.list_namespaced_service("kube-system")
        for svc in svc_list.items:
            print(f"kube-system namespace Service is:{svc.metadata.name}")
        return " "

if __name__ == "__main__":
    list_m = ListAll(config_file="config")
    pods = list_m.ListPods()
    deps = list_m.ListDep()
    svcs = list_m.ListSvc()
################################## Result ##################################
kube-system namespace Pod is:coredns-78fcd69978-vbm4g
kube-system namespace Pod is:coredns-78fcd69978-vkbzv
kube-system namespace Pod is:etcd-k8s-master-node1
kube-system namespace Pod is:kube-apiserver-k8s-master-node1
kube-system namespace Pod is:kube-controller-manager-k8s-master-node1
kube-system namespace Pod is:kube-flannel-ds-4cv8q
kube-system namespace Pod is:kube-flannel-ds-sh2j9
kube-system namespace Pod is:kube-multus-ds-7b7qc
kube-system namespace Pod is:kube-multus-ds-vpfwq
kube-system namespace Pod is:kube-proxy-5g9ln
kube-system namespace Pod is:kube-proxy-lh8mq
kube-system namespace Pod is:kube-scheduler-k8s-master-node1
kube-system namespace Pod is:metrics-server-77564bc84d-d8dt6
kube-system namespaces Deployment is:coredns
kube-system namespaces Deployment is:metrics-server
kube-system namespace deployment is:kube-dns
kube-system namespace deployment is:metrics-server
