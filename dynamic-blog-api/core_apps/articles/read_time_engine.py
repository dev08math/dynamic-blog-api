class ArticleReadEngine:
    def __init__(self, article):    # passing an article obj as input parameter
        self.article = article
        self.wpm = 60 # words per minute constant
        self.banner_adjustment_time = round(1/6, 3) # 0.167 contant time for adjusting....

    def check_if_article_has_banner_image(self):
        has_banner_image = True
        if not self.article.banner_image:
            has_banner_image = False
            self.banner_adjustment_time = 0
        return has_banner_image
    
    def get_title(self):
        return self.article.title
    
    def get_tags(self):
        tag_list = []
        tag_list.extend([tag_word.split() for tag_word in self.article.list_of_tags ])
        return tag_list
    
    def get_body(self):
        return self.article.body

    def get_description(self):
        return self.article.description
    
    def get_article_details(self):
        details = []
        details.extend(self.get_title().split())
        details.extend(self.get_description().split())
        details.extend(self.get_body()) # dont know whether i have to split it or not
        details.extend(self.get_tags())
        return details
    
    def get_read_time(self):
        word_length = len(self.get_article_details()) # will correctly work only if i put split() in get_body
        read_time = ""
        self.check_if_article_has_banner_image()

        if word_length:
            time_to_read = word_length / self.wpm
            if time_to_read < 1: read_time += str(round(time_to_read + self.banner_adjustment_time)*60) + "second(s)"
            else : read_time += str(round(time_to_read + self.banner_adjustment_time)) + "minute(s)"
        return  read_time

    