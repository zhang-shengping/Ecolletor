from openstack import connection

def open_con():
    auth_url = "http://10.0.192.18:35357/v3"
    project_name = "shengping-project"
    username = "shengping"
    password = "Passw0rd"
    user_domain_name = "default"
    project_domain_name = "default"
    con = connection.Connection(auth_url=auth_url,
                                 project_name=project_name,
                                 username=username,
                                 password=password,
                                 user_domain_name=user_domain_name,
                                 project_domain_name=project_domain_name
                                 )
    return con
