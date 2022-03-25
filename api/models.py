from django.db import models

class DailySummaryPrice(models.Model):
    name = 'daily_summary_price'
    verbose_name = 'daily summary price' 
    class Meta:
        db_table = 'daily_summary_price'
    pair = models.CharField(max_length=10)
    timestamp = models.IntegerField()
    mms_20 = models.FloatField(null=True, blank=True)
    mms_50 = models.FloatField(null=True, blank=True)
    mms_200 = models.FloatField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.pair}, {self.timestamp}, {self.mms_20}, {self.mms_50}, {self.mms_200}'  
