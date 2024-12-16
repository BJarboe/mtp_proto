import os, re

os.chdir('output')

class Media:
    def __init__(self, name, link):
        self.name = name
        self.link = link


def read_queue():
    prev_files = os.listdir('.')

    with open('../queue.txt', 'r') as f:
        lines = f.read().splitlines()
    
    media = []
    for line in lines:
        pair = line.split()
        try:
            if (pair[0] + '.mp4') not in prev_files:
                media.append(Media(pair[0], pair[1]))
        except Exception as e:
            print(f'Error at line {lines.index(line)}.  Check formatting?\n{e}')
            continue
    return media


def parse_hash(media):
    hash = {}

    pattern = r'/p/([^/]+)/' # extract hash

    for video in media:
        match = re.search(pattern, video.link).group(1)
        hash[match] = video
    return hash


def download(queue):
    command = 'yt-dlp -P output '
    for video in queue:
        command += video.link + ' '
    os.system(command)


def export(hash):
    files = os.listdir('.')
    pattern = r"\[([A-Za-z0-9_\-]+)\]"
    for file in files:
        try:
            if 'Video' not in file:
                continue
            match = re.search(pattern, file).group(1)
            if hash[match]:
                command = 'move \"' + file + '\" \"' + hash[match].name + '.mp4\"'
                os.system(command)
        except Exception as e:
            print(f'File Error: {file} | {e}')


def main():
    media_queue = read_queue()
    hash = parse_hash(media_queue)
    # download(media_queue)
    export(hash)


if __name__ == '__main__':
    main()