import urllib3
import yaml
from kubernetes import config,client
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class DepManager:
    def __init__(self,config_file):
        config.load_kube_config(config_file)
        self.apis = client.AppsV1Api()

    def CreateDeployment(self,yamlFile):
        with open(yamlFile,encoding='utf8')as f:
            body = yaml.safe_load(f)
        res = self.apis.create_namespaced_deployment(namespace="default",body=body)
        return res

    def GetDep(self):
        v1 = self.apis
        res = v1.read_namespaced_deployment("test","default")
        return res
    
    def delete_dep(self):
        v1 = self.apis
        res = v1.delete_namespaced_deployment("test","default")
        return res
    
if __name__ == "__main__":
    dep_m = DepManager(config_file="config")
    
    create = dep_m.CreateDeployment("nginx-dep.yaml")
    print(f"Create Deployment Successful:{create}")
    
    get = dep_m.GetDep()
    print(f"Get Deployment Successful:{get}")
    res = str(get)
    with open("dep_demo.json","w")as outfile:
        outfile.write(res)
        
    # delete = dep_m.delete_dep()
    # print(f"Delete Deployment Successful:{delete}")


###########
内容太多，都放到dep_demo.json文件中去了
