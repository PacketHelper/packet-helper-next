from django.db import models


class Hexes(models.Model):
    hex = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return (
            f"{self.hex[:10]}... Likes|Dislikes: {str(self.likes)}|{str(self.dislikes)}"
        )
