from django.contrib import admin
from voting.models import VoteCart, Vote, VoteStatus, VoteMessage
from voting.moremodels import Category

admin.site.register(Category)
admin.site.register(VoteCart)
admin.site.register(Vote)
admin.site.register(VoteStatus)
admin.site.register(VoteMessage)
