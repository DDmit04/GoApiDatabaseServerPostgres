import psutil

from App.controller.dto.ServerStatsDto import ServerStatDto


class ServerService:

    def get_server_stats(self):
        free_space = self.get_free_disk_space()
        return ServerStatDto(free_space)

    def get_free_disk_space(self):
        hdd = psutil.disk_usage('/')
        return hdd.free
