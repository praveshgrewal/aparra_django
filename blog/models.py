from django.db import models
from store.models import generate_id


class BlogPost(models.Model):
    STATUS_CHOICES = [('draft', 'Draft'), ('published', 'Published'), ('archived', 'Archived')]

    id = models.CharField(max_length=50, primary_key=True, default=generate_id)
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, unique=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    featured_image_url = models.CharField(max_length=500, blank=True)
    author = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    category_ids = models.JSONField(default=list, blank=True)
    related_post_ids = models.JSONField(default=list, blank=True)
    theme = models.CharField(max_length=50, blank=True, null=True)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
