# _*_coding=UTF-8_*_
from rpyc.utils.server import ThreadedServer
from rpyc import Service
import subprocess
import argparse
import threading

class PingService(Service):
    # when connected
    def on_connect(self, conn):
        # print('\nconnected on {}'.format(date_time))
        pass
    # when disconnected
    def on_disconnect(self, conn):
        # print('Disonnect on {}\n'.format(date_time))
        pass

    def ping_test(self, ip):
        global ping_res
        ping_res = {}
        try:
            command = "ping -c 4 {}".format(ip)
            output = subprocess.run(command, timeout=60, shell=True, universal_newlines=True)
            ping_res[ip] = output.returncode
        except subprocess.TimeoutExpired:
            ping_res[ip] = 1

    def exposed_run_command(self, ip_list):
        threads = []
        # print(len(ip_list))
        for i in range(len(ip_list)):
            # print("Current IP is:{}".format(ip_list[i]))
            one_thread = threading.Thread(target=self.ping_test, args=(ip_list[i],), name="ping-{}".format(ip_list[i]))
            threads.append(one_thread)

        for index in threads:
            index.start()

        for j in threads:
            j.join()

        return ping_res

def main():
    parser = argparse.ArgumentParser(description="Ping Server")
    parser.add_argument('-p', '--port', type=int, default=1, help='Enter custom port number')
    args = parser.parse_args()
    port = args.port

    server = ThreadedServer(PingService, port=port)
    server.start()

if __name__ == '__main__':
    main()
