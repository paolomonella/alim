#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
'''Source:
    https://stackoverflow.com/questions/299588/validating-with-an-xml-schema-in-python
    '''
from lxml import etree


class Validator:

    # def __init__(self, xsd_path):
    # My edit:
    def __init__(self, dtd_path):
        # My edit:
        # xmlschema_doc = etree.parse(xsd_path)
        self.dtd = etree.DTD(dtd_path)
        # self.xmlschema = etree.XMLSchema(dtd)

    def validate(self, xml_path):
        xml_doc = etree.parse(xml_path)
        result = self.dtd.validate(xml_doc)
        # result = self.xmlschema.validate(xml_doc)
        return result

    def errors(self, xml_path):
        return self.dtd.error_log.filter_from_errors()[0]
        # self.dtd.error_log.filter_from_errors()


'''
dtd = etree.DTD('/home/ilbuonme/voluminosi/0.foo/2020-03-10_alim/tei_all.dtd')
infile = ('/home/ilbuonme/voluminosi/0.foo/2020-03-10_alim/in/'
          'letterarie/[JC-00179] Anonymus - Annales breves Veronenses.xml')
tree = etree.parse(infile)
print(dtd.validate(tree))
'''
