import yaml
import os

#
# 작성일 : 20200822
# 작성자 : 김준현
#

class NaverImageCrwling():

    FILE_PATH = "./get_info/info.yml"

    @classmethod
    def get_information(cls):
        result = os.path.isfile( NaverImageCrwling.FILE_PATH )
        if result:
            with open(NaverImageCrwling.FILE_PATH, "r", encoding="utf-8") as fr:
                info = yaml.safe_load(fr)
                fr.close()
                return {"result": True, "data": info}
        else:
            return {"result": False, "data": None}