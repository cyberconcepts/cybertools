=================
Report Management
=================

  ($Id$)

  >>> from zope import component
  >>> from cybertools.composer.report.base import ReportManager, Report

  >>> manager = ReportManager()

  >>> rep01 = manager.addReport(Report('testreport'))

The base report provides a fairly basic collection of field definitions:

  >>> len(rep01.fields)
  1
  >>> rep01.fields.keys()
  ['label']
  >>> rep01.fields.get('label')
  <cybertools.composer.report.field.Field object ...>
  >>> rep01.fields.get('title')
