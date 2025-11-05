from django.db.models import Count, Q
from .models import Blog, Reaction

def get_profile_stats(user):
    return user.blog_set.aggregate(
        total_posts=Count('id'),
        total_likes=Count('reactionid', filter=Q(reactiontype=Reaction.LIKE)),
        total_dislikes=Count('reactionid', filter=Q(reactiontype=Reaction.DISLIKE)),
    )