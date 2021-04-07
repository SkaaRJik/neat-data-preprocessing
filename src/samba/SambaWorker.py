from smb.SMBConnection import SMBConnection
import logging
import logging.config
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

    def upload(self, path_to_save, file):
        file_obj = open(file, 'rb')
        self.server.storeFile(self.shared_name, '/{0}'.format(path_to_save), file_obj)
        file_obj.close()

    def download(self, fileName):
        file_obj = open(fileName, 'wb+')
        self.server.retrieveFile(self.shared_name, fileName, file_obj)
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


