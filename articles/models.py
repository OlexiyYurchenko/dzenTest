from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from PIL import Image
import os
# Create your models here.

class Comments(MPTTModel):
    user_name = models.CharField(_('User Name'), max_length=128)
    email = models.EmailField(_('E-mail'), max_length=128)
    home_page = models.URLField(max_length=200, null=True, blank=True) 
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    text = models.CharField(_('text'), max_length=4096)
    browser_info = models.CharField(max_length=4096, blank=True)
    ip = models.CharField(max_length=4096, blank=True)
    img = models.FileField(blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.user_name
    
    def save(self):
        super().save()

        if self.img.name:
            ext = os.path.splitext(self.img.name)[1]

            if ext.lower() != '.txt':
                img_new = Image.open(self.img.path)

                if (img_new.height > 320 or img_new.width > 240) and img_new:
                    output_size = (320, 320)
                    img_new.thumbnail(output_size)
                    img_new.save(self.img.path)

    class MPTTMeta:
        order_insertion_by = ['-created_at']