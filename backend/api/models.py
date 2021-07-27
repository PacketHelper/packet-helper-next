from django.db import models


class Hexes(models.Model):
    Hex = models.TextField()
    Likes = models.PositiveIntegerField(default=0)
    Dislikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return (
            f"{self.Hex[:10]}... Likes|Dislikes: {str(self.Likes)}|{str(self.Dislikes)}"
        )
