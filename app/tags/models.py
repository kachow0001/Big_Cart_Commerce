from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)

        return TaggedItem.objects \
            .select_related('tag') \
            .filter(
                content_type=content_type,
                object_id=obj_id
            )
# Create your models here.
class Tag(models.Model):
    label = models.CharField(max_length=255)
    
    def __str__(self):
        return self.label

class TaggedItem(models.Model):
    objects = TaggedItemManager()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
    # Type Product (later for videos, audios)
    # id
    # Adding ContentType, we can add generic relations to other models
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    
    # To identify ANY tagged product in the table RECORD
    content_object = GenericForeignKey()  # Corrected usage by adding parentheses

