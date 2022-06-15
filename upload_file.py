import paramiko

def upload_file(host, user, password, localpath, remotepath):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print('Connecting to: {} ..'.format(host))
    ssh_client.connect(hostname=host, username=user, password=password)
    sftp_client = ssh_client.open_sftp()
    sftp_client.put(localpath, remotepath)
