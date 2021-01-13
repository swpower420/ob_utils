import os
from icrawler.builtin import GoogleImageCrawler, BaiduImageCrawler, BingImageCrawler

crawl_dir = "google크롤링\\test"


def checked_dir_and_get_path(dir_name):
    dir_path = os.path.join(crawl_dir, dir_name)

    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    return dir_path


google_path = checked_dir_and_get_path("google")
# baidu_path = checked_dir_and_get_path("baidu")
# bing_path = checked_dir_and_get_path("bing")

google_crawler = GoogleImageCrawler(
    feeder_threads=1,
    parser_threads=2,
    downloader_threads=4,
    storage={'root_dir': google_path})

filters = dict(
    type="photo",
    size='large',
    # color='white',
    # license='commercial,modify',
    # date=((2000, 1, 1), (2019, 8, 27))
)

keyword = ""
google_crawler.crawl(keyword=keyword, filters=filters, max_num=200, file_idx_offset=0)

# filters = dict(
#     type="photo",
#     size='large',
#     # license='commercial,modify',
#     date="pastyear")
# bing_crawler = BingImageCrawler(downloader_threads=4,
#                                 storage={'root_dir': bing_path})
# bing_crawler.crawl(keyword=keyword, filters=filters, offset=0, max_num=100)

# baidu_crawler = BaiduImageCrawler(storage={'root_dir': baidu_path})
# baidu_crawler.crawl(keyword=keyword, offset=0, max_num=100, min_size=(200,200), max_size=None)