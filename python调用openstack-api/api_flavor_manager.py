import requests,json,time

def get_auth_token(controller_ip,domain,name,password):
    try:
        url = f"http://{controller_ip}:5000/v3/auth/tokens"
        body = {
            "auth": {
                "identity": {
                    "methods": ['password'],
                    "password": {
                        "user": {
                            "domain": {"name": domain},
                            "name": name,
                            "password": password,
                        }
                    }
                },
                "scope": {
                    "project": {
                        "domain": {"name": domain},
                        "name": name,
                    }
                }
            }
        }
        headers = {
            "Content-Type": "application/json"
        }
        token = requests.post(url,headers=headers,data=json.dumps(body)).headers['X-Subject-Token']
        headers = {
            "X-Auth-Token": token
        }
        print(f"token:{token}")
        return headers
    except Exception as e:
        print(f"token error:{e}")

class flavor_manager:
    def __init__(self,handers:dict,resUrl):
        self.headers = handers
        self.resUrl = resUrl

    def create_flavor(self,name,ram,disk,vcpus,id):
        body = {
            "flavor": {
                "name": name,
                "ram": ram,
                "disk": disk,
                "vcpus": vcpus,
                "id": id
            }
        }
        req = requests.post(self.resUrl,headers=self.headers,data=json.dumps(body)).text
        return req

    def get_flavor_id(self,name):
        req = json.loads(requests.get(self.resUrl,headers=self.headers).text)
        for flavor in req['flavors']:
            if flavor['name'] == name:
                return flavor['id']
        return "NONE"

    def get_flavor(self,id):
        url = self.resUrl + "/" + id
        req = requests.get(url,headers=self.headers)
        result = json.loads(req.text)
        return result

    def delete_flavor(self,id:str):
        api_url = self.resUrl + "/" + id
        req = requests.delete(api_url,headers=self.headers)
        print(req.status_code)
        if req.status_code == 202:
            return {"Delte Flavor is Successful",req.status_code}



if __name__ == "__main__":
    controller_ip = "172.128.130.165"
    domain = "demo"
    name = "admin"
    password = "000000"
    headers = get_auth_token(controller_ip,domain,name,password)

    flavor_m = flavor_manager(headers,f"http://{controller_ip}:8774/v2.1/flavors")

    #create
    create_flavor = flavor_m.create_flavor("nova-flavor","1024","10","2","9999")
    print(f"create flavor is:{create_flavor}")

    # id
    id = flavor_m.get_flavor_id("nova-flavor")

    #get
    get_flavor = flavor_m.get_flavor(id)
    print(f"get flavor is:{get_flavor}")
    with open("flavor_demo.json","w")as outfile:
        json.dump(get_flavor,outfile,indent=4)

    # delete flavor
    # delete_flavor =flavor_m.delete_flavor(id)
    # print(f"delete flavor is:{delete_flavor}"


#1. 使用Python语言，基于OpenStack APIs，封装flavor_manager 的Python类，实现OpenStack云主机类型管理的增、删、查，以json格式返回操作结果，完成后提交实现代码文件。
################################# Respone ################################3
create flavor is:{"flavor": {"links": [{"href": "http://172.128.130.165:8774/v2.1/flavors/9999", "rel": "self"}, {"href": "http://172.128.130.165:8774/flavors/9999", "rel": "bookmark"}], "ram": 1024, "OS-FLV-DISABLED:disabled": false, "os-flavor-access:is_public": true, "rxtx_factor": 1.0, "disk": 10, "id": "9999", "name": "nova-flavor", "vcpus": 2, "swap": "", "OS-FLV-EXT-DATA:ephemeral": 0}}

get flavor is:{'flavor': {'links': [{'href': 'http://172.128.130.165:8774/v2.1/flavors/9999', 'rel': 'self'}, {'href': 'http://172.128.130.165:8774/flavors/9999', 'rel': 'bookmark'}], 'ram': 1024, 'OS-FLV-DISABLED:disabled': False, 'os-flavor-access:is_public': True, 'rxtx_factor': 1.0, 'disk': 10, 'id': '9999', 'name': 'nova-flavor', 'vcpus': 2, 'swap': '', 'OS-FLV-EXT-DATA:ephemeral': 0}}
