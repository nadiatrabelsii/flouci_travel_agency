from travel_app.models import TravelNews

class TravelScraperPipeline:
    def process_item(self, item, spider):
        TravelNews.objects.create(
            title=item['title'],
            url=item['url'],
        )
        return item