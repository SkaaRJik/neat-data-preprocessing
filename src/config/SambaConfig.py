import pika as pika


class SambaConfig:

    def __init__(self, global_config):

        _SHARED_DIRECTORY = 'default'
        _HOST = 5672
        _USERNAME = "guest"
        _PASSWORD = "guest"
        _NETBIOS_NAME = "name"
        _WORKGROUP = "WORKGROUP"
        

        self._HOST = global_config['samba']['host'] if global_config['samba']['host'] else _HOST
        self._SHARED_DIRECTORY = global_config['samba']['shared_directory'] if global_config['samba']['shared_directory'] else _SHARED_DIRECTORY
        self._USERNAME = global_config['samba']['username'] if global_config['samba']['username'] else _USERNAME
        self._PASSWORD = global_config['samba']['password'] if global_config['samba']['password'] else _PASSWORD
        self._NETBIOS_NAME = global_config['samba']['netbios_name'] if global_config['samba']['netbios_name'] else _NETBIOS_NAME
        self._WORKGROUP = global_config['samba']['workgroup'] if global_config['samba']['workgroup'] else _WORKGROUP

    
    @property
    def SHARED_DIRECTORY(self):
        return self._SHARED_DIRECTORY

    @property
    def HOST(self):
        return self._HOST

    @property
    def USERNAME(self):
        return self._USERNAME

    @property
    def PASSWORD(self):
        return self._PASSWORD

    @property
    def WORKGROUP(self):
        return self._WORKGROUP

    @property
    def NETBIOS_NAME(self):
        return self._NETBIOS_NAME
