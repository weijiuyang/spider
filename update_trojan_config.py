import requests
import base64
import json

# Trojan配置文件路径
config_path = "/etc/trojan/config.json"

# 订阅链接
subscription_url = "https://knmvc.site/ND2J7/Dg2qi"

# 获取订阅内容
response = requests.get(subscription_url)
if response.status_code != 200:
    raise Exception("Failed to fetch subscription link")

# 解码Base64内容
decoded_data = base64.b64decode(response.text).decode("utf-8")
servers = decoded_data.splitlines()

print(servers)
# 解析订阅内容
server_list = []
for server in servers:
    if server.startswith("trojan://"):
        parts = server[9:].split("@")
        password = parts[0]
        server_info = parts[1].split(":")
        address = server_info[0]
        port = int(server_info[1].split("?")[0])
        # 解析其他参数
        params = server_info[1].split("?")[1]
        param_dict = {p.split("=")[0]: p.split("=")[1] for p in params.split("&")}
        peer = param_dict.get("peer", "")
        sni = param_dict.get("sni", "")
        allow_insecure = param_dict.get("allowInsecure", "0") == "1"
        server_list.append({
            "remote_addr": address,
            "remote_port": port,
            "password": password,
            "peer": peer,
            "sni": sni,
            "allow_insecure": allow_insecure
        })

print(server_list)
for one in server_list:
    print(one['remote_addr'], one['remote_port'], one['password'])
# 创建新的Trojan配置文件内容
trojan_config = {
    "run_type": "client",
    "local_addr": "0.0.0.0",
    "local_port": 1080,
    "remote_addr": server_list[0]["remote_addr"],  # 默认使用第一个服务器作为主服务器
    "remote_port": server_list[0]["remote_port"],  # 默认使用第一个服务器作为主服务器
    "password": [server["password"] for server in server_list],  # 添加所有服务器的密码
    "log_level": 1,
    "ssl": {
        "verify": True,
        "verify_hostname": True,
        "peer": server_list[0]["peer"],
        "sni": server_list[0]["sni"],
        "allow_insecure": server_list[0]["allow_insecure"],
        "cipher": "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384",
        "cipher_tls13": "TLS_AES_128_GCM_SHA256:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_256_GCM_SHA384",
        "prefer_server_cipher": True,
        "alpn": ["http/1.1"],
        "reuse_session": True,
        "session_ticket": False,
        "session_timeout": 600,
        "plain_http_response": "",
        "curves": ""
    },
    "tcp": {
        "prefer_ipv4": False,
        "no_delay": True,
        "keep_alive": True,
        "reuse_port": False,
        "fast_open": False,
        "fast_open_qlen": 20
    },
    "mux": {
        "enabled": False,
        "concurrency": 8,
        "idle_timeout": 60
    },
    "router": {
        "enabled": False,
        "bypass": [],
        "proxy": [],
        "block": [],
        "default_policy": "proxy",
        "domain_strategy": "as_is",
        "geoip": "/usr/share/trojan/geoip.dat",
        "geosite": "/usr/share/trojan/geosite.dat"
    },
    "websocket": {
        "enabled": False,
        "path": "",
        "host": ""
    },
    "shadowsocks": {
        "enabled": True,
        "method": "",
        "password": ""
    },
    "transport_plugin": {
        "enabled": False,
        "type": "",
        "command": "",
        "plugin_option": "",
        "arg": [],
        "env": []
    },
    "forward_proxy": {
        "enabled": False,
        "proxy_addr": "",
        "proxy_port": 0,
        "username": "",
        "password": ""
    },
    "mysql": {
        "enabled": False,
        "server_addr": "",
        "server_port": 3306,
        "database": "",
        "username": "",
        "password": "",
        "cafile": ""
    }
}

# 将新配置写入文件
with open(config_path, 'w') as config_file:
    json.dump(trojan_config, config_file, indent=4)

print("Trojan configuration updated successfully.")
