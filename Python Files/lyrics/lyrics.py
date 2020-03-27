import urllib.request, urllib.parse, requests
import os
import ez
from ez import find, sub, similar
import eyed3
import traceback
import json

music_fmt = ['.mp3', '.wma', '.ape', '.flac']
is_music = lambda x: any(x.endswith(fmt) for fmt in music_fmt)
find_fmt = lambda x: next((fmt for fmt in music_fmt if x.endswith(fmt)), "")
get_title = lambda x: ez.without(x, find_fmt(x))
separator = '\n' + '=' * 5 + '分割线' + '=' * 5 + '\n'
defaultPath = r"C:\Users\Seaky\Desktop\Media\Music"

def utf8(byte):
    '''不知道怎么弄成utf8=  = '''
    if type(byte) == str and byte:
        return sub(repr(byte.encode())[2:-1], '\'', '%27', '\\x', '%', ' ', '%20')
    return ''

def lyrics_stripper(lrc: str) -> str:
    return '\n'.join(sentence.strip() for sentence in lrc.split('\n'))

class Searcher:
    def __init__(self, title: str, artist: str = '', Print: bool = True, amount: int = 1):
        '''
        @params:
        title : the name of the target song.
        artist: optional but recommended for more accurate results.
        Print : print lyrics if True.
        amount: the max number of lyrics returned.
                Set to 0 to get all results.
        '''
        self.search(title, artist, Print, amount)

    def init(self, title: str, artist: str = '', Print: bool = True, amount: int = 1):
        self.title = title
        self.artist = artist
        self.text = '《{}》'.format(self.title)
        if self.artist:
            self.text = self.artist + '的' + self.text
        self.lyrics = ''
        self.lyrics_list = []
        self.urls = []
        self.again = False
        self.Print = Print
        self.amount = amount

    def search(self, title, artist, Print, amount):
        '''Find and output lyrics.'''
        self.init(title, artist, Print, amount)
        try:
            self._search(title, artist, amount)
            if self.lyrics_list == []:
                print(f'QAQ主人sama搜不到{text}的歌词诶...')
                self.again = True
                for left, right in [('(', ')'), ('（', '）'), ('《', '》'), ('(', '）'), ('（', ')')]:
                    if ez.contains(title, left, right):
                        new_title = (title[:title.find(left)] + title[find(title).last(right) + 1:]).strip()
                        print(f'直接搜一下《{new_title}》看看~')
                        self._search(new_title, artist, amount)
                        if self.lyrics_list:
                            print('哇哇哇找到啦!!!~~~')
                            break
                        else:
                            print(f'QAQ抱歉，直接搜《{new_title}》也找不到诶...')
                else:
                    if artist:
                        print(f'不管作者了，直接搜一下《{title}》看看~')
                        self._search(title, '', amount)
                        if self.lyrics_list:
                            print('嘤嘤嘤找到啦!!!~~~')
                        else:
                            print(f'QAQ抱歉，只搜《{title}》也找不到诶...')
                            return ''
                    else:
                        print('网址在这里，主人sama您自己试试吧~')
                        for url in self.urls:
                            print(url)
                        return ''
            self.lyrics = self.lyrics_list[0]
            if Print:
                print(f'总共找到了{len(self.lyrics_list)}条结果, 为您呈现第1条~\n\n{self.lyrics}\n')
        except PermissionError:
            print('请先关闭音乐播放器哦~')
            self.error = PermissionError
        except KeyboardInterrupt:
            if self.error == KeyboardInterrupt:
                raise Exception('好吧好吧，看起来是真的想离开人家呢o(╥﹏╥)o')
            else:
                print('嘤嘤嘤被键盘打断了，再来一次强行终止哦')
                self.error = KeyboardInterrupt
        except Exception as e:
            print(traceback.format_exc())
            print('诶呀呀出故障了，网址在这里，主人sama您自己试试吧~')
            for url in self.urls:
                print(url)
            self.error = type(e)
        finally:
            return '' if self.error else self.lyrics

    def _search(self, title, artist, amount):
        self.urls.clear()
        self.qqmusic(title, artist, amount)

    def qqmusic(self, title, artist, amount):
        keyword = (title + ' ' + artist) if artist else title
        self.urls.append('https://y.qq.com/portal/search.html#page=1&searchid=1&remoteplace=txt.yqq.top&t=song&w=' + utf8(keyword))
        url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp'
        params = {
            'ct': 24,
            'qqmusic_ver': 1298,
            'new_json': 1,
            'remoteplace':'sizer.yqq.lyric_next',
            'searchid': 63514736641951294,
            'aggr': 1,
            'cr': 1,
            'catZhida': 1,
            'lossless': 0,
            'sem': 1,
            't': 7,
            'p': 1,
            'n': 1,
            'w': keyword,
            'g_tk': 1714057807,
            'loginUin': 0,
            'hostUin': 0,
            'format': 'json',
            'inCharset': 'utf8',
            'outCharset': 'utf-8',
            'notice': 0,
            'platform': 'yqq.json',
            'needNewCode': 0
        }
        headers = {
            'content-type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0',
            'referer':'https://y.qq.com/portal/search.html'
        }
        result = requests.get(url, params = params, headers = headers)
        data = json.loads(result.text)
        for item in data['data']['lyric']['list']:
            lyrics = lyrics_stripper(item['content'].replace('\\n', '\n'))
            self.lyrics_list.append(lyrics)
            if len(self.lyrics_list) == amount:
                break
        return len(self.lyrics_list) == 0

    def save(self, fmt = 'lrc', All = True):
        '''
        @params:
            fmt: save lyrics into a file with the specified format.
            All: save all instead of the one
        '''
        filename = f'{self.title}-{self.artist}'
        if All and len(self.lyrics_list) > 1:
            for i, lrc in enumerate(self.lyrics_list):
                ez.fwrite(f'{filename}（{i + 1}）.{fmt}', lrc)
        else:
            ez.fwrite(f'{filename}.{fmt}', self.lyrics)

    def read(self, All = True):
        '''Print the lyrics of a song.'''
        if self.lyrics:
            if All and len(self.lyrics_list) > 1:
                print(f'总共有{len(self.lyrics)}条歌词~')
                for i, lrc in enumerate(self.lyrics_list):
                    print(f'这是第{i + 1}条歌词：\n\n')
                    print(lrc)
                    print(separator)
            else:
                print(self.lyrics)
        else:
            print('没有歌词哦')

    def next(self, nth = 1):
        '''Should be called when lyrics given are undesired.
           Remove the first lyrics and display the next.
           @parmas:
               nth: jump to the nth lyrics after the first one.'''
        if nth >= len(self.lyrics_list):
            print('没有那么多歌词哦')
            return
        self.lyrics_list = self.lyrics_list[nth:]
        self.lyrics = self.lyrics_list[0]
        print(f'将您的歌词设置为第{nth}条辣：\n{self.lyrics}')

