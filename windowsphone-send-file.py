import argparse
import subprocess
import os


class Sender:
    def __init__(self, *args, **kwargs):
        self.dest = kwargs['dest']
        mapping = {'picture': '/Pictures',
                   'video': '/Video',
                   'music': '/Music'}
        try:
            self.data_type_path = mapping[kwargs['data_type']]
        except KeyError:
            raise Exception("Please enter one of the following types: {picture, video, music}")
        else:
            print("path is {} mode is {}".format(self.dest, self.data_type_path))

    def get_files(self):
        for path, dirs, files in os.walk(self.dest):
            for f in files:
                yield path, f

    def send_files(self):
        for path, f in self.get_files():
            path = os.path.join(path, f)
            subprocess.call(["mtp-sendfile",
                             path,
                             self.data_type_path])

    def run(self):
        return self.send_files()

if __name__ == '__main__':

    default_path = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description='Send file to windows-phone')
    parser.add_argument("-d", "-destination", help="Path of files", default=default_path)
    parser.add_argument("-t", "-data_type", help="Type of data (picture, video, music)")
    args = parser.parse_args()
    type_, dest = args.t, args.d
    s = Sender(data_type=type_, dest=dest)
    s.run()
