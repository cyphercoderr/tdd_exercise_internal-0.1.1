from django.db import models

# Create your models here.
class Entry(models.Model):
  entry_text = models.CharField(max_length=255)

  def __str__(self):
    return f"{self.entry_text}"

class Puzzle(models.Model):
  title = models.CharField(max_length=255, default='Untitled')
  date = models.DateField()
  byline = models.CharField(max_length=255, default='Unknown')
  publisher = models.CharField(max_length=50)

  def __str__(self):
    return f"Publisher: {self.publisher}, Date: {self.date}"


class Clue(models.Model):
  clue_text = models.CharField(max_length=255)
  entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
  puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE, default=1)

  def __str__(self):
    return f"{self.entry.entry_text} - {self.clue_text}"