class Setter:
    def __init__(self, path = '', artist = ''):
        f'''
        @params:
            path  : can be either a folder or a music but needs to end with ".mp3".
            artist: the artist of the music.'''
        os.chdir(defaultPath)
        if path:
            path = os.path.normpath(path)
            path = path[path.startswith('\\'):].strip()
            self.path = path
        else:
            self.path = defaultPath
        self.title = ''  ## No .mp3 at the end
        self.artist = artist
        self.format = '.mp3'
        self.lyrics = ''
        self.lyrics_list = []
        self.song_list = []
        self.success_list = []
        self.fail_list = []
        self.again_list = []
        self.talf = ()  ## title artist lyrics format

        if os.path.exists(self.path):
            if os.path.isdir(self.path):
                os.chdir(self.path)
            elif os.path.isfile(self.path) and is_music(self.path):
                self.title = get_title(os.path.basename(self.path))
                self.format = find_fmt(self.path)
                self.path = os.path.dirname(self.path)
        else:
            self.title = get_title(os.path.basename(self.path))
            self.path = os.path.dirname(self.path) or defaultPath
            ## 忘记文件格式
            for fmt in music_fmt:
                full_path = path + fmt
                if os.path.isfile(full_path):
                    music = eyed3.load(full_path)
                    self.artist = music.tag.artist
                    self.format = fmt
                    self.lyrics = music.tag.lyrics[-1].text
                    break
            else:
                ## 模糊查找相似歌曲，不支持模糊查找路径
                assert os.path.exists(self.path), '路径不存在哦'
                os.chdir(self.path)
                most_similar = ('', 0, '') ## song, score, artist
                for song in os.listdir():
                    if not is_music(song):
                        continue
                    score = similar(song, self.title)
                    music_artist = eyed3.load(song).tag.artist
                    if artist:
                        bonus = similar(music_artist, artist)
                        score += bonus
                    if score != 0 and score >= most_similar[1]:
                        most_similar = (song, score, music_artist)
                song, score, self.artist = most_similar
                de = '的' if self.artist else ''
                text = f'{self.artist}{de}《{song}》'
                if score:
                    self.title = get_title(song)
                    self.format = find_fmt(song)
                    print(f'这个路径下只能找到{text}哦，自动调整成这首歌啦')
                else:
                    raise FileNotFoundError(f'QAQ这个路径下找不到{text}诶...')

        self.is_file = self.title != ''
        if not path.startswith(defaultPath) and os.path.exists(defaultPath + self.path):
            self.path = defaultPath + self.path
        if not self.path.endswith('\\'):
            self.path += '\\'
        if self.is_file:
            music = eyed3.load(self.path + self.title + self.format)
            self.artist = music.tag.artist
            try:
                self.lyrics = music.tag.lyrics[-1].text
                self.lyrics_list.append(self.lyrics)
            except IndexError:
                pass
        else:
            for song in os.listdir(self.path):
                if is_music(song):
                    self.song_list.append(song)
                    try:
                        self.lyrics_list.append(eyed3.load(song).tag.lyrics[-1].text)
                    except IndexError:
                        pass
            songs = len(self.song_list)
            if songs == 0:
                raise FileNotFoundError('噫，这个文件夹好像没有音乐呢……')
            elif songs == 1:
                song = self.song_list[0]
                music = eyed3.load(song)
                self.title = get_title(song)
                self.artist = music.tag.artist
                self.format = find_fmt(song)
                try:
                    self.lyrics = self.lyrics_list[0]
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
            for i, song in enumerate(self.song_list):
                artist = eyed3.load(self.path + song).tag.artist
                self.set(title = song, artist = artist, src = source, ow = overwrite)
                print(f'还剩{len(self.song_list) - i - 1}首！')
            if len(self.success_list) == 1 and self.title == '' and self.artist == '' and self.lyrics == '':
                self.title, self.artist, self.lyrics, self.format = self.talf
            print('~~~嘻嘻嘻任务完成啦~~~')
            if self.success_list and input('如果想查看导入歌词成功的歌曲请输入"y"哟，其他输入表示不想看嘤嘤嘤\n>>>') == 'y':
                self.success()
            if self.fail_list and input('如果想查看导入歌词失败的歌曲请输入"y"哟，其他输入表示不想看嘤嘤嘤\n>>>') == 'y':
                self.fail()

    def set(self, title, artist = '', src = '', ow = False):
        '''Set lyrics.'''
        fmt = '.mp3'
        if is_music(title):
            fmt = find_fmt(title)
            title = get_title(title)
        de = '的' if artist else ''
        text = f'{artist}{de}《{title}》'
        try:
            music = eyed3.load(self.path + title + self.format)
            print(f'成功加载{text}~~~')
            if music.tag.lyrics and not ow:
                self.lyrics = music.tag.lyrics[-1].text
                print('这首歌已经有歌词了呢~')
                return
            if artist == '':
                artist = music.tag.artist
                if self.is_file and self.artist == '':
                    self.artist = artist
            if src == '':
                print('开始搜索歌词...')
                search = Searcher(title, artist, Print = False)
                if search.error in [KeyboardInterrupt, PermissionError]:
                    return
                self.lyrics = search.lyrics
                self.lyrics_list = search.lyrics_list[:]
                if self.lyrics:
                    self.success_list.append((title, artist))
                    if len(self.success_list) == 1:
                        self.talf = (title, artist, search.lyrics, fmt)
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
        file = self.path + (title or self.title) + self.format
        try:
            music = eyed3.load(file)
        except FileNotFoundError:
            print('没有这首歌嘤嘤嘤')
            return
        music.tag.lyrics.set(lyrics)
        music.tag.save()
        self.lyrics = lyrics
        self.lyrics_list = [lyrics]
        print('重设歌词成功~')

    def delete(self, title = ''):
        '''Delete lyrics.'''
        title = title or self.title
        if title:
            music = eyed3.load(self.path + title + self.format)
            music.tag.lyrics.set('')
            music.tag.save()
            print('《' + self.title + '》的歌词已经被删除啦~')
        elif input(f'你真的想删除{self.path}下所有歌曲的歌词嘛？输入"y"表示确定，其他输入会被当做"哎呀呀弄错惹"哟\n>>>') == 'y':
            for song in self.song_list:
                music = eyed3.load(self.path + song)
                music.tag.lyrics.set('')
                music.tag.save()
                print(f'《{get_title(song)}》的歌词已经被删除啦~')

    def fail(self):
        '''Print all songs failed to find matching lyrics.'''
        if self.fail_list:
            print(f'哭哭，失败的歌曲有{len(self.fail_list)}首，他们是：')
            for title, artist in self.fail_list:
                if artist:
                    print(f'《{title}》', '-' * 3, artist)
                else:
                    print(f'《{title}》')
        else:
            print('没有失败的哦~~~')

    def success(self):
        '''Print all songs that were set lyrics.'''
        if self.success_list:
            print(f'嘻嘻，成功的歌曲有{len(self.success_list)}首！他们是：')
            for title, artist in self.success_list:
                if artist:
                    print(f'《{title}》', '-' * 3, artist)
                else:
                    print(f'《{title}》')
        else:
            print('没有成功的诶……')


    def retry(self):
        '''Rematch lyrics for the failed songs.'''
        for title, artist in self.fail_list:
            self.set(title = title, artist = artist)

    def again(self):
        '''Print all songs that searches multiple times.'''
        if self.again_list:
            for title, artist in self.again_list:
                if artist:
                    print(f'《{title}》', '-' * 3, artist)
                else:
                    print(f'《{title}》')
        else:
            print('没有多次搜索的哦~~~')

    def read(self, title = ''):
        '''Print the lyrics of a song or print the lyrics of all songs in a folder.'''
        if title:
            music = eyed3.load(self.path + title)
            print(music.tag.lyrics[-1].text)
            print()
        else:
            if self.lyrics_list:
                if self.is_file:
                    print(self.lyrics)
                else:
                    for i, song in enumerate(self.song_list):
                        try:
                            music = eyed3.load(self.path + song)
                            name = get_title(song)
                            lyrics = music.tag.lyrics[-1].text
                            print(f'这是《{name}》的歌词~\n')
                            print(lyrics)
                        except IndexError:
                            print(f'《{name}》没有歌词哟')
                        finally:
                            if i < len(self.song_list) - 1:
                                print(separator)
                            else:
                                print()
            else:
                print('没有歌词哦')

    def next(self, nth = 1):
        '''Should be called when lyrics given are undesired.
           Remove the first lyrics and display the next.
           @parmas:
               nth: jump to the nth lyrics after the first one.'''
        if self.is_file:
            if nth >= len(self.lyrics_list):
                print('没有那么多歌词哦')
                return
            self.lyrics_list = self.lyrics_list[nth:]
            self.lyrics = self.lyrics_list[0]
            self.set(self.title, self.artist, src = self.lyrics, ow = True)
            print(f'已经帮您把歌词设置为第{nth}条歌词辣\n~')
        else:
            print('无法变更哦')