import requests
if __name__=="__main__":
    url="http://yun.chinadream.org:888/paper/check"

    files={ "file" :open("11.jpg", "rb")}
    d = {"limit":6}
    resp=requests.post(url=url,files = files,data=d)
    print(resp.text)