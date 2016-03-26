from django.contrib import admin
from django_iot.apps.interactions.models import TwitterVote


class TwitterVoteAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'hashtag', 'winner', 'n_votes_winner', 'n_votes_total']


admin.site.register(TwitterVote, TwitterVoteAdmin)
