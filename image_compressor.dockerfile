FROM mindkosh/minimal_pillow:latest

ADD python/compress_images.py /
ADD python/utils.py /

ENTRYPOINT ["python", "./compress_images.py"]