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

class ImageManager:
    def __init__(self,headers,url):
        self.headers = headers
        self.url = url

    def CreateImage(self,name,disk_format,container_format):
        body = {
            "name": name,
            "disk_format": disk_format,
            "container_format": container_format
        }
        req = json.loads(requests.post(self.url,headers=self.headers,data=json.dumps(body)).text)
        return req

    def GetImageId(self,name):
        images = json.loads(requests.get(self.url,headers=self.headers).text)
        for img in images['images']:
            if img['name'] == name:
                return img['id']
            return "NONE"

    def UploadImage(self,id,image_file):
        url = self.url + "/" + id + "/file"
        self.headers["Content-Type"] = "application/octet-stream"
        req = requests.put(url, headers=self.headers, data=open(image_file, 'rb').read())
        return req

    def GetImage(self,id):
        url = self.url + "/" + id
        req = json.loads(requests.get(url,headers=self.headers).text)
        return req

    def DeleteImage(self,id):
        url = self.url + "/" + id
        req = requests.delete(url,headers=self.headers)
        if req.status_code == 204:
            return {"Delte Image Successful:",req.status_code}

if __name__ == "__main__":
    controller_ip = "172.128.130.165"
    domain_name = "demo"
    username = "admin"
    password = "000000"
    headers = get_auth_token(controller_ip,domain_name,username,password)
    image_m = ImageManager(headers,f"http://{controller_ip}:9292/v2/images")

    create_im = image_m.CreateImage("cirros0001","qcow2","bare")
    print(f"Create Image Successful:{create_im}")

    id = image_m.GetImageId("cirros0001")
    print(f"ImageId is:{id}")

    upload_im = image_m.UploadImage(id,"./cirros-0.3.4-x86_64-disk.img")
    print(f"Upload Status:{upload_im}")

    get_im = image_m.GetImage(id)
    print(f"Images is:{get_im}")
    with open("image_demo.json","w") as outfile:
        json.dump(get_im,outfile,indent=4)

    # delete_im = image_m.DeleteImage(id)
    # print(f"Delete Image Successful:{delete_im}")



#使用Python语言，基于OpenStack APIs，编写镜像管理程序，实现所有镜像查询与创建和删除，完成后提交实现代码文件。

################################### Respone ###########################################
python3 api_image_manager.py 
get token:gAAAAABi7gNBXOSUv-i9u-vylAMNfoG_qxB01S-efAPn_scCf7ETRGRWlokZnyvz5YpiaEfSwW-rEkAUkgEmQ3jPNT092BLrFxUjC6l6c4HmVqatf83I60TNP3if0LvWLyhpqFU1kMY0kVMDA1Ie0BDA0vA3PvyWg39cErT_mj2HOpOhPnCBmP4
Create Image Successful:{'container_format': 'bare', 'min_ram': 0, 'updated_at': '2022-08-06T05:59:30Z', 'file': '/v2/images/2200ae31-df6b-4323-b450-77ba2c0dc528/file', 'owner': '9c1b973da53a4446aa8bb720c41a2fb0', 'id': '2200ae31-df6b-4323-b450-77ba2c0dc528', 'size': None, 'self': '/v2/images/2200ae31-df6b-4323-b450-77ba2c0dc528', 'disk_format': 'qcow2', 'os_hash_algo': None, 'schema': '/v2/schemas/image', 'status': 'queued', 'tags': [], 'visibility': 'shared', 'min_disk': 0, 'virtual_size': None, 'name': 'cirros0001', 'checksum': None, 'created_at': '2022-08-06T05:59:30Z', 'os_hidden': False, 'protected': False, 'os_hash_value': None}

ImageId is:2200ae31-df6b-4323-b450-77ba2c0dc528

Upload Status:<Response [204]>

Images is:{'container_format': 'bare', 'min_ram': 0, 'updated_at': '2022-08-06T05:59:30Z', 'file': '/v2/images/2200ae31-df6b-4323-b450-77ba2c0dc528/file', 'owner': '9c1b973da53a4446aa8bb720c41a2fb0', 'id': '2200ae31-df6b-4323-b450-77ba2c0dc528', 'size': 13287936, 'self': '/v2/images/2200ae31-df6b-4323-b450-77ba2c0dc528', 'disk_format': 'qcow2', 'os_hash_algo': 'sha512', 'schema': '/v2/schemas/image', 'status': 'active', 'tags': [], 'visibility': 'shared', 'min_disk': 0, 'virtual_size': None, 'name': 'cirros0001', 'checksum': 'ee1eca47dc88f4879d8a229cc70a07c6', 'created_at': '2022-08-06T05:59:30Z', 'os_hidden': False, 'protected': False, 'os_hash_value': '1b03ca1bc3fafe448b90583c12f367949f8b0e665685979d95b004e48574b953316799e23240f4f739d1b5eb4c4ca24d38fdc6f4f9d8247a2bc64db25d6bbdb2'}
