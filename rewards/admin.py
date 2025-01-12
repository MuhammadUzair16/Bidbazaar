from django.contrib import admin
from .models import RewardPool, UserRewardPoints, RewardTransaction

admin.site.register(RewardPool)
admin.site.register(UserRewardPoints)
admin.site.register(RewardTransaction)
