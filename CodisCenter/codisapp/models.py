from __future__ import unicode_literals

from django.db import models

# Create your models here.

class HostInfo(models.Model):
  HostID = models.AutoField(primary_key=True)
  HostIP = models.CharField(max_length=64)
  HostName = models.CharField(max_length=128)
  HostMem = models.IntegerField()
  Room = models.CharField(max_length=64)
  Used = models.IntegerField()
  Description = models.CharField(max_length=1024)

class CodisInfo(models.Model):
  CodisID = models.AutoField(primary_key=True)
  ProductName = models.CharField(max_length=128)
  Dashboard = models.CharField(max_length=128)
  ProjectName = models.CharField(max_length=128)
  RdOwner = models.CharField(max_length=128)
  XyVIP = models.CharField(max_length=128)
  YzVIP = models.CharField(max_length=128)
  Domain = models.CharField(max_length=128)
  Description = models.CharField(max_length=1024)

class PublicPrefix(models.Model):
  PrefixID = models.AutoField(primary_key=True)
  PrefixName = models.CharField(max_length=128)
  PrefixProject = models.CharField(max_length=128)
  OpOwner = models.CharField(max_length=128)
  RdOwner = models.CharField(max_length=128)
  AccessTime = models.CharField(max_length=128)
  Description = models.CharField(max_length=1024)
