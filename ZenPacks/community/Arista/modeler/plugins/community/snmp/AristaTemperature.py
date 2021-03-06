#
# Copyright (c) 2015, Arista Networks, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#  - Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#  - Neither the name of Arista Networks nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL ARISTA NETWORKS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#
#    Version 0.7.0  - 4/29/2015
#    Written by:
#       Jeremy Georges - Arista Networks
#       jgeorges@arista.com
#
#    Revision history:
#       0.7.0 - initial release
#
# Modeler for switch Temperature Sensors



import logging
log = logging.getLogger('zen.Arista')

from Products.DataCollector.plugins.CollectorPlugin \
    import SnmpPlugin, GetMap, GetTableMap

from Products.DataCollector.plugins.DataMaps import MultiArgs, ObjectMap



class AristaTemperature(SnmpPlugin):
    relname = 'temperature_sensors'
    modname = 'ZenPacks.community.Arista.AristaTemperature'
    snmpGetTableMaps = (
        GetTableMap('entPhysicalTable',
                    '.1.3.6.1.2.1.47.1.1.1.1',
                    {
                        '.2': 'entPhysicalDescr',
                    }
        ),
    )    

    def process(self, device, results, log):
        import re
        temp_sensors = results[1].get('entPhysicalTable',{})
        rm = self.relMap()
        for snmpindex, row in temp_sensors.items():
            name = row.get('entPhysicalDescr')
            if not name:
                log.warn('ignore sensor with no name')
                continue
            # We want to only include the sensors that have 'temp sensor' in description
            if not re.findall("temp sensor.*", name):
                continue
 
            #Need to add another check for name to include 'temp'
            om = self.objectMap()
            #Sanitize name
            om.id = self.prepId(name) 
            om.title = name
            om.snmpindex = snmpindex.strip('.')
            rm.append(om)

        log.info('Modeler %s processing data for device %s',self.name(), device.id)
        
        return rm
