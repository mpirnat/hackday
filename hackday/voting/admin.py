from django.contrib import admin
from hackday.voting.models import VoteCart, Vote, VoteStatus, VoteMessage
from hackday.voting.moremodels import Category

admin.site.register(Category)
#admin.site.register(VoteCart)
#admin.site.register(Vote)
admin.site.register(VoteStatus)
#admin.site.register(VoteMessage)
