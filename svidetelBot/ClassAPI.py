import requests
import numpy as np
import re
import datetime



class API:
    def __init__(self, domain):
        self.news = {}
        self.domain = domain
        self.news["today"] = self.getPosts()
        self.news["autoberdskNews"] = self.getDTP_autoberdsk()
        self.rubricks = self.getAllRubricks()
        self.updateTimeAutoberdsk = datetime.datetime.now()
        self.updatePosts = datetime.datetime.now()






    def getPosts(self):

        allPosts = np.array(requests.get("https://"+self.domain+f"/wp-json/wp/v2/posts").json())
        return self.compareToToday(allPosts)

    def getDTP_autoberdsk(self):
        news = np.array(requests.get("http://autoberdsk.ru/wp-json/wp/v2/posts?categories=3").json())

        return list(map(lambda x:{"id":x["id"], "title":x["title"]["rendered"], "link":x["link"], "content":x["content"]["rendered"], "tags":x["tags"], "categories":x["categories"], "date":re.sub('-','.',x["date"])[:10]}, news))


    def getRubrickNews(self, id):
        if id==3:

            if (datetime.datetime.now() - self.updateTimeAutoberdsk).seconds > 300:

                self.updateTimeAutoberdsk = datetime.datetime.now()
                self.news["autoberdskNews"] =  self.getDTP_autoberdsk()
            return list(map(lambda x:[x["id"],x["title"], re.sub('-','.',x["date"])[:10]], self.news["autoberdskNews"]))
        allPosts = np.array(requests.get("https://" + self.domain + f"/wp-json/wp/v2/posts?categories={id}").json())
        return list(map(lambda x:[x["id"],x["title"]["rendered"], re.sub('-','.',x["date"])[:10]], allPosts))

    def getNew(self, id):
        res = requests.get("https://" + self.domain + f"/wp-json/wp/v2/posts/{id}").json()
        try:
            return [res["link"], res["title"]["rendered"], res["content"]["rendered"], re.sub('-','.',res["date"])[:10], res["id"]]
        except KeyError:
            try:
                res = requests.get(f"http://autoberdsk.ru/wp-json/wp/v2/posts/{id}").json()
                return [res["link"], res["title"]["rendered"], res["content"]["rendered"],
                    re.sub('-', '.', res["date"])[:10], res["id"]]
            except KeyError:
                return None


    def getAllRubricks(self):
        allRubricks = np.array(requests.get("https://" + self.domain + f"/wp-json/wp/v2/categories").json())
        dict = {}
        for x in allRubricks:
            dict[x["id"]] = x["name"]
        dict.pop(1)
        dict.pop(8)
        dict.pop(29)

        dict.update({
            51: 'Образование',
            7: 'Происшествия',
            1038: 'Право',
            25: 'Спорт',
            23: 'Культура', })

        return dict

    def get_todayNews(self):

        if (datetime.datetime.now() - self.updatePosts).seconds > 300:

            self.updatePosts = datetime.datetime.now()
            self.news["today"] = self.getPosts()
        return list(map(lambda x: [x['id'], str(x["title"]), x["date"]], self.news["today"]))

    def compareToToday(self, jsonRes):

        news = np.array(jsonRes)
        """
        today = datetime.datetime.now().date()
        for new in jsonRes:

            if new["date"][:10] == str(today):
                news = np.append(news, new)
        """
        return list(map(lambda x:{"id":x["id"], "title":x["title"]["rendered"], "link":x["link"], "content":x["content"]["rendered"], "tags":x["tags"], "categories":x["categories"], "date":re.sub('-','.',x["date"])[:10]}, news))



