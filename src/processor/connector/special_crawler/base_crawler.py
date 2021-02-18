
class BaseCrawler:
    def __init__(self, resources, **kwargs):
        self.resources = resources
        self.resource_types = {}

    def check_for_special_crawl(self, resource_type):
        """ 
        check the resource type need special crawling or not. if it need special crawling then 
        it will process the special crawler and returns the updated resources
        """
        return self.resources