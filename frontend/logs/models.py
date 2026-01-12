from djongo import models

class PredictionLog(models.Model):
    _id = models.ObjectIdField()
    endpoint = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    input = models.JSONField()
    prediction = models.CharField(max_length=100)
    client = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.timestamp} - {self.endpoint}"