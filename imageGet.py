import requests as req
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from urllib.request import urlopen
import ssl
import time

from naver_image_crwling import NaverImageCrwling
from ret_chrome_obj import ChromeDriverObj

#
# python study
# 작성일 : 20200822
# 작성자 : 김준현
# =========================
#

class ImageGet:


    def __init__(self):

        self.config = NaverImageCrwling.get_information()
        self.chrome_driver = None
        self.cllct_time = time.strftime("%Y%m%d", time.localtime())

    def get_image_data(self):
        """

        :return:
        """
        if self.config["result"]:

            sess = req.Session()

            try:
                response = sess.get(url=self.config["data"]["hosts"])
            except req.exceptions.ConnectionError as err:
                print(err)
                sess.close()
            else:
                if response.status_code == 200 and response.ok:

                    self.chrome_driver = ChromeDriverObj.get_chrome_obj()
                    self.chrome_driver.get(url= self.config["data"]["hosts"])
                    self.chrome_driver.implicitly_wait(3)

                    ## iframe 처리 start >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    editor = self.chrome_driver.find_element_by_css_selector("iframe#da_iframe_time")
                    self.chrome_driver.switch_to.frame(editor)
                    response = self.chrome_driver.find_element_by_css_selector("div#addiv.ad > a#ac_banner_a > img")

                    try:
                        url = response.get_attribute("src")
                        print(url)
                    except:
                        pass
                    else:
                        self.image_download(url= url)

                    ## iframe 처리 end   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    self.chrome_driver.switch_to.default_content()

                    sess.close()
                    self.chrome_driver.close()

            finally:
                sess.close()

        else:
            print ("파일이 존재 하지 않는다.")

    def image_download(self, url):
        """

        :param url:
        :return:
        """
        # https ssl 처리
        context = ssl._create_unverified_context()

        try:

            html = urlopen(url, context=context)
        except:
            print ("request fail !!")
            pass
        else:

            with open("./result_image/naver_image_{}.jpg".format(self.cllct_time), "wb") as f:
                f.write(html.read())
                f.close()

            print ("image download success")


if __name__ == "__main__":
    image_object = ImageGet()
    image_object.get_image_data()