import requests,json,time

def get_auth_token(controller_ip,domain_name,username,password):
    try:
        url = f"http://{controller_ip}:5000/v3/auth/tokens"
        body = {
            "auth": {
                "identity": {
                    "methods": ['password'],
                    "password": {
                        "user": {
                            "domain": {"name": domain_name},
                            "name": username,
                            "password": password
                        }
                    }
                },
                "scope": {
                    "project": {
                        "domain": {"name": domain_name},
                        "name": username,
                    }
                }
            }
        }
        headers = {
            "Content-Type": "application/json"
        }
        tokens = requests.post(url,headers=headers,data=json.dumps(body)).headers['X-Subject-Token']
        headers = {
            "X-Auth-Token": tokens
        }
        print(f"get token:{tokens}")
        return headers
    except Exception as e:
        print(f"token err:{e}")

class ServerManager:
    def __init__(self,headers,url):
        self.headers = headers
        self.url = url

    def CreateServer(self,server_name,imageId,flavorId,networkId):
        body = {
            "server": {
                "name": server_name,
                "imageRef": imageId,
                "flavorRef": flavorId,
                "networks": [{
                    "uuid": networkId
                }]
            }
        }
        req = json.loads(requests.post(self.url,headers=self.headers,data=json.dumps(body)).text)
        return req

    def GetServerId(self,server_name):
        req = json.loads(requests.get(self.url,headers=self.headers).text)
        for server in req['servers']:
            if server['name'] == server_name:
                return server['id']
            return "NONE"

    def GetServer(self,id):
        url = self.url + "/" + id
        req = json.loads(requests.get(url,headers=self.headers).text)
        return req

    def DeleteServer(self,id):
        url = self.url + "/" + id
        req = requests.delete(url,self.headers)
        return req.text

if __name__ == "__main__":
    controller_ip = "172.128.130.165"
    domain_name = "demo"
    username = "admin"
    password = "000000"
    headers = get_auth_token(controller_ip, domain_name, username, password)
    server_m = ServerManager(headers,f"http://{controller_ip}:8774/v2.1/servers")

    create_s = server_m.CreateServer("server001","2200ae31-df6b-4323-b450-77ba2c0dc528","9999","6bbfadac-d938-4540-ba2e-052fd03bf895")
    print(f"Create Cloud Server Successful:{create_s}")
    time.sleep(10)

    id = server_m.GetServerId("server001")

    get_s = server_m.GetServer(id)
    print(f"Get Server is:{get_s}")
    with open("server_demo.json","w")as outfile:
        json.dump(get_s,outfile,indent=4)

    # delete_s = server_m.DeleteServer(id)
    # print(f"Delete Server is:{delete_s}")



#使用Python语言，基于OpenStack APIs，封装server_manager 的Python类，实现OpenStack主机管理的增、删、查、，以json格式返回操作结果，完成后提交实现代码文件

################################## Respone ########################################
Create Cloud Server Successful:{'server': {'security_groups': [{'name': 'default'}], 'OS-DCF:diskConfig': 'MANUAL', 'id': 'c458802e-4ce1-4cba-a572-4e4ea57ac23e', 'links': [{'href': 'http://172.128.130.165:8774/v2.1/servers/c458802e-4ce1-4cba-a572-4e4ea57ac23e', 'rel': 'self'}, {'href': 'http://172.128.130.165:8774/servers/c458802e-4ce1-4cba-a572-4e4ea57ac23e', 'rel': 'bookmark'}], 'adminPass': 'rqQnm8cSLPQt'}}

Get Server is:{'server': {'OS-EXT-STS:task_state': None, 'addresses': {'network': [{'OS-EXT-IPS-MAC:mac_addr': 'fa:16:3e:22:48:46', 'version': 4, 'addr': '10.10.24.43', 'OS-EXT-IPS:type': 'fixed'}]}, 'links': [{'href': 'http://172.128.130.165:8774/v2.1/servers/c458802e-4ce1-4cba-a572-4e4ea57ac23e', 'rel': 'self'}, {'href': 'http://172.128.130.165:8774/servers/c458802e-4ce1-4cba-a572-4e4ea57ac23e', 'rel': 'bookmark'}], 'image': {'id': '2200ae31-df6b-4323-b450-77ba2c0dc528', 'links': [{'href': 'http://172.128.130.165:8774/images/2200ae31-df6b-4323-b450-77ba2c0dc528', 'rel': 'bookmark'}]}, 'OS-EXT-STS:vm_state': 'active', 'OS-EXT-SRV-ATTR:instance_name': 'instance-00000002', 'OS-SRV-USG:launched_at': '2022-08-06T06:11:54.000000', 'flavor': {'id': '9999', 'links': [{'href': 'http://172.128.130.165:8774/flavors/9999', 'rel': 'bookmark'}]}, 'id': 'c458802e-4ce1-4cba-a572-4e4ea57ac23e', 'security_groups': [{'name': 'default'}], 'user_id': '2f1261804deb4bb082d9f93c56630e0c', 'OS-DCF:diskConfig': 'MANUAL', 'accessIPv4': '', 'accessIPv6': '', 'progress': 0, 'OS-EXT-STS:power_state': 1, 'OS-EXT-AZ:availability_zone': 'nova', 'config_drive': '', 'status': 'ACTIVE', 'updated': '2022-08-06T06:11:54Z', 'hostId': 'a8ef451ad4b9bc26261c1aebdb011a7119e7354fa8cecae29de7cbb4', 'OS-EXT-SRV-ATTR:host': 'compute', 'OS-SRV-USG:terminated_at': None, 'key_name': None, 'OS-EXT-SRV-ATTR:hypervisor_hostname': 'compute', 'name': 'server001', 'created': '2022-08-06T06:11:48Z', 'tenant_id': '9c1b973da53a4446aa8bb720c41a2fb0', 'os-extended-volumes:volumes_attached': [], 'metadata': {}}}
