# encoding: utf8
#
# Copyright © Burak Arslan <burak at arskom dot com dot tr>,
#             Arskom Ltd. http://www.arskom.com.tr
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#    3. Neither the name of the owner nor the names of its contributors may be
#       used to endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

from spyne.model.primitive import Integer32
from spyne.model.primitive import AnyUri
from spyne.model.primitive import UnsignedInteger32
from spyne.model.primitive import Unicode
from spyne.model.primitive import DateTime
from spyne.model.complex import Array
from spyne.model.complex import ComplexModel
from spyne.model.complex import XmlData
from spyne.model.complex import XmlAttribute
from spyne.model.complex import TTableModel

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker

db = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=db)
TableModel = TTableModel(MetaData(bind=db))


class User(TableModel):
    __tablename__ = 'spyne_user'
    __table_args__ = {"sqlite_autoincrement": True} # sqlite-specific

    id = UnsignedInteger32(pk=True)
    user_name = Unicode(32, min_len=4, pattern='[a-z0-9.]+')
    full_name = Unicode(64, pattern='\w+( \w+)+')
    email = Unicode(64, pattern=r'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}')


class Identifier(ComplexModel):
    id = XmlAttribute(Unicode(values=['calibre_id', 'uuid_id']))
    scheme = XmlAttribute(Unicode(values=['calibre', 'uuid', 'ISBN']))
    value = XmlData(Unicode)

class MetaData(TableModel):
    __tablename__ = 'metadata'
    __table_args__ = {"sqlite_autoincrement": True} # sqlite-specific

    id = Integer32(pk=True)
    identifiers = Array(Identifier).store_as('xml')
    date = DateTime
    title = Unicode(256)
    creator = Unicode(256)
    contributor = Unicode(256)
    description = Unicode
    publisher = Unicode(256)
    language = Unicode(3)
    meta = Unicode(1, max_occurs='unbounded')
    content = XmlAttribute(Unicode, attribute_of='meta')
    name = XmlAttribute(Unicode, attribute_of='meta')


class Guide(ComplexModel):
    reference = Unicode(1)
    href = XmlAttribute(AnyUri, attribute_of='reference')
    title = XmlAttribute(Unicode(128))


class Package(TableModel):
    __tablename__ = 'package'
    __namespace__ = "http://www.idpf.org/2007/opf"
    __table_args__ = {"sqlite_autoincrement": True} # sqlite-specific
    _type_info = [
        ('id', Integer32(pk=True)),
        ('guide', Guide.store_as('xml')),
        ('metadata' , MetaData.store_as('table')),
        ('unique-identifier', Unicode(values=['uuid_id'])),
    ]


"""
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
