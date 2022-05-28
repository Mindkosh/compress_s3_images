FROM mindkosh/minimal_pillow:latest

ADD python/rotate_and_save.py /
ADD python/utils.py /

ENTRYPOINT ["python", "./rotate_and_save.py"]