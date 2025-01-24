from django.db import models

from django.db import models

class TravelPackage(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    themes = models.CharField(max_length=255, blank=True, default="") 

    def __str__(self):
        return self.name

    def get_themes(self):
        return self.themes.split(",") if self.themes else []

    def get_themes_vector(self):
        all_themes = ['beach', 'adventure', 'nature', 'relax', 'culture'] 
        package_themes = self.get_themes()
        return [1 if theme in package_themes else 0 for theme in all_themes]


class UserActivity(models.Model):
    user_id = models.CharField(max_length=255)
    action = models.CharField(max_length=255)  
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    feedback_score = models.IntegerField(null=True, blank=True)
    package = models.ForeignKey(TravelPackage, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user_id} - {self.action}"


class TravelNews(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.title
        
