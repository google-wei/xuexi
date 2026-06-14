import random
from kubernetes import client,config,watch

config.load_kube_config("config")
v1 = client.CoreV1Api()

def nodes_avai():
    ready_nodes = []
    for node in v1.list_node().items:
        for status in node.status.conditions:
            if status.status == "True" and status.type == "Ready":
                ready_nodes.append(node.metadata.name)
    return ready_nodes

def scheduler(name,node,namespace="default"):
    target = client.V1ObjectReference()
    target.kind = "Node"
    target.api_version = "v1"
    target.name = node

    meta = client.V1ObjectMeta()
    meta.name = name
    body = client.V1Binding(target=target)
    body.target = target
    body.metadata = meta
    try:
        v1.create_namespaced_binding(namespace, body)
        return True
    except Exception as e:
        print(f"err:{e}")
        return False
def main():
    w = watch.Watch()
    print(f"available nodes is :{nodes_avai()}")
    for event in w.stream(v1.list_namespaced_pod,"default"):
        if event['object'].status.phase == "Pending" and event['object'].spec.node_name == None:
            try:
                print(f"Start Pending pod Scheduler:",event['object'].metadata.name)
                print("Start Scheduler")
                res = scheduler(event['object'].metadata.name,random.choice(nodes_avai()))
                print("Choice Nodes:",random.choice(nodes_avai()))
                print(f"Successful Scheduler")
                return True
            except Exception as e:
                print(f"Error:{e}")
if __name__ == "__main__":
    main()


############################################## 结果为 ##############################
Start Pending pod Scheduler: nginx-pod
Start Schedulererr:Invalid value for `target`, must not be `None`
Choice Nodes: k8s-master-node1
