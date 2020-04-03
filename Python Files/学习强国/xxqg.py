
from appium import webdriver
# from ez import ez
import ez
import json
import utils, time, random
import os

class Xuexiqiangguo:
    def __init__(self):
        self.timeout = 600
        self.prevent_timeout = 0.1 * self.timeout
        self.config()

    def config(self):
        self.artical_counter = 6
        self.article_time = 12 * 60
        self.audio_counter = 6
        self.audiuo_time = 18 * 60
        self.collect_counter = 2
        self.share_counter = 1
        self.subscription_counter = 2
        self.comment_counter = 2
        self.articles = []
        self.audio = []

    def connect(self):
        self.driver = webdriver.Remote('http://0.0.0.0:4723/wd/hub', {
            "automationName": "uiautomator2",
            "platformName": "ANDROID",
            "noReset": True,
            "unicodeKeyboard": True,
            "resetKeyboard": True,
            "deviceName": "Phone",
            "appPackage": "cn.xuexi.android",
            "appActivity": "com.alibaba.android.rimet.biz.SplashActivity",
            "newCommandTimeout": self.timeout
        })
        print('已连接！')

    def read_article(self):
        # 收藏
        while self.collect_counter:
            print('点击收藏')
            star = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.ImageView[1]'
            self.collect_counter -= utils.click(self.driver, star)
            time.sleep(random.uniform(1, 2))
            # 可能会有”我知道了“的提示
            if utils.click(self.driver, 'cn.xuexi.android:id/btn_right_text'):
                time.sleep(random.uniform(1, 2))
            # 取消收藏
            print(f'取消收藏')
            utils.click(self.driver, star)
            time.sleep(random.uniform(1, 2))
        while self.share_counter:
            print('点击分享')
            utils.click(self.driver, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.ImageView[2]')
            time.sleep(random.uniform(1, 2))
            # 分享到微信
            if utils.click(self.driver, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.support.v4.view.ViewPager/android.widget.GridView/android.widget.RelativeLayout[1]/android.widget.ImageView'):
                self.share_counter -= 1
            self.driver.back()
        while self.comment_counter:
            print('评论')
            if utils.click(self.driver, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView'):
                # 发评论
                utils.set_text(self.driver, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.EditText', '中国加油！！')
                utils.click(self.driver, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.TextView[2]')
                # 删评论
                utils.click(self.driver, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout[1]/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.LinearLayout[3]/android.widget.LinearLayout[3]/android.widget.TextView[3]')
                self.comment_counter -= 1
                if self.comment_counter:
                    time.sleep(10)
        print('开始阅读')
        self.wait(read_time := random.uniform(115, 125))
        print(f'读了{round(read_time, 2)}秒', end='\r', flush=True)
        self.article_time -= read_time
        self.driver.back()

    def play_video(self, item):
        title = utils.get_text(self.driver, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.TextView')
        print(f'点开了视频《{title}》')
        duration = utils.get_text(self.driver, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout[2]/android.widget.TextView')
        duration_text = duration.split(' / ')[1].split(':')
        duration = int(duration_text[0]) * 60 + int(duration_text[1])
        print(f'这个视频要看：{duration}秒')
        utils.click(self.driver, item)
        self.wait(duration)
        self.audiuo_time -= duration

    def wait(self, duration):
        timer = int(duration) + 1
        start = time.time()
        while timer > 0:
            time.sleep(1)
            # 防止超时
            if int(time.time() - start) % self.timeout == self.prevent_timeout:
                operation_start_time = time.time()
                utils.swipe_left(self.driver)
                timer -= int(time.time() - operation_start_time)
            timer -= 1
            print(f'预计还要{timer}秒', end='\r', flush=True)

    def subscribe(self):
        print('开始订阅')
        utils.click(self.driver, 'cn.xuexi.android:id/comm_head_xuexi_mine')
        utils.click(self.driver, 'cn.xuexi.android:id/my_subscribe_tv')
        utils.click(self.driver, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.TextView[2]')
        time.sleep(2)
        tmp = 'tmp.png'
        while self.subscription_counter:
            element = utils.find_element(self.driver, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.support.v4.view.ViewPager/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.FrameLayout[1]/android.widget.LinearLayout[2]/android.widget.ImageView')
            element.save_screenshot(tmp)
            if utils.compare_images(tmp, 'checked.png'):
                utils.swipe_up(self.driver, y_ratio=5/9)
                if utils.find_element(self.driver, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.support.v4.view.ViewPager/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView'):
                    print('看到底线了')
                    utils.click(self.driver, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.support.v7.app.ActionBar.Tab[2]/android.widget.TextView')
            else:
                if utils.click(self.driver, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.support.v4.view.ViewPager/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.FrameLayout[1]/android.widget.LinearLayout[2]'):
                    self.subscription_counter -= 1
                    print(f'订阅了：{utils.get_text(self.driver, "")}')

    def run(self):
        while True:
            try:
                self.connect()
                time.sleep(6) # Splash Screen

                utils.swipe_left(self.driver, y_ratio=3/4)
                print('开始读要闻')
                for i in range(1, self.artical_counter + 1):
                    item = f'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.support.v4.view.ViewPager/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.FrameLayout[1]/android.widget.LinearLayout'
                    title = utils.get_text(self.driver, item + '/android.widget.TextView')
                    utils.click(self.driver, item)
                    print(f'点开了文章《{title}》')
                    if title and title not in self.articles:
                        self.read_article()
                        self.articles.append(title)
                        print(f'读完惹，还有{self.artical_counter - i}篇要读')
                    else:
                        utils.swipe_up(self.driver, y_ratio=5/9)
                if self.article_time > 0:
                    read_time = random.uniform(self.article_time, self.article_time + 2)
                    print(f'读完了，但距离完成任务还有{round(self.article_time, 2)}秒，所以随便等个{round(read_time, 2)}秒')
                    self.wait(read_time)

                # 本地频道内功能
                if utils.click(self.driver, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.support.v4.view.ViewPager/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[4]'):
                    utils.click(self.driver, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.support.v4.view.ViewPager/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.FrameLayout/android.support.v7.widget.RecyclerView/android.widget.LinearLayout[1]')
                    self.driver.back()

                while not utils.click(self.driver, '//android.widget.FrameLayout[@content-desc="百灵"]/android.widget.RelativeLayout'):
                    time.sleep(1)
                utils.click(self.driver, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.support.v4.view.ViewPager/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView')
                print('开始看视频')

                for i in range(1, self.audio_counter + 1):
                    self.play_video()
                    print(f'看完惹，还有{self.audio_counter - i}个要看')
                if self.audiuo_time > 0:
                    print(f'虽然视频看完了，但是还剩下{int(self.audiuo_time)}秒，所以再看看别的')
                    self.wait(random.uniform(self.audiuo_time, self.audiuo_time + 1))
                self.driver.back()

                # self.subscribe()
                print('搞定啦~')
                break
            except KeyboardInterrupt:
                break
            except Exception as e:
                print('Exception:', e)
            finally:
                self.driver.quit()

if __name__ == '__main__':
    x = Xuexiqiangguo()
    x.run()

    ez.cddt()
    ez.cd('Win-Mac/xuexiqiangguo')