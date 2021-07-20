from django.db import models

class Hexes(models.Model):
    hex = models.TextField()
    like = models.PositiveIntegerField(default=0)
    unlike = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.hex[:10]  + "... Likes|Unlikes: " + str(self.like) + "|" + str(self.unlike)