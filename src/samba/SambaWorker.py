import smb
from smb.SMBConnection import SMBConnection
import logging
import logging.config

from smb.smb_structs import OperationFailure

from src.config.SambaConfig import SambaConfig

logging.config.fileConfig('../resources/logging.conf')
LOGGER = logging.getLogger('exampleApp')

class SambaWorker(object):


    def __init__(self, sambaConfig: SambaConfig):
        self.host = sambaConfig.HOST
        self.username = sambaConfig.USERNAME
        self.password = sambaConfig.PASSWORD
        self.shared_name = sambaConfig.SHARED_DIRECTORY
        self.netbios_name = sambaConfig.NETBIOS_NAME
        self.workgroup = sambaConfig.WORKGROUP
        self.server: SMBConnection = None

    def connect(self):
        self.server: SMBConnection = SMBConnection(username=self.username,
                                    password=self.password,
                                    my_name=self.netbios_name,
                                    remote_name=self.netbios_name,
                                    use_ntlm_v2=True)
        self.server.connect(self.host, 139)

    def upload(self, path_to_save: str, file):
        directories = path_to_save.split('/')
        for i in range(0, len(directories) - 1):
            if directories[i] == '':
                continue
            directories[i+1] = '{0}/{1}'.format(directories[i], directories[i+1])
            try:
                self.server.createDirectory(self.shared_name, directories[i])
            except OperationFailure as ex:
                pass
            except smb.base.NotConnectedError:
                LOGGER.error("samba is not connected, try to reconnect!")
                self.connect()
                self.server.createDirectory(self.shared_name, directories[i])
        try:
            file_obj = open(file, 'rb')
            self.server.storeFile(self.shared_name, path_to_save, file_obj)
        except smb.base.NotConnectedError:
            LOGGER.error("samba is not connected, try to reconnect!")
            self.connect()
            self.server.storeFile(self.shared_name, path_to_save, file_obj)
        except BaseException as ex:
            LOGGER.exception(ex)
            raise ex
        finally:
            file_obj.close()


    def download(self, shared_file_path, temp_filename):
        file_obj = open('/tmp/{0}'.format(temp_filename), 'wb+')
        try:
            self.server.retrieveFile(self.shared_name, shared_file_path, file_obj)
        except smb.base.NotConnectedError:
            LOGGER.error("samba is not connected, try to reconnect!")
            self.connect()
            self.server.retrieveFile(self.shared_name, shared_file_path, file_obj)
        except BaseException as ex:
            LOGGER.exception(ex)
            raise ex

        return file_obj

    def delete(self, file):
        'remove file from remote share'
        file = '/' + file
        self.server.deleteFiles(self.shared_name, file)

    def list(self):
        ' list files of remote share '
        filelist = self.server.listPath(self.shared_name, '/')
        for f in filelist:
            print
            f.filename

    def close(self):
        try:
            self.server.close()
        except BaseException as ex:
            LOGGER.exception(ex)


