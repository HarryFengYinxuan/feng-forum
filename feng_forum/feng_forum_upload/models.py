from django.db import models


def user_upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class UploadedMedia(models.Model):
    '''
    用户可以上传的多媒体。
    '''

    name = models.CharField('文件名', max_length=10, blank=True)
    content = models.TextField('描述', max_length=500, blank=True)
    user = models.ForeignKey('feng_forum_user.User', 
                             related_name='uploadedmedia_user',
                             on_delete=models.CASCADE)
    is_icon = models.BooleanField(default=False)

    uploaded_file = models.FileField('上传的文件', upload_to=user_upload_path,      
                                     null=True, blank=True)
    uploaded_img = models.ImageField('上传的图像', upload_to=user_upload_path, 
                                     blank=True, null=True)
    uploaded_vid = models.ImageField('上传的视频', upload_to=user_upload_path,      
                                     blank=True, null=True)


    class Meta:
        verbose_name = '被上传的多媒体'
        verbose_name_plural = verbose_name


    def __str__(self,):
        return self.name