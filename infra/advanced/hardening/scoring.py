#Requirements pip3 install mysql-connector-python paramiko
import ftplib
import mysql.connector
import requests
import time
import paramiko
from mysql.connector import Error, errors
from paramiko.ssh_exception import NoValidConnectionsError

penalty_points = {}

def check_anonymous_access(host, port=21, timeout=10):
    ftp = ftplib.FTP(timeout=timeout)
    try:
        ftp.connect(host, port)
        ftp.login()
        #print(f"{host}: Anonymous access allowed.")
        return False
    except ftplib.error_perm as e:
        #print(f"{host}: Anonymous access denied. ")
        return True
    except TimeoutError:
        #print(f"{host}: FTP connection timed out.")
        return False
    finally:
        if ftp.sock:
            ftp.quit()

def check_mysql_connection(host, user, password, timeout=10):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host,
            user="wordpress",
            password="String001",
            database="wordpress",
            connection_timeout=timeout,
        )
        #print(f"{host}: MySQL connection successful.")
        return False
    except Error as e:
        if isinstance(e, errors.InterfaceError):
            return False
            #print(f"{host}: MySQL server not found or not running.")
        elif isinstance(e, errors.ProgrammingError):
            return False
            #print(f"{host}: MySQL user, password, or database is incorrect.")
        else:
            return False
            #print(f"{host}: MySQL connection failed.")
            #print("Error details:", e)
    finally:
        if connection and connection.is_connected():
            connection.close()

def check_https(url, timeout=10):
    try:
        response = requests.get(url, timeout=timeout)
        if response.url.startswith("https://"):
            #print(f"{url}: HTTPS enabled.")
            return True
        else:
            #print(f"{url}: HTTPS not enabled.")
            return False
    except requests.exceptions.RequestException as e:
       #print(f"{url}: Failed to connect.")
        return False

def check_sudo_vim_permission(host, timeout=10):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, username="anne", password="AqRtZ123!", timeout=timeout)
        stdin, stdout, stderr = ssh.exec_command(f"sudo -l | grep '(ALL) NOPASSWD: /usr/bin/vim'", get_pty=True)
        output = stdout.read().decode('utf-8').strip()

        if output:
            #print(f"{host}: anne has sudo rights for vim.")
            return False
        else:
            #print(f"{host}: anne does not have sudo rights for vim.")
            return True
    except paramiko.SSHException as e:
        #print(f"{host}: SSH connection failed.")
        return False
    except NoValidConnectionsError as e:
        #print(f"{host}: No valid SSH connections. Check host details and ensure the SSH server is running.")
        return False
    except TimeoutError:
        #print(f"{host}: SSH connection timed out.")
        return False
    finally:
        ssh.close()

def check_ssh_file_exists(host, username, password, filepath='/var/www/html/tracker.php', timeout=10):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, username=username, password=password, timeout=timeout)
        stdin, stdout, stderr = ssh.exec_command(f"test -f {filepath} && echo 'File exists' || echo 'File not found'")
        output = stdout.read().decode('utf-8').strip()
        if output == 'File exists':
            #print(f"{host}: {filepath} exists.")
            return False
        else:
            #print(f"{host}: {filepath} not found.")
            return True
    except paramiko.SSHException as e:
        #print(f"{host}: SSH connection failed.")
        return False
    except NoValidConnectionsError as e:
        #print(f"{host}: No valid SSH connections. Check host details and ensure the SSH server is running.")
        return False
    except TimeoutError:
        #print(f"{host}: SSH connection timed out.")
        return False
    finally:
        ssh.close()

def check_modsecurity_installed(host, username, password, timeout=10):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, username=username, password=password, timeout=timeout)
        stdin, stdout, stderr = ssh.exec_command("apache2ctl -M | grep 'security2_module'")
        output = stdout.read().decode('utf-8').strip()

        if output:
            #print(f"{host}: ModSecurity is installed.")
            return True
        else:
            #print(f"{host}: ModSecurity is not installed.")
            return False
    except paramiko.SSHException as e:
        #print(f"{host}: SSH connection failed.")
        return False
    except NoValidConnectionsError as e:
        #print(f"{host}: No valid SSH connections. Check host details and ensure the SSH server is running.")
        return False
    except TimeoutError:
        #print(f"{host}: SSH connection timed out.")
        return False
    finally:
        ssh.close()

def check_admin_cronjob(host, username, password, cronjob_path="persistance.sh", timeout=10):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, username=username, password=password, timeout=timeout)
        stdin, stdout, stderr = ssh.exec_command(f"crontab -l | grep '{cronjob_path}'")
        output = stdout.read().decode('utf-8').strip()

        if output:
            #print(f"{host}: admin has a cronjob running {cronjob_path}.")
            return False
        else:
            #print(f"{host}: admin does not have a cronjob running {cronjob_path}.")
            return True
    except paramiko.SSHException as e:
        #print(f"{host}: SSH connection failed.")
        return False
    except NoValidConnectionsError as e:
        #print(f"{host}: No valid SSH connections. Check host details and ensure the SSH server is running.")
        return False
    except TimeoutError:
        #print(f"{host}: SSH connection timed out.")
        return False
    finally:
        ssh.close()

import xmlrpc.client

def check_wordpress_default_credentials(url, username="admin", password="admin", timeout=10):
    xmlrpc_url = f"{url}/xmlrpc.php"
    try:
        wp_client = xmlrpc.client.ServerProxy(xmlrpc_url)
        user_id = wp_client.wp.getUsersBlogs(username, password)[0]["blogid"]

        if user_id:
            #print(f"{url}: Default WordPress credentials found: {username}/{password}.")
            return False
    except xmlrpc.client.Fault as e:
        if e.faultCode == 403:
            #print(f"{url}: Default WordPress credentials not found.")
            return True
        else:
            #print(f"{url}: Error while checking WordPress credentials: {e}")
            return False
    except Exception as e:
        #print(f"{url}: Error while checking WordPress credentials: {e}")
        return False


def check_firewall_ports(host, username, password, allowed_ports=[21, 22, 80, 443], timeout=10):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, username=username, password=password, timeout=timeout)
        stdin, stdout, stderr = ssh.exec_command("sudo iptables -L INPUT -v -n")
        output = stdout.read().decode('utf-8').strip()

        if "Chain INPUT (policy DROP)" not in output:
            #print(f"{host}: Firewall not enabled or not configured to DROP by default.")
            return False

        allowed_ports_str = " ".join(str(port) for port in allowed_ports)
        for line in output.split('\n'):
            if "ACCEPT" in line:
                for port in allowed_ports:
                    if str(port) in line:
                        allowed_ports_str = allowed_ports_str.replace(str(port), "")

        if not allowed_ports_str.strip():
            #print(f"{host}: All required ports are allowed: {allowed_ports}")
            return True
        else:
            #print(f"{host}: Some required ports are not allowed: {allowed_ports_str.strip()}")
            return False

    except paramiko.SSHException as e:
        #print(f"{host}: SSH connection failed.")
        return False
    except NoValidConnectionsError as e:
        #print(f"{host}: No valid SSH connections. Check host details and ensure the SSH server is running.")
        return False
    except TimeoutError:
        #print(f"{host}: SSH connection timed out.")
        return False
    finally:
        ssh.close()


def main():
    servers = [
        {"host": "secureby.design"},
        {"host": "127.0.0.1"},
        # Add more servers as needed
    ]

    while True:

        for server in servers:
            host = server["host"]
            mysql_user = "wordpress"
            mysql_password = "String001"
            website_url = "http://" + server["host"]

            wordpress_default_credentials_check = check_wordpress_default_credentials(website_url)
            if not wordpress_default_credentials_check:
                penalty_points[host] = penalty_points.get(host, 0) + 10
                print(host+" wordpress")

            irewall_ports_check = check_firewall_ports(host, "admin", "SecPwdStr001")
            if not irewall_ports_check:
                penalty_points[host] = penalty_points.get(host, 0) + 10
                print(host+" firewall")

            admin_cronjob_check = check_admin_cronjob(host, "admin", "SecPwdStr001")
            if not admin_cronjob_check:
                penalty_points[host] = penalty_points.get(host, 0) + 10
                print(host+" cronjob")

            modsecurity_check = check_modsecurity_installed(host, "admin", "SecPwdStr001")
            if not modsecurity_check:
                penalty_points[host] = penalty_points.get(host, 0) + 10
                print(host+" modsecurity")

            ssh_file_check = check_ssh_file_exists(host, "admin", "SecPwdStr001")
            if not ssh_file_check:
                penalty_points[host] = penalty_points.get(host, 0) + 10
                print(host+" file check")

            anonymous_access = check_anonymous_access(host, 21)
            if not anonymous_access:
                penalty_points[host] = penalty_points.get(host, 0) + 10
                print(host+" ftp")

            mysql_connection = check_mysql_connection(host, mysql_user, mysql_password)
            if not mysql_connection:
                penalty_points[host] = penalty_points.get(host, 0) + 10
                print(host+" mysql")

            https_check = check_https(website_url)
            if not https_check:
                penalty_points[host] = penalty_points.get(host, 0) + 10
                print(host+" https")

            anne_sudo_vim_check = check_sudo_vim_permission(host)
            if not anne_sudo_vim_check:
                penalty_points[host] = penalty_points.get(host, 0) + 10
                print(host+" sudo")

        print("\nPenalty Points:")
        for host, points in penalty_points.items():
            print(f" ")
            print(f"{host}: {points} points")

        time.sleep(30)  # Wait for 5 minutes (300 seconds) before running the checks again

if __name__ == "__main__":
    main()