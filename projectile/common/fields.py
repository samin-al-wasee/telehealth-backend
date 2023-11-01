import time
import datetime

from sorl.thumbnail import ImageField

from rest_framework import serializers
    

class TimestampImageField(ImageField):
    def generate_filename(self, instance, filename):
        """
        Add unique timestamp at beginning of the file to avoid naming collisions.
        """
        time_ = time.time()
        date_ = datetime.datetime.fromtimestamp(time_).strftime("%Y%m%d-%H%M%S")
        filename_ = f"{date_}-{filename}"
        return super(TimestampImageField, self).generate_filename(instance, filename_)


class FileSizeField(serializers.Field):
    def to_representation(self, value):
        # Convert bytes to kilobytes, megabytes, etc.
        
        sizes = ['B', 'KB', 'MB', 'GB', 'TB']
        index = 0
        size = float(value)
        while size >= 1024 and index < len(sizes) - 1:
            size /= 1024
            index += 1
        return '{:.1f} {}'.format(size, sizes[index])
    