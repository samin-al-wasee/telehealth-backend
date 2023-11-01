import logging


logger = logging.getLogger(__name__)


def post_save_patient(sender, instance, created, *args, **kwargs):
    if created:
        logger.debug(instance)
        pass


def post_save_patient_address(sender, instance, created, *args, **kwargs):
    if created:
        logger.debug(instance)
        pass


def post_delete_patient(sender, instance, *args, **kwargs):
    pass
