import urllib.request, urllib.parse
import os
import ez
from ez import have, find, sub, similar
import eyed3
import traceback

music_fmt = ['.mp3', '.wma', '.ape', '.flac']
isMusic = lambda x:have(x.lower()).any(*music_fmt)
find_fmt = lambda x:have(x.lower()).which(*music_fmt)
deformat = lambda x:ez.without(x, find_fmt(x))
fengexian = '\n' + ' = ' * 5 + '分割线' + ' = ' * 5 + '\n'
defaultPath = "D:\\Media\\Music\\"
header = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,  like Gecko) Chrome/31.0.165063 Safari/537.36 AppEngine-Google."}

def utf8(byte):
    '''不知道怎么弄成utf8=  = '''
    if type(byte) == str and byte:
        return sub(repr(byte.encode())[2:-1], '\'', '%27', '\\x', '%', ' ', '%20')
    return ''

def lyrics_stripper(lrc):
    lst=lrc.split('\n')
    new_lrc = ''
    for sentence in lst:
        new_lrc += sentence.strip() + '\n'
    print(new_lrc)

class searcher:
    def __init__(self, title, artist = '', Print = True, saveAs = False, speed = 'f'):
        '''Title means the title of a song.
            The artist of the song is optional but recommended for more accurate results.
            Default set to print the lyrics but not to save them.
            Change "saveAs" to the format of lyrics(Default: lrc) to save.
            If speed is "y"(fast),  then find the lyrics as fast as possible.
            If speed is "n"(normal),  then find a reasonable amount of lyrics.
            Otherwise,  then find all the lyrics from available sources.'''
        if type(title) != str:
            raise Exception('Invalid title!')
        elif title == '':
            raise Exception('没有歌名怎么让人家帮你搜啦')
        if type(artist) != str:
            raise Exception('Invalid artist!')
        os.chdir(ez.desktop)
        self.invalid = ['<em>', '</em>', '<br />', '<br>', '</p>']
        self.title = self.new_title = title
        self.artist = artist
        self.text = '《{}》'.format(self.title)
        if self.artist:
            self.text = self.artist + '的' + self.text
        self.lyrics = ''
        self.lyrics_list = []
        self.url = {}
        self.again = False
        self.lrcfmt = ['lrc', 'txt', 'doc', 'docx']
        self.error = False
        self.search(Print, saveAs, speed)

    def search(self, Print = True, saveAs = False, speed = 'f'):
        '''Print and save the first lyrics only.
            If speed is "f"(fast),  then find the lyrics as fast as possible.
            If speed is "n"(normal),  then find a reasonable amount of lyrics.
            Otherwise,  then find all the lyrics from available sources.'''
        srclist = ['baidu', 'xiami']
        try:
            self.parse(self.title, self.artist, speed)
            if self.lyrics_list == []:
                print('QAQ主人sama搜不到{}的歌词诶...'.format(self.text))
                self.again = True
                for left, right in [('(', ')'), ('（', '）'), ('《', '》'), ('(', '）'), ('（', ')')]:
                    if have(self.title).all(left, right):
                        self.new_title = (self.title[:self.title.find(left)] + self.title[find(self.title).last(right) + 1:]).strip()
                        print('直接搜一下《{}》看看~'.format(self.new_title))
                        self.parse(self.new_title, self.artist, speed)
                        if self.lyrics_list:
                            print('嘤嘤嘤找到啦!!!~~~')
                            break
                        else:
                            print('QAQ抱歉，直接搜《{}》找不到诶...'.format(self.new_title))
                else:
                    if self.artist:
                        print('不管作者了，直接搜一下《{}》看看~'.format(self.title))
                        self.parse(self.new_title, '', speed)
                        if self.lyrics_list:
                            print('嘤嘤嘤找到啦!!!~~~')
                        else:
                            print('QAQ抱歉，直接搜《{}》也找不到诶...'.format(self.new_title))
                            return ''
                    else:
                        print('网址在这里，主人sama您自己试试吧~')
                        for url in self.url:
                            print(url + ': ' + self.url[url])
                        return ''
            self.lyrics = self.lyrics_list[0]
            if saveAs:
                self.save(saveAs)
            if Print:
                print('总共找到了{}条结果, 为您呈现第1条~\n\n{}\n'.format(len(self.lyrics_list), self.lyrics))
            else:
                return self.lyrics
        except PermissionError:
            print('请先关闭音乐播放器哦~')
            self.error = PermissionError
        except KeyboardInterrupt:
            if self.error == KeyboardInterrupt:
                raise Exception('好吧好吧 看起来是真的想离开人家呢o(╥﹏╥)o')
            else:
                print('嘤嘤嘤被键盘打断了')
                self.error = KeyboardInterrupt
                return
        except:
            print(traceback.format_exc())
            print('诶呀呀出故障了，网址在这里，主人sama您自己试试吧~')
            for src in self.url:
                print(self.url[src])
            self.error = True

    def parse(self, title = '', artist = '', speed = ''):
        ctitle = utf8(title) ## c means encoded
        cartist = utf8(artist)
        self.url={'baidu':'http://music.baidu.com/search/lrc?key = ' + ctitle + ['', '%20' + cartist][artist != ''],
            'xiami':'http://www.xiami.com/search?key = ' + ctitle + ['', ' + ' + cartist][artist != '']}
        for source in self.url:
            request=urllib.request.Request(self.url[source],  headers=header)
            data=urllib.request.urlopen(request).read().decode().split('\n')
            lyrics = ''
            begin = False
            if source == 'baidu':
                for line in data:
                    line=line.strip()
                    hv=have(line)
                    if hv.start('<a href="/song') and 'title = "{}"'.format(title) in line:
                        start = True
                    elif hv.start('<span class="author_list"'):
                        if artist and not hv.end('title = "{}"'.format(artist)):
                            begin = False
                    elif hv.end('<div class="page-cont">'):
                        break
                    elif begin:
                        if hv.start('<p id="lyricCont-'):
                            line=line[line.find('>') + 1:]
                        if hv.end('<br />', '</p>'):
                            lyrics += ez.without(sub(line, '<br />', '\n', '&#039;', '\'').strip(), *self.invalid) + '\n'
                            if have(line).end('</p>'):
                                self.lyrics_list.append(lyrics[:-1])
                                lyrics = ''
                                if speed == 'f':
                                    return
                                elif speed == 'n' and len(self.lyrics_list) > 2:
                                    return
            elif source == 'xiami':
                urls = []
                for line in data:
                    line = line.strip()
                    hv = have(line)
                    if hv.start('<a target="_blank" href = ') and hv.all('song', 'title = "{}"'.format(sub(title, '\'', '&#039;'))):
                        urls.append(find(line).between('href="', '" title'))
                    elif hv.end('''<a class="song_digg" href="javascript:void(0)" title = "推荐" onclick="recommend('1773881048', '32')"><span>推荐</span></a>'''):
                        break
                for url in urls:
                    request = urllib.request.Request(url,  headers=header)
                    data = urllib.request.urlopen(request).read().decode().split('\n')
                    for line in data:
                        line = line.strip()
                        if line == '<div class="lrc_main">':
                            begin = True
                        elif begin:
                            if line == '</div>':
                                self.lyrics_list.append(lyrics[:-1])
                                lyrics = ''
                                if speed == 'f':
                                    return
                                elif speed == 'n' and len(self.lyrics_list)>2:
                                    return
                                break
                            lyrics += ez.without(sub(line, '<br>', '\n', '<br />', '\n', '&#039;', '\'').strip(), *self.invalid) + '\n'

    def save(self, saveAs = 'lrc', ALL = True):
        '''Save the lyrics as a file.'''
        if self.lyrics:
            if saveAs == '':
                saveAs = 'lrc'
            elif saveAs not in self.lrcfmt:
                print('不支持这种格式哦，只支持{}呢'.format(',  '.join(self.lrcfmt)))
                return
            if len(self.lyrics_list) == 1 or not ALL:
                ez.fwrite(self.title + ' ' + self.artist + '.' + saveAs, self.lyrics)
            else:
                path = self.title + ' ' + self.artist
                os.mkdir(path)
                os.chdir(path)
                for i, lrc in enumerate(self.lyrics_list):
                    ez.fwrite(f'{i + 1}.{saveAs}', lrc)
        else:
            print('没有歌词哦')

    def read(self, ALL = True):
        '''Print the lyrics of a song.'''
        if self.lyrics:
            if len(self.lyrics_list) == 1 or not ALL:
                print(self.lyrics)
            else:
                print('总共有{}条歌词~'.format(len(self.lyrics)))
                for i, lrc in enumerate(self.lyrics_list):
                    print('这是第{}条歌词：\n\n'.format(i + 1))
                    print(lrc)
                    print(fengexian)
        else:
            print('没有歌词哦')

    def next(self, number = -1):
        '''Should be called when undesired lyrics were given.
           Remove the first lyrics and display the next.
           Evaluate "number" to jump to the nth lyrics.
           Notice: Index starts from 1,  not 0.'''
        if self.lyrics_list:
            if number == -1:
                self.lyrics_list.pop(0)
                print(f'删掉了第1个结果咩~为您呈现下一个~\n\n{self.lyrics}')
            else:
                try:
                    self.lyrics_list = self.lyrics_list[number - 1:]
                except IndexError:
                    print('没有那么多歌词哦')
                    return
                print(f'将您的歌词设置为第{number}条辣\n~{self.lyrics}')
            self.lyrics = self.lyrics_list[0]
        else:
            print('没有歌词辣!')

class setter:
    def __init__(self, path = '', artist = ''):
        '''Default path: "D:\\Media\\Music".
           Path can be music but needs ".mp3" at the end.
           Input artist to specify the song.'''
        self.path = "D:\\Media\\Music\\"
        os.chdir(defaultPath)
        if path:
            path = path[have(path).start('\\'):].strip()
            self.path = path
        self.title = ''  ## Doesn't have .mp3 at the end
        self.artist = artist
        self.format = '.mp3'
        self.lyrics = ''
        self.lyrics_list = []
        self.song_list = []
        self.fail_list = []
        self.again_list = []
        self.count = 0  ##Count how many times set() is successfully called.
        self.talf = ()  ##title artist lyrics format

        if os.path.exists(self.path):
            if os.path.isdir(self.path):
                os.chdir(self.path)
            elif os.path.isfile(self.path) and isMusic(self.path):
                index=find(self.path).last('\\')
                self.title = deformat(self.path[index + 1:])
                self.format = find_fmt(self.path)
                self.path = self.path[:index + 1]
        else:
            index=find(path).last('\\')
            self.title = deformat(self.path[index + 1:])
            if index != -1:
                self.path = path[:index + 1]
            else:
                self.path = defaultPath
            ## 忘记文件格式
            for fmt in music_fmt:
                if os.path.isfile(path + fmt):
                    music = eyed3.load(path + fmt)
                    self.artist = music.tag.artist
                    self.format = fmt
                    self.lyrics = music.tag.lyrics[0].text
                    break
            else:
                ## 找相似歌曲
                if path and not os.path.exists(self.path):
                    raise Exception('路径不存在哦')
                os.chdir(self.path)
                most_similar = ('', 0, '') ## song, score, artist
                for song in os.listdir():
                    if not isMusic(song):
                        continue
                    score = similar(song, self.title)
                    music_artist = eyed3.load(song).tag.artist
                    if artist:
                        bonus = similar(music_artist, artist)
                        score += bonus
                    if score != 0 and score >= most_similar[1]:
                        most_similar=(song, score, music_artist)
                song, score, self.artist = most_similar
                de = '的' if self.artist else ''
                text = f'{self.artist}{de}《{self.title}》'
                if score:
                    self.title = deformat(song)
                    self.format = find_fmt(song)
                    print(f'这个路径下只能找到{text}哦，自动调整成这首歌啦')
                else:
                    raise Exception(f'QAQ这个路径下找不到{text}诶...')

        if not path.startswith(defaultPath) and os.path.exists(defaultPath + self.path):
            have(path).start(defaultPath)
            self.path = defaultPath + self.path
        if not self.path.endswith('\\'):
            self.path += '\\'
        if self.title == '':
            for song in os.listdir(self.path):
                if os.path.isfile(song) and isMusic(song):
                    self.song_list.append(song)
                    try:
                        self.lyrics_list.append(eyed3.load(song).tag.lyrics[0].text)
                    except IndexError:
                        pass
            self.many_songs = len(self.song_list)
            if self.many_songs == 0:
                print('噫，这个文件夹好像没有音乐呢……')
                return
            elif self.many_songs == 1:
                song = self.song_list[0]
                music = eyed3.load(song)
                self.title = deformat(song)
                self.artist = music.tag.artist
                self.format = find_fmt(song)
                try:
                    self.lyrics = self.lyrics_list[0]
                except IndexError:
                    pass
        else:
            music = eyed3.load(self.path + self.title + self.format)
            self.artist = music.tag.artist
            try:
                self.lyrics = music.tag.lyrics[0].text
                self.lyrics_list = [self.lyrics]
            except IndexError:
                pass

    def add(self, source = '', overwrite = False):
        '''Add lyrics (Recommended for users).'''
        if source:
            overwrite = True
        if self.title:
            self.set(self.title, self.artist, source, overwrite)
            if not self.fail_list:
                print('下面是歌词~\n\n' + self.lyrics + '\n')
        else:
            for song in self.song_list:
                songartist = eyed3.load(self.path + song).tag.artist
                self.set(title = song, artist = songArtist, src = source, ow = overwrite)
            if self.count == 1 and self.title == '' and self.artist == '' and self.lyrics == '':
                self.title, self.artist, self.lyrics, self.format = self.talf
            if self.count:
                self.count = 0
                print('\n嘻嘻任务搞定啦~~~')
            if self.fail_list:
                response = input('如果想查看导入歌词失败的歌曲请输入"y"哟，其他输入表示不想看嘤嘤\n>>>')
                if response == 'y':
                    print('失败的歌曲有{}首，哭哭'.format(len(self.fail_list)))
                    self.fail()

    def set(self, title, artist = '', src = '', ow = False):
        '''Set lyrics.'''
        fmt = '.mp3'
        if isMusic(title):
            fmt = find_fmt(title)
            title = deformat(title)
        de = '的' if artist else ''
        text = f'{artist}{de}《{title}》'
        try:
            music = eyed3.load(self.path + title + self.format)
            print(f'成功加载{text}~~~')
            if len(music.tag.lyrics):
                if music.tag.lyrics[0].text and not ow:
                    self.lyrics = music.tag.lyrics[0].text
                    print('这首歌已经有歌词了呢~')
                    return
            if artist == '':
                artist = music.tag.artist
                if self.title and self.artist == '':
                    self.artist = artist
            if src == '':
                print('正在搜索歌词...')
                search = searcher(title, artist, Print = False, saveAs = False)
                if search.error in [KeyboardInterrupt, PermissionError]:
                    return
                self.lyrics = search.lyrics
                self.lyrics_list = search.lyrics_list[:]
                if self.lyrics:
                    self.count += 1
                    if self.count == 1:
                        self.talf=(title, artist, search.lyrics, fmt)
                else:
                    self.fail_list.append((title, artist))
                    print(f'QAQ找不到{text}的歌词，歌词写入失败...')
                    return
                if search.again:
                    self.again_list.append((title, artist))
            elif self.title:
                self.lyrics = src
            music.tag.lyrics.set(self.lyrics)
            music.tag.save()
            if ow:
                if src:
                    print(f'{text}成功覆盖写入歌词~~~')
                else:
                    print(f'总共找到{len(self.lyrics_list)}条歌词，已覆盖写入第1条√')
            else:
                print(f'总共找到{len(self.lyrics_list)}条歌词，已成功写入第1条~~~')
        except KeyboardInterrupt:
            return
        except:
            self.fail_list.append((title, artist))
            print(traceback.format_exc())

    def reset(self, lyrics, title = ''):
        '''Reset lyrics.'''
        file = self.path
        if not title:
            title = self.title
        file += title + self.format
        try:
            music = eyed3.load(file)
        except FileNotFoundError:
            print('没有这首歌嘤嘤')
            return
        music.tag.lyrics.set(lyrics)
        music.tag.save()
        self.lyrics = lyrics
        self.lyrics_list = [lyrics]
        print('重设歌词成功~')

    def delete(self, title = ''):
        '''Delete lyrics.'''
        if not title:
            title = self.title
        if title:
            music = eyed3.load(self.path + title + self.format)
            music.tag.lyrics.set('')
            music.tag.save()
            print('《' + self.title + '》的歌词已经被删除啦~')
        else:
            areusure = input('你真的想删除所有的歌词嘛？输入"y"表示确定，其他输入会被当做哎呀呀弄错惹\n>>>')
            if areusure != 'y':
                return
            for song in self.song_list:
                music = eyed3.load(self.path + song)
                music.tag.lyrics.set('')
                music.tag.save()
                print(f'《{deformat(song)}》的歌词已经被删除啦~')

    def fail(self):
        '''Print all songs failed to find matching lyrics.'''
        if self.fail_list:
            for title, artist in self.fail_list:
                if artist:
                    print(f'《{title}》', '-' * 3, artist)
                else:
                    print(title)
        else:
            print('没有失败的哦~~~')

    def retry(self):
        '''Rematch lyrics for the failed songs.'''
        for song in self.fail_list:
            songartist = eyed3.load(self.path + song).tag.artist
            self.set(title = song, artist = songArtist, src = source)

    def again(self):
        '''Print all songs that are searched again to find matching lyrics.'''
        if self.again_list:
            for title, artist in self.again_list:
                if artist:
                    print(title, '-' * 3, artist)
                else:
                    print(title)
        else:
            print('没有多次搜索的哦~~~')

    def read(self, title = ''):
        '''Print all the lyrics of a song or print the lyrics of all songs in a folder.'''
        if title:
            music = eyed3.load(self.path + title)
            print(music.tag.lyrics[0].text + '\n')
        else:
            if self.lyrics_list:
                if self.title:
                    print(self.lyrics)
                else:
                    for i, song in enumerate(self.song_list):
                        try:
                            music = eyed3.load(self.path + song)
                            print(f'这是《{deformat(song)}》的歌词\n~')
                            print(music.tag.lyrics[0].text)
                            if i < self.many_songs - 1:
                                print(fengexian)
                            else:
                                print()
                        except IndexError:
                            pass
            else:
                print('没有歌词哦')

    def next(self, number = -1):
        '''Should be called when undesired lyrics were given.
           Remove the first lyrics and display the next.
           Evaluate "number" to jump to the nth lyrics.
           Notice: Index starts from 1,  not 0.'''
        if self.title:
            if self.lyrics:
                if number == -1:
                    self.lyrics_list.pop(0)
                    print('删掉了第1个结果咩~')
                else:
                    try:
                        self.lyrics_list = self.lyrics_list[number - 1:]
                    except IndexError:
                        print('没有那么多歌词哦')
                        return
                    print(f'已经帮您将歌词设置为歌词库里的第{number}条歌词辣\n~')
                self.lyrics = self.lyrics_list[0]
                self.set(self.title, self.artist, src = self.lyrics, ow = True)
            else:
                raise Exception('No more lyrics!')
        else:
            print('无法变更哦')
