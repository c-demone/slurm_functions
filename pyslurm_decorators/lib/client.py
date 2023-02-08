import os
import sys
from os import system
from scp import SCPClient, SCPException
from paramiko import SSHClient, AutoAddPolicy, RSAKey
from paramiko.auth_handler import AuthenticationException, SSHException
from loguru import logger
from Cryptop.PublicKey import RSA

# specify logger level formats
logger.add(sys.stderr,
           format="{time} {level} {message}",
           filter="client",
           level="INFO")

logger.add('logs/log_{time:YYYY-MM-DD}.log',
           format="{time} {level} {message}",
           filter="client",
           level="ERROR")



class RemoteClient:

    """
    Remote host Client object to handle connections and actions.
    The Client object is specifically for interacting with a 
    remote host via SSH and SCP using Paramiko
    """


    def __init__(self, 
                 host, 
                 user,
                 ssh_keydir=None
                 ssh_pubkey_filename='id_rsa.pub',
                 ssh_privkey_filename='id_rsa',
                 remote_workdir=None):
        self.host = host
        self.user = user
        self.homedir = os.path.expanduser(f"~{self.user}")

        if ssh_keydir is None:
            self.ssh_keydir = f"{self.homedir}/.ssh")
        else:
            self.ssh_keydir = ssh_keydir
    
        self.ssh_pubkey_filename = ssh_pubkey_filename
        self.ssh_privkey_filename = ssh_privkey_filename
        

        self.ssh_pubkey_filepath = f"{self.ssh_keydir.rstrip()}/{self.ssh_pubkey_filename}"
        self.ssh_privkey_filepath = f"{self.ssh_keydir.rstrip()}/{self.ssh_privkey_filename}"
        
        self.remote_workdir = remote_workdir
        self.remote_keys_accesible = False
        self.client = None
        self.scp = None
    

        self.__get_ssh_key()
        self.__upload_ssh_key()


    def __get_ssh_key(self):
        """
        Fetch locally stored SSH key
        """

        try:
            self.ssh_key = RSAKey.from_private_key_file(self.ssh_privkey_filepath)
            logger.info(f'Found SSH key at {self.ssh_privkey_filepath}')
            return self.ssh_key
        
        except SSHException as error:
            logger.info(error)
            logger.info(f'Generate RSA key pair at {self.ssh_keydir}')
            self.__generate_rsa_keypair()
            self.__get_ssh_key()


    def __generate_rsa_keypair(self, bits=2048):
        key = RSA.generate(bits)
        with open(f"{self.ssh_privkey_filepath}", 'wb') as priv:
            priv.write(key.exportKey('PEM'))

        pubkey = key.publicKey()
        with open("f{self.ssh_pubkey_filepath}", 'wb') as pub:
            pub.write(pubkey.exportKey('OpenSSH'))


    def __upload_ssh_key(self):
        self.__connect()
        if self.client is not None:
            return 
        else:
            try:
                system(f'ssh-copy-id -i {self.ssh_key_filepath} {self.user}@{self.host}>/dev/null 2>&1')
                system(f'ssh-copy-id -i {self.ssh_key_filepath}.pub {self.user}@{self.host}>/dev/null 2>&1')
                logger.info(f'{self.ssh_pubkey_filepath} uploaded to {self.host}')
            except FileNotFoundError as error:
                logger.error(error) 


    def __connect(self):
        """Open connection to remote host."""
        try:
            self.client = SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(AutoAddPolicy())
            self.client.connect(self.host,
                                username=self.user,
                                key_filename=self.ssh_key_filepath,
                                look_for_keys=True,
                                timeout=5000)
            self.scp = SCPClient(self.client.get_transport())  # For later
        except AuthenticationException as error:
            logger.info('Authentication failed: did you remember to create an SSH key?')
            logger.error(error)
            raise error
        finally:
            return self.client


    def disconnect(self):
        """
        Disconnect from remote client
        """

        self.client.close()
        self.scp.close()


    def execute_command(self, commands:list) -> None:
        """
        Execute multiple commands on remote client

        Args:
            commands(list): list of commanbds to execute

            >>> e.g. ['cd /var/www/ && ls','ps aux | grep node']

        Commands will be executed in order they are listed
        """
        if self.client is None:
            self.client = self.__connect()


        for cmd in commands:
            stdin, stdout, stderr = self.client.exec_command(cmd)
            stdout.channel.recv_exit_status()
            response = stdout.readlines()
            for line in response:
                logger.info(f'INPUT: {cmd} | OUTPUT: {line}')


    def bulk_dir_upload(self, dirs)
    # a set of paths that are iterated over in a for loop and then __single_dir_upload is run
    if self.client is None:
        self.client = self.__connect()
    uploads = [self.upload_directory(d) for d in dirs]
    logger.info(f'Uploaded {len(uploads)} directories to {self.remote_path} on {self.host}')
    

    def upload_directory(self, source_dir), recursive=True):
        """
        Upload a directory of files. To upload any subdirectories within
        source_dir, leave recursive=True
        """
        for root, dirs, files in os.walk(source_dir, topdown=True):
            logger.info(f'Descending into directory {root}') 
            self.bulk_file_upload([f"{root]/{f}" for f in files])
            if not recursive:
                return [f"{root]/{f}" for f in files]


    def bulk_file_upload(self, files):
        """Upload multiple files to a remote directory."""
        if self.client is None:
            self.client = self.__connect()
        uploads = [self.upload_file(file) for file in files]
        logger.info(f'Uploaded {len(uploads)} files to {self.remote_path} on {self.host}')


    def upload_file(self, file):
        """Upload a single file to a remote directory."""
        try:
            self.scp.put(file,
                         recursive=True,
                         remote_path=self.remote_path)
        except SCPException as error:
            logger.error(error)
            raise error
        finally:
            return file 


    def download_file(self, file):
        """Download file from remote host"""
        if self.client is None:
            self.client = self.__connect()

        self.scp.get(file)
