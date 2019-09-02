from django.db import models
from django.db.models import *
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import User
import logging
from time import strftime
import uuid
from django.utils.text import slugify
import os
import shutil
from dfirtrack_main import models as main_models
from dfirtrack.config import EVIDENCE_PATH

# get active user model
User = get_user_model()

# initialize logger
stdlogger = logging.getLogger(__name__)

class Artifact(models.Model):
    ''' Model used for storing a forensic artifact '''

    # primary key
    artifact_id = models.AutoField(primary_key=True)

    # foreing key(s)
    artifactstatus = models.ForeignKey('Artifactstatus', on_delete=models.PROTECT, default=1)
    artifacttype = models.ForeignKey('Artifacttype', on_delete=models.PROTECT)
    case = models.ForeignKey('dfirtrack_main.Case', related_name='artifact_case',on_delete=models.PROTECT, blank=True, null=True)
    system = models.ForeignKey('dfirtrack_main.System', related_name='artifact_system',on_delete=models.PROTECT)

    # main entity information
    artifact_acquisition_time = models.DateTimeField(blank=True, null=True)
    artifact_md5 = models.CharField(max_length=32, blank=True, null=True)
    artifact_name = models.CharField(max_length=4096)
    artifact_note = models.TextField(blank=True, null=True)
    artifact_requested_time = models.DateTimeField(blank=True, null=True)
    artifact_sha1 = models.CharField(max_length=40, blank=True, null=True)
    artifact_sha256 = models.CharField(max_length=64, blank=True, null=True)
    artifact_slug = models.CharField(max_length=4096)
    artifact_source_path = models.CharField(max_length=4096, blank=True, null=True)
    artifact_storage_path = models.CharField(max_length=4096, unique=True)
    artifact_uuid = models.UUIDField(editable=False)

    # meta information
    artifact_create_time = models.DateTimeField(auto_now_add=True)
    artifact_modify_time = models.DateTimeField(auto_now=True)
    artifact_created_by_user_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='artifact_created_by')
    artifact_modified_by_user_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='artifact_modified_by')

    # set the ordering criteria
    class Meta:
        ordering = ('artifact_name', )

    # string representation
    def __str__(self):
        return 'Artifact {0} ({1})'.format(str(self.artifact_id), self.system)
        
    def __unicode__(self):
        return u'%s' % self.artifact_name

    # define logger
    def logger(artifact, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " artifact_id:" + str(artifact.artifact_id) +
            "|artifact_name:" + str(artifact.artifact_name) +
            "|artifactstatus:" + str(artifact.artifactstatus.artifactstatus_name) +
            "|artifacttype:" + str(artifact.artifacttype.artifacttype_name) +
            "|system:" + str(artifact.system) +
            "|case:" + str(artifact.case) +
            "|artifact_note:" + str(artifact.artifact_note) +
            "|artifact_slug:" + str(artifact.artifact_slug) +
            "|artifact_requested_time:" + str(artifact.artifact_requested_time) +
            "|artifact_acquisition_time:" + str(artifact.artifact_acquisition_time) +
	    "|artifact_md5:" + str(artifact.artifact_md5) +
	    "|artifact_sha1:" + str(artifact.artifact_sha1) +
	    "|artifact_sha256:" + str(artifact.artifact_sha256) +
	    "|artifact_source_path:" + str(artifact.artifact_source_path) +
	    "|artifact_storage_path:" + str(artifact.artifact_storage_path) +
	    "|artifact_uuid:" + str(artifact.artifact_uuid)
        )

    def save(self, *args, **kwargs):
        # generate slug
        self.artifact_slug = slugify(self.artifact_name)

        # check for new artifact
        if not self.pk:
            """ tasks only to perform for a new artifact """

            # generate uuid type4 (completely random type)
            self.artifact_uuid = uuid.uuid4()

            # generate the artifact storage path within EVIDENCE_PATH
            self.artifact_storage_path = self.create_artifact_storage_path(self.system.system_uuid, self.artifacttype.artifacttype_slug, self.artifact_uuid)

        # set hashes to calculating while hash calculating is performed in background
        # self.artifact_md5 = 'Calculating...'
        # self.artifact_sha1 = 'Calculating...'
        # self.artifact_sha256 = 'Calculating...'

        ## check if the storage_path from the form is equal to the artifact_evidence_path
        #if self.artifact_storage_path != artifact_evidence_path:
        #    #TODO: We mnust change this logic, so that exception will be thrown if file does not exist
        #    #TODO: Check if we do not have file at the beginning --> calculate evidence path --> edit use new path testen
        #    # os.path.exists(self.artifact_storage_path)
        #    # check if we have a folder, then we do not need to create the dir
        #    if os.path.isdir(self.artifact_storage_path):
        #        pass
        #    elif os.path.isfile(self.artifact_storage_path):
        #        # if not we will copy the artifact to the artifact_evidence_path
        #        destination = ''
        #        destination = shutil.copy(self.artifact_storage_path, artifact_evidence_path)
        #    self.artifact_storage_path = destination
        #else:
        #    self.artifact_storage_path = artifact_evidence_path
        ##TODO: check if this works or if wee need
        ## super().save(*args,**kwargs)

        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('artifacts_artifact_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('artifacts_artifact_update', args=(self.pk,))

    def create_artifact_storage_path(self, system_uuid, artifacttype, artifact_uuid):
            """ generates the directory in which the artifact will be stored """

            # generate the path for the artifact to store it in EVIDENCE_PATH
            artifact_storage_path = (EVIDENCE_PATH + '/' + str(system_uuid) + '/' + artifacttype + '/' + str(artifact_uuid))
            # create directory if it does not exist
            if not os.path.exists(artifact_storage_path):
                os.makedirs(artifact_storage_path)
                return artifact_storage_path

class Artifactstatus(models.Model):
    ''' Artifactstatus that shows the current status of the artifact like: New, Requested, Processed, Imported, ...'''

    # primary key
    artifactstatus_id = models.AutoField(primary_key=True)

    # main entity information
    artifactstatus_name = models.CharField(max_length=255, unique=True)
    artifactstatus_note = models.TextField(blank=True, null=True)
    artifactstatus_slug = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('artifactstatus_id',)

    # string representation
    def __str__(self):
        return self.artifactstatus_name

    # define logger
    def logger(artifactstatus, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " artifactstatus_id:" + str(artifactstatus.artifactstatus_id) +
            "|artifactstatus_name:" + str(artifactstatus.artifactstatus_name) +
            "|artifactstatus_note:" + str(artifactstatus.artifactstatus_note) +
            "|artifactstatus_slug:" + str(artifactstatus.artifactstatus_slug)
        )

    def save(self, *args, **kwargs):
        # generate slug
        self.artifactstatus_slug = slugify(self.artifactstatus_name)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('artifacts_artifactstatus_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('artifacts_artifactstatus_update', args=(self.pk,))

class Artifacttype(models.Model):
    ''' Artifacttype like File, Registry-Key, Registry-Hive, etc. '''

    # primary key
    artifacttype_id = models.AutoField(primary_key=True)

    # main entity information
    artifacttype_name = models.CharField(max_length=255, unique=True)
    artifacttype_note = models.TextField(blank=True, null=True)
    artifacttype_slug = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('artifacttype_id',)

    # string representation
    def __str__(self):
        return self.artifacttype_name

    # define logger
    def logger(artifacttype, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " artifacttype_id:" + str(artifacttype.artifacttype_id) +
            "|artifacttype_name:" + str(artifacttype.artifacttype_name) +
            "|artifacttype_note:" + str(artifacttype.artifacttype_note) +
            "|artifacttype_slug:" + str(artifacttype.artifacttype_slug)
        )

    def get_absolute_url(self):
            return reverse('artifacts_artifacttype_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('artifacts_artifacttype_update', args=(self.pk,))
    
    def save(self, *args, **kwargs):
        # generate slug
        self.artifacttype_slug = slugify(self.artifacttype_name)
        return super().save(*args, **kwargs)

#TODO: Signals for DjangoQ reciever that creates the hassums
#def artifact_created()
