
import unittest

from lxml import etree

from spyne.util.xml import get_xml_as_object

from kontes.db import Package


SAMPLE_OPF_DOC = """
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="uuid_id">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/"
              xmlns:opf="http://www.idpf.org/2007/opf">
        <dc:identifier opf:scheme="calibre" id="calibre_id">8</dc:identifier>
        <dc:identifier opf:scheme="uuid" id="uuid_id">
            7b48b711-c746-4091-983e-7c3a3fb045c3
        </dc:identifier>
        <dc:identifier opf:scheme="ISBN">
            978-0-307-59019-0
        </dc:identifier>

        <dc:title>The Penguin and the Leviathan</dc:title>
        <dc:creator opf:file-as="Benkler, Yochai" opf:role="aut">Yochai Benkler</dc:creator>
        <dc:contributor opf:file-as="calibre" opf:role="bkp">calibre (0.9.27) [http://calibre-ebook.com]</dc:contributor>
        <dc:date>2011-08-08T21:00:00+00:00</dc:date>
        <dc:description>&lt;p&gt;</dc:description>
        <dc:publisher>Crown Publishing Group</dc:publisher>
        <dc:language>eng</dc:language>
        <meta content="{&quot;Yochai Benkler&quot;: &quot;&quot;}" name="calibre:author_link_map"/>
        <meta content="2013-04-02T12:15:21+00:00" name="calibre:timestamp"/>
        <meta content="Penguin and the Leviathan, The" name="calibre:title_sort"/>
    </metadata>
    <guide>
        <reference href="Penguin and the Leviathan, The - Yochai Benkler.jpg" title="Cover" type="cover"/>
    </guide>
</package>
"""

class TestOpf(unittest.TestCase):
    def test_parse(self):
        package = get_xml_as_object(etree.fromstring(SAMPLE_OPF_DOC), Package)
