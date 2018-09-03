#!/usr/bin/env python

import os
from time import sleep
from pprint import pprint
from sets import Set
from shutil import copy2
from copy import copy
import sys
import argparse
import standard_utils as su
import manifest
import descriptor
import update_profile
import subcomponent_to_version_string_map as stvsm
import suu

"""
System level firmware update tool for Seagate Systems / Storage and Application Platforms

Copyright (C) 2017 Seagate Technology, Ltd.
Seagate Systems / Storage and Application Platforms

Overview
===========
Consumes several XML files which describe both the target system to be maintained as well as the firmware update and software tools packages used to perform the udpates:
- ...configuration_descriptor.xml: Describes the target system configuration(s) that will be maintained, including:
    - identification data (is this the system we're looking for?)
    - which firmware components do we want to update? (using tags which match firmware manifest files)
    - what are the tools required and commands used to query, update and activate firmware? (among other items)
    - in what order should the commands be applied?
- ...manifest.xml: Describes a firmware or tools release, including:
    - header: describes the overall release type, version, etc.
    - files: describe every file in a given release, including Automation_Tag (common across releases), directory, file name, MD5 checksum, included FW subcomponents, etc.

Current Platform Scope
======================
GOBI platforms with SUU only support (LS)

Planned Additions to Platform Scope
==========================
GOBI platforms with Yafuflash only support (SP)
Legacy platforms with XYafu+FWDownloader support (TL, BR)
Legacy platforms with FWDownlaoder only support (E12EBD, E6EBD)

Use Cases
=========

Full Automatic FW Update
- Discover Manifests, parse [COMPLETE]
- Discover Configuration Descriptor (CD), parse [COMPLETE]
- Validate Manifests against Configuration Descriptor [COMPLETE]
    - Confirm that all package_path in CD are present in Manifests
    - Call Manifest.validateFile against every referenced file
- Package manual update [COMPLETE]
    - Create a manual update folder
    - Walk through CD, look up the file name from the manifest
    - Copy all of the necessary firmware files to the manual update directory 
    - Copy all of the necessary tools files to the manual update directory
    - Generate the full commands for each update step into shell scripts
- Show Package Versions [COMPLETE]
- Perform tool execution tests (passive check for 'can I run the referenced tool in the current environment?')
- Validate Targets against CD (are these the targets I'm looking for?)
- Query Target versions based on CD (what are the versions for the components I'm interested in?) [COMPLETE]
    - Execute query commands, parse subsystem-specific version output [COMPLETE]
    - Apply version translation rules to match manifest content
    - Display a table of all instances of each subomponent in a given system
- Compare Target versions to Manifest (which components are at the expected level, which are not?) [COMPLETE]
- Create Update solution based on comparison (what is the order of required updates, and their impact?) [COMPLETE]
- Execute Update solution (actually perform the updates, checking progress throughout) [COMPLETE
"""

### Globals
version_string='2017-09-20_avid_test'
description_string='System level firmware update tool for Seagate Systems / Storage and Application Platforms'

class PackageVersion:
    """ Container to hold complete version details on a given package System::SubSystem::SubComponent from within included manifests """
    def __init__(self, subsystem_index, subsystem_automation_tag, subcomponent_name, version=None, crc=None, image=None, status=None):
        self.subsystem_index = subsystem_index
        self.subsystem_automation_tag = subsystem_automation_tag
        self.subcomponent_name = subcomponent_name
        if version is None:
            self.version = '-'
        else:
            self.version = version
        if crc is None:
            self.crc = '-'
        else:
            self.crc = crc
        if image is None:
            self.image = '-'
        else:
            self.image = image
        if status is None:
            self.status = '-'
        else:
            self.status = status

class PackageVersions:
    """ Container to hold SubComponentVersions for all SubSystems in a given System from within included manifests """
    def __init__(self):
        self.subcomponents = []
        self.count = 0
    
    def addPackageVersion(self, newsub):
        """ Append newsub to self.subcomponents """
        self.subcomponents.append(newsub)
        self.count += 1

    def getPackageVersions(self, this_descriptor, manifests, system_index):
        """ Get the SubComponent package versions or the specified sysem in the following manner:
            1. Loop through each SubSystem and SubComponent in the specified system.
            2. Apply manifest default version+crc string translation rule (strip+upper)
            3. Store the results in self.subcomponents for later display and comparison to system versions
            """
        this_system = this_descriptor.systems[system_index]
        su.info('Getting package versions for descriptor system index %i - %s' % (system_index, this_system.description))
    
        # Loop through subsystems, display manifest-translated versions of the version+crc strings (strip + convert to upper case)    
        for this_subsystem in this_system.subsystems:

            subsystem_index = this_subsystem.index
            subsystem_automation_tag = this_subsystem.automationtagpath.automationtag

            # Grab the firmware file from the manifest based on what was specified in the descriptor subsystem definition
            this_fw_file = getManifestFile(manifests, this_subsystem.automationtagpath)
        
            # Loop through the subcomponents in the subsystem, adding the Versions + CRCs from the manifest to a PackageVersion instance
            for this_subcomponent in this_subsystem.subcomponents:
                subcomponent_name = this_subcomponent.name
                # Grab the matching ManifestFile.SubComponent
                this_manifest_subcomponent = this_fw_file.getSubComponent(this_subcomponent.name)
                version = this_manifest_subcomponent.version
                if version == '':
                    version = '-'
                crc = this_manifest_subcomponent.crc
                if crc == '':
                    crc = '-'
                temp_package_version = PackageVersion(subsystem_index, subsystem_automation_tag, subcomponent_name, version, crc)
                self.addPackageVersion(temp_package_version)

    def showPackageVersions(self):
        """ Show the SubComponent system versions contained within self.subcomponents """
        
        # We will use standard_utils.pretty_table_generator, which needs a list
        temp_list = []
        
        # Create the column colors list
        column_colors = (su.c.CYAN, su.c.CYAN, su.c.GREEN, su.c.WHITE, su.c.WHITE)

        # Create the header row
        header = ('Idx', 'Automation_Tag', 'SubComponent_Name', 'Version', 'CRC')
        temp_list.append(header)
                
        # Add the subcomponents to the list
        for s in self.subcomponents:
            temp_row = (str(s.subsystem_index), s.subsystem_automation_tag, s.subcomponent_name, s.version, s.crc)
            temp_list.append(temp_row)

        # Display the list
        su.msg('')
        for line in su.pretty_table_generator(temp_list, column_colors=column_colors, delimeter='|', header_separator='='):
            su.msg(line)
        su.msg('')

class SubComponentVersion:
    """ Container to hold complete version details on a given System::Subsystem::SubComponent """
    def __init__(self, subsystem_index, subsystem_automation_tag, subcomponent_name, query_string, version=None, crc=None, image=None, status=None, mode=None, slot=None, controller_count=None, update_filters=None, notes=None):
        self.subsystem_index = subsystem_index
        self.subsystem_automation_tag = subsystem_automation_tag
        self.subcomponent_name = subcomponent_name
        self.query_string = query_string
        if version is None:
            self.version = '-'
        else:
            self.version = version
        if crc is None:
            self.crc = '-'
        else:
            self.crc = crc
        if image is None:
            self.image = '-'
        else:
            self.image = image
        if status is None:
            self.status = '-'
        else:
            self.status = status
        self.mode = mode
        self.slot = slot
        self.controller_count = controller_count
        if update_filters is None:
            self.update_filters = []
        else:
            self.update_filters = update_filters
        if notes is None:
            self.notes = []
        else:
            self.notes = notes
            
    def __repr__(self):
        return '%s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.subsystem_index, self.subsystem_automation_tag, self.subcomponent_name, self.query_string, self.version, self.crc, self.image, self.status, self.mode, self.slot, self.controller_count, str(self.update_filters), str(self.notes))

class SystemVersions:
    """ Container to hold SubComponentVersions for all SubSystems in a given System """
    def __init__(self):
        self.subcomponents = []
        self.count = 0
        self.autotarget = None
        self.notes_list = []
    
    def addSubComponentVersion(self, newsub):
        """ Append newsub to self.subcomponents """
        self.subcomponents.append(newsub)
        self.count += 1
        
    def addUpdateNote(self,new_note):
        """ Add any new unique update notes to self.notes_list """
        if new_note not in self.notes_list:
            self.notes_list.append(new_note)

    def getSystemVersions(self, this_descriptor, manifests, this_query_profile, stvsm_map, system_index, target):
        """ Get the SubComponent system versions or the specified sysem in the following manner:
            1. Loop through each SubSystem and SubComponent in the specified system.
            2. Apply the specified <Query_Profile> version+crc string translation rules from stvsm_map
            3. Fill in a SystemVersions class and return it
            """
        this_system = this_descriptor.systems[system_index]
        su.info('Getting system versions at target %s for descriptor system index %i - %s' % (target, system_index, this_system.description))
        
        # Loop through subsystems, run the specified query commands, then display translated versions of the version+crc strings (according to specified translation rules)    
        for this_subsystem in this_system.subsystems:
        
            su.debug(sys._getframe().f_code.co_name+'::%s' % this_subsystem)
            
            # Get some necessary information up front
            this_fw_file = getManifestFile(manifests, this_subsystem.automationtagpath)
            this_query_profile_object = this_query_profile.getProfile(this_subsystem.queryprofile)
            update_filters = this_subsystem.updatefilters
            
            # Run the specified SubSystem query command and store the result of automatic target detection, then parse the result
            (this_versions, this_target) = runQuery(this_subsystem , manifests, this_query_profile, target)
            self.autotarget = this_target
                    
            # Use the stvsm (map) to pick out the values we are interested in for the subcomponents in this subsystem
            for this_subcomponent in this_subsystem.subcomponents:
                subsystem_match_count = 0
                subsystem_index = this_subsystem.index
                subsystem_automation_tag = this_subsystem.automationtagpath.automationtag
                subcomponent_name = this_subcomponent.name
                for this_map in stvsm_map.getMaps(subcomponent_name, subsystem_automation_tag):
                    for this_versionstring in this_map.versionstrings:
                        matching_versions = this_versions.lookup(this_versionstring)
                        (this_mode, this_slot, this_controller_count) = (matching_versions.mode, matching_versions.slot, matching_versions.controller_count)
                        for version_entry in matching_versions.version_list:
                            subsystem_match_count += 1
                            (query_string, version, image, status, crc) = ('-', '-', '-', '-', '-')
                            if version_entry.name:
                                query_string = version_entry.name
                            if version_entry.version:
                                version = this_map.applyVersionRule(version_entry.version)
                            if version_entry.index:
                                image = version_entry.index
                            if version_entry.status:
                                status = version_entry.status
                            if version_entry.name and version_entry.version == '':
                                su.warn('Version string is empty: [%s] [%s], setting version string to MISSING' % (version_entry.name, version_entry.version))
                                version = 'MISSING'
                            this_notes = []
                            for this_filter in update_filters:
                                this_filter_note = None
                                if this_filter == 'exclude_backup':
                                    if status == 'Backup':
                                        this_filter_note = (False,'Backup images are excluded from updates')
                                        this_notes.append(this_filter_note)
                                        self.addUpdateNote(this_filter_note)
                                elif this_filter == 'slot0_only':
                                    if this_slot == '1':
                                        this_filter_note = (False,'Update only allowed from slot 0, this controller is in slot 1')
                                        this_notes.append(this_filter_note)
                                        self.addUpdateNote(this_filter_note)
                                elif this_filter == 'slot1_only':
                                    if this_slot == '0':
                                        this_filter_note = (False,'Update only allowed from slot 1, this controller is in slot 0')
                                        this_notes.append(this_filter_note)
                                        self.addUpdateNote(this_filter_note)
                                elif this_filter == 'slot0_preferred':
                                    if this_controller_count == '2' and this_slot == '1':
                                        this_filter_note = (False,'Update preferred from slot 0, this controller is in slot 1 and there are 2 controllers present')
                                        this_notes.append(this_filter_note)
                                        self.addUpdateNote(this_filter_note)
                                    elif this_controller_count is None and this_slot == '1':
                                        this_filter_note = (False,'Update preferred from slot 0, this controller is in slot 1 and the controller count is unknown')
                                        this_notes.append(this_filter_note)
                                        self.addUpdateNote(this_filter_note)
                                elif this_filter == 'slot1_preferred':
                                    if this_controller_count == '2' and this_slot == '0':
                                        this_filter_note = (False,'Update preferred from slot 1, this controller is in slot 0 and there are 2 controllers present')
                                        this_notes.append(this_filter_note)
                                        self.addUpdateNote(this_filter_note)
                                    elif this_controller_count is None and this_slot == '0':
                                        this_filter_note = (False,'Update preferred from slot 1, this controller is in slot 0 and the controller count is unknown')
                                        this_notes.append(this_filter_note)
                                        self.addUpdateNote(this_filter_note)
                            temp_subcomponent_version = SubComponentVersion(subsystem_index, subsystem_automation_tag, subcomponent_name, query_string, version, crc, image, status, 
                                                                            this_mode, this_slot, this_controller_count, update_filters, this_notes)
                            su.debug(str(temp_subcomponent_version))
                            self.addSubComponentVersion(temp_subcomponent_version)                        
                    for this_crcstring in this_map.crcstrings:
                        matching_versions = this_versions.lookup(this_crcstring)
                        (this_mode, this_slot, this_controller_count) = (matching_versions.mode, matching_versions.slot, matching_versions.controller_count)
                        for version_entry in matching_versions.version_list:
                            subsystem_match_count += 1
                            (query_string, version, image, status, crc) = ('-', '-', '-', '-', '-')
                            if version_entry.name:
                                query_string = version_entry.name
                            if version_entry.version:
                                crc = this_map.applyCRCRule(version_entry.version)
                            if version_entry.index:
                                image = version_entry.index
                            if version_entry.status:
                                status = version_entry.status
                            if version_entry.name and version_entry.version == '':
                                su.warn('CRC string is empty: [%s] [%s], setting CRC string to MISSING' % (version_entry.name, version_entry.version))
                                crc = 'MISSING'
                            this_notes = []
                            for this_filter in update_filters:
                                this_filter_note = None
                                if this_filter == 'exclude_backup':
                                    if status == 'Backup':
                                        this_filter_note = (False,'Backup images are excluded from updates')
                                        this_notes.append(this_filter_note)
                                        self.addUpdateNote(this_filter_note)
                                elif this_filter == 'slot0_only':
                                    if this_slot == '1':
                                        this_filter_note = (False,'Update only allowed from slot 0, this controller is in slot 1')
                                        this_notes.append(this_filter_note)
                                        self.addUpdateNote(this_filter_note)
                                elif this_filter == 'slot1_only':
                                    if this_slot == '0':
                                        this_filter_note = (False,'Update only allowed from slot 1, this controller is in slot 0')
                                        this_notes.append(this_filter_note)
                                        self.addUpdateNote(this_filter_note)
                                elif this_filter == 'slot0_preferred':
                                    if this_controller_count == '2' and this_slot == '1':
                                        this_filter_note = (False,'Update preferred from slot 0, this controller is in slot 1 and there are 2 controllers present')
                                        this_notes.append(this_filter_note)
                                        self.addUpdateNote(this_filter_note)
                                elif this_filter == 'slot1_preferred':
                                    if this_controller_count == '2' and this_slot == '0':
                                        this_filter_note = (False,'Update preferred from slot 1, this controller is in slot 0 and there are 2 controller present')
                                        this_notes.append(this_filter_note)
                                        self.addUpdateNote(this_filter_note)
                            temp_subcomponent_version = SubComponentVersion(subsystem_index, subsystem_automation_tag, subcomponent_name, query_string, version, crc, image, status, 
                                                                            this_mode, this_slot, this_controller_count, update_filters, this_notes)
                            su.debug(str(temp_subcomponent_version))
                            self.addSubComponentVersion(temp_subcomponent_version)
                if subsystem_match_count == 0:
                    su.warn('Failed to match subcomponent %s, setting all system string values to MISSING' % str(this_subcomponent))
                    (query_string, version, image, status, crc) = ('MISSING', 'MISSING', 'MISSING', 'MISSING', 'MISSING')
                    (this_mode, this_slot) = (None, None)
                    temp_subcomponent_version = SubComponentVersion(subsystem_index, subsystem_automation_tag, subcomponent_name, query_string, version, crc, image, status,
                                                                    this_mode, this_slot, update_filters)
                    su.warn(str(temp_subcomponent_version))
                    self.addSubComponentVersion(temp_subcomponent_version)
                            
    def showSystemVersions(self):
        """ Show the SubComponent system versions contained within self.subcomponents """

        # We will use standard_utils.pretty_table_generator, which needs a list
        temp_list = []
        
        # Create the column colors list
        column_colors = (su.c.CYAN, su.c.CYAN, su.c.GREEN, su.c.MAGENTA, su.c.WHITE, su.c.WHITE, su.c.WHITE, su.c.WHITE)

        # Create the header row
        header = ('Idx', 'Automation_Tag', 'SubComponent_Name', 'Query_String', 'Version', 'CRC', 'Img', 'Status')
        temp_list.append(header)
                
        # Add the subcomponents to the list
        for s in self.subcomponents:
            temp_row = (str(s.subsystem_index), s.subsystem_automation_tag, s.subcomponent_name, s.query_string, s.version, s.crc, s.image, s.status)
            temp_list.append(temp_row)

        # Display the list
        su.msg('')
        for line in su.pretty_table_generator(temp_list, column_colors=column_colors, delimeter='|', header_separator='='):
            su.msg(line)
        su.msg('')

class SubComponentVersionCompare:
    """ Container to hold complete version comparison details between package and system for a given System::Subsystem::SubComponent """
    def __init__(self, packagesubcomponent, systemsubcomponent):
    
        # We will modify self.pack for display purposes, so make a copy
        self.pack = copy(packagesubcomponent)
        self.sys = systemsubcomponent
        self.match = False
        self.exclude = False

        # First make sure we are comparing the same subcomponent:
        if self.pack.subsystem_automation_tag != self.sys.subsystem_automation_tag and self.pack.subcomponent_name != self.sys.subcomponent_name:
            su.warn('SubComponentVersionCompare:: attempt to compare package [%s::%s] to system [%s::%s]')
            return
        
        # Now compare the version or crc and set the match flag accordingly
        if self.sys.version == '-':
            self.pack.version = '-'
        else:
            if self.sys.version == self.pack.version:
                self.match = True
        if self.sys.crc == '-':
            self.pack.crc = '-'
        else:
            if self.sys.crc == self.pack.crc:
                self.match = True
        # Check if the update filter notes exclude this update, if so, set the exclude flag accordingly
        for note in self.sys.notes:
            if self.match == False and note[0] == False:
                self.exclude = True

class VersionCompare:
    """ Encapsulate the current deltas between a PackageVersions instance and a SystemVersions instance """
    
    def __init__(self, packageversion, systemversion):
        self.packageversion = packageversion
        self.systemversion = systemversion
        self.subcomponentcomparison = []
        self.mismatchcount = 0
        self.excludecount = 0
        
        self.checkSanity()
        self.compareVersions()
        
    def checkSanity(self):
        """ Ensure that there are no unique combinations of subsystem_automation_tag + subcomponent_name between self.packageversion and self.systemversion """

        tag_check_fail_count = 0
        for system_subcomponent in self.systemversion.subcomponents:
            found_match = False
            for package_subcomponent in self.packageversion.subcomponents:
                if (system_subcomponent.subsystem_automation_tag == package_subcomponent.subsystem_automation_tag and 
                   system_subcomponent.subcomponent_name == package_subcomponent.subcomponent_name):
                    found_match = True
            if not found_match:
                tag_check_fail_count += 1
                su.warn('No match for system_subcomponent %s::%s found in packageversion')
        if tag_check_fail_count == 0:
            su.debug('Version compare passed sanity check, all included system subcomponents were present in the package versions')
            
    def compareVersions(self):
        """ Compare all self.systemversion subcomponents to the matching self.packageversion subcomponents """

        for system_subcomponent in self.systemversion.subcomponents:
            for package_subcomponent in self.packageversion.subcomponents:
                if (system_subcomponent.subsystem_automation_tag == package_subcomponent.subsystem_automation_tag and
                   system_subcomponent.subcomponent_name == package_subcomponent.subcomponent_name):
                    this_comparison = SubComponentVersionCompare(package_subcomponent, system_subcomponent)
                    if this_comparison.match == False:
                        self.mismatchcount += 1
                    if this_comparison.exclude == True:
                        self.excludecount += 1
                    self.subcomponentcomparison.append(this_comparison)
                    
    def showComparison(self):
        """ Display a table showing the comparison results for all self.systemversion subcomponents to the matching self.packageversion subcomponents """

        # We will use standard_utils.pretty_table_generator, which needs a list
        temp_list = []
        
        # Create the column colors list
        column_colors = (su.c.CYAN, su.c.CYAN, su.c.GREEN, su.c.MAGENTA, su.c.WHITE, su.c.WHITE, '', '', '', '', '', su.c.WHITE)

        # Create the header row
        header = ('Idx', 'Automation_Tag', 'SubComponent_Name', 'Query_String', 'Pack-Vers', 'Pack-CRC', su.c.WHITE+'Sys-Vers', su.c.WHITE+'Sys-CRC', su.c.WHITE+'Img', 
                  su.c.WHITE+'Status', su.c.WHITE+'M', su.c.WHITE+'N')
        temp_list.append(header)
                
        # Add the subcomponents to the list
        for s in self.subcomponentcomparison:
            # There may be update notes that we need to display at the end of the list
            update_note_indices = []
            update_excluded_by_filter = False
            update_note_index = 0
            for update_note in self.systemversion.notes_list:
                for this_update_note in s.sys.notes:
                    if this_update_note == update_note:
                        update_note_indices.append(str(update_note_index))
                        if this_update_note[0] == False:
                            update_excluded_by_filter = True
                update_note_index += 1
            update_note_table_entry = ','.join(update_note_indices)
            # If the system version does match the package version, display the versions in green
            if s.match:
                temp_row = (str(s.sys.subsystem_index), s.sys.subsystem_automation_tag, s.sys.subcomponent_name, s.sys.query_string, s.pack.version, s.pack.crc, 
                            su.c.GREEN+s.sys.version, su.c.GREEN+s.sys.crc, su.c.GREEN+s.sys.image, su.c.GREEN+s.sys.status, su.c.GREEN+'Y', su.c.GREEN+update_note_table_entry)
                temp_list.append(temp_row)
            else:
                # If the system version does not match the package version, display the versions in yellow if the update is excluded by a filter (i.e. we won't perform the update)
                if update_excluded_by_filter:
                    temp_row = (str(s.sys.subsystem_index), s.sys.subsystem_automation_tag, s.sys.subcomponent_name, s.sys.query_string, s.pack.version, s.pack.crc, 
                                su.c.YELLOW+s.sys.version, su.c.YELLOW+s.sys.crc, su.c.YELLOW+s.sys.image, su.c.YELLOW+s.sys.status, su.c.YELLOW+'N', su.c.YELLOW+update_note_table_entry)
                # If the system version does not match the package version, display the versions in red if the update is not excluded by a filter (i.e. we will actually perform the update)
                else:
                    temp_row = (str(s.sys.subsystem_index), s.sys.subsystem_automation_tag, s.sys.subcomponent_name, s.sys.query_string, s.pack.version, s.pack.crc, 
                                su.c.RED+s.sys.version, su.c.RED+s.sys.crc, su.c.RED+s.sys.image, su.c.RED+s.sys.status, su.c.RED+'N', su.c.RED+update_note_table_entry)
                temp_list.append(temp_row)

        # Display the comparison list
        su.msg('')
        for line in su.pretty_table_generator(temp_list, column_colors=column_colors, delimeter='|', header_separator='='):
            su.msg(line)
        su.msg('')
        # Display any update notes
        if self.systemversion.notes_list:
            su.msg(su.c.YELLOW+'Update Notes:')
            note_index = 0
            for note in self.systemversion.notes_list:
                su.msg(su.c.YELLOW+'  %i: %s' % (note_index, note[1]))
                note_index += 1
            su.msg('')
        
    def getNextMismatchedSubComponent(self):
        """ Walk through self.subcomponentcomparison and return the first entry that does not match and is not excluded"""
        for s in self.subcomponentcomparison:
            if not s.match:
                if s.exclude:
                    su.warn('Skipping update of %s %s %s %s due to update filter (see notes)' % (s.sys.subsystem_automation_tag, s.sys.subcomponent_name, s.sys.image, s.sys.status))
                    continue
                else:
                    return s

def discoverManifests(checkroot):
    """ Walk the directory tree starting at checkroot and return a list of discovered *manifest.xml and stx*.xml + <FirmwarePackage> files. """
    manifest_files = []
    for directory, dirnames, filenames in os.walk(checkroot):
        for f in filenames:
            # Older USM packages and all STX_Tools packages have a suffix of '*manifest.xml'
            if f.endswith('manifest.xml'):
                manifest_files.append({'filename':f, 'path':directory})
            # Newer USM packages have dropped the '*manifest.xml' suffix, so look for *.xml and then search within for a <FirmwarePackage> line:
            elif f.endswith('.xml'):
                add_the_file = False
                for l in open(os.path.join(directory, f)).readlines():
                    if l.strip() == '<FirmwarePackage>':
                        add_the_file = True
                        break
                if add_the_file:
                    manifest_files.append({'filename':f, 'path':directory})
    for m in manifest_files:
        su.good('Discovered manifest: %s' % m['filename'])
    return manifest_files
    
def discoverDescriptor(checkroot):
    """ Look for a single file named *configuration_descriptor.xml in checkroot, die if anything other than exactly one file is found """
    descriptor_files = []
    for directory, dirnames, filenames in os.walk(checkroot):
        for f in filenames:
            if f.endswith('configuration_descriptor.xml'):
                descriptor_files.append({'filename':f, 'path':directory})
        ### The break below will effectively stop after searching checkroot, without searching any subfolders
        break
    if len(descriptor_files) == 0:
        su.die('FATAL: Unable to locate any files matching *configuration_descriptor.xml in %s' % checkroot)
    elif len(descriptor_files) > 1:
        su.msg('ERROR: Multiple files matching *configuration_descriptor.xml were found in %s' % checkroot)
        for d in descriptor_files:
            su.msg(str(d))
        su.die('FATAL: Unable to proceed with multiple configuration_descriptors present')
    else:
        su.good('Discovered configuration descriptor: %s' % descriptor_files[0]['filename'])
        return descriptor_files[0]
        
def discoverUpdateProfile(checkroot):
    """ Look for a single file named *update_profile.xml in checkroot, die if anything other than exactly one file is found """
    update_profile_files = []
    for directory, dirnames, filenames in os.walk(checkroot):
        for f in filenames:
            if f.endswith('update_profile.xml'):
                update_profile_files.append({'filename':f, 'path':directory})
        ### The break below will effectively stop after searching checkroot, without searching any subfolders
        break
    if len(update_profile_files) == 0:
        su.die('FATAL: Unable to locate any files matching *update_profile.xml in %s' % checkroot)
    elif len(update_profile_files) > 1:
        su.msg('ERROR: Multiple files matching *update_profile.xml were found in %s' % checkroot)
        for p in update_profile_files:
            su.msg(str(p))
        su.die('FATAL: Unable to proceed with multiple update_profiles present')
    else:
        su.good('Discovered update profile: %s' % update_profile_files[0]['filename'])
        return update_profile_files[0]

def discoverSTVSM(checkroot):
    """ Look for a single file named *subcomponent_to_version_string_map.xml in checkroot, die if anything other than exactly one file is found """
    stvsm_files = []
    for directory, dirnames, filenames in os.walk(checkroot):
        for f in filenames:
            if f.endswith('subcomponent_to_version_string_map.xml'):
                stvsm_files.append(os.path.join(directory, f))
        ### The break below will effectively stop after searching checkroot, without searching any subfolders
        break
    if len(stvsm_files) == 0:
        su.die('FATAL: Unable to locate any files matching *subcomponent_to_version_string_map.xml in %s' % checkroot)
    elif len(stvsm_files) > 1:
        su.msg('ERROR: Multiple files matching *subcomponent_to_version_string_map.xml were found in %s' % checkroot)
        for p in stvsm_files:
            su.msg(str(p))
        su.die('FATAL: Unable to proceed with multiple subcomponent_to_version_string_map.xml files present')
    else:
        su.good('Discovered subcomponent_to_version_string_map: %s' % os.path.basename(stvsm_files[0]))
        return stvsm_files[0]

        
def getManifestFile(manifests, tagpath):
    """ Search manifests for tagpath, return the matching ManifestFile instance if found, otherwise return None """
    results = []
    for this_manifest in manifests:
        tmp_result = None
        # tagpath can be either a string in the form of 'PACKAGETYPE/automationtag' or a descriptor.AutomationTagPath object
        if type(tagpath) is str:
            tagpath = descriptor.AutomationTagPath(tagpath)
        if this_manifest.header.packagetype == tagpath.packagetype:
            tmp_result = this_manifest.getFile(tagpath.automationtag)
        if tmp_result is not None:
            results.append(tmp_result)
    if len(results) == 0:
        return None
    elif len(results) == 1:
        return results[0]
    else:
        su.die('Tag Path collision: %s' % str(results))
        
def checkFiles(this_descriptor, manifests, system_index=None):
    file_not_matched = False
    missing_subcomponent = False
    this_system_index = 0
    for system in this_descriptor.systems:
        # If a system_index was specified, only check the files in the specified system, otherwise check all of them
        if system_index is not None:
            if this_system_index != system_index:
                this_system_index += 1
                continue
        su.info('Checking System: %s' % str(system))
        for subsystem in system.subsystems:
            # Check if any of the discovered manifests match the manifest path that is specified in the SubSystem tag path
            manifest_matched = False
            tag_matched = False
            for manifest in manifests:
                if subsystem.automationtagpath.packagetype == manifest.header.packagetype:
                    manifest_matched = True
                    # Check to see if the file specified in the descriptor SubSystem automationtag exists in the manifest
                    manifest_file = manifest.getFile(subsystem.automationtagpath.automationtag)
                    if manifest_file is not None:
                        tag_matched = True
                        # Perform checksum validation on the file specified in the descriptor SubSystem tag
                        if manifest.validateFile(manifest_file):
                            su.good('Checksum validation passed for %s [%s]' % (subsystem.automationtagpath.string, manifest_file.filename))
                        else:
                            su.warn('Checksum validation failed for %s [%s]' % (subsystem.automationtagpath.string, manifest_file.filename))
                        for subcomponent in subsystem.subcomponents:
                            if not manifest_file.getSubComponent(subcomponent.name):
                                missing_subcomponent = True
                                su.error('Unable to locate requested SubComponent in manifest with filename %s' % (manifest.filename))
                                tag = subsystem.automationtagpath.automationtag
                                name = subcomponent.name
                                su.error('- <File> with <Automation_Tag> %s does not include <SubComponent> with the name %s' % (tag, name))
            if not (manifest_matched and tag_matched):
                file_not_matched = True
                su.warn('Unable to locate %s in all discovered manifests' % subsystem.automationtagpath.string)
        this_system_index += 1
    if file_not_matched or missing_subcomponent:
        return False
    else:
        return True
        
def getToolPath(this_step, manifests):
    """ Generate the full file system path to this_step.directpath or this_step.automationtagpath """
    
    if this_step.tooldirectpath:
        return this_step.tooldirectpath
    else:
        return getManifestFile(manifests, this_step.toolautomationtagpath).full_os_path
        
def runQuery(this_subsystem, manifests, this_query_profile, target):
    """ Execute specified <QueryProfile><QuerySteps> for this_subsystem on target 
        1. Loop through each specified <QueryStep>, create and execute the query command(s), checking for zero exit status before continuing
        2. Collect the stdout output from all <QueryStep> commands into a string buffer
        3. Return the resulting combined output along with the target (used for automatic target detection) """
    this_query_profile_object = this_query_profile.getProfile(this_subsystem.queryprofile)
    this_target = None
    this_versions = suu.VersionList()

    su.debug(sys._getframe().f_code.co_name+'::%s target %s' % (this_query_profile_object, this_target))
    for this_step in this_query_profile_object.querysteps:
        combined_output = ''
        query_parser_type = this_step.parsertype
        this_query_toolpath = getToolPath(this_step, manifests)
        su.debug('%s %s' % (target,this_target))
        if target == 'auto' and this_target is None:
            this_target = suu.getUSBTarget(this_query_toolpath)
            su.debug('Automatic target detected: %s' % this_target)
        elif this_target is None:
            this_target = target
        su.debug('suu::runQuery to target [%s]' % this_target)
        cmdlist = this_step.completeCommandList(this_query_toolpath, this_target)
        cmdstring = this_step.completeCommandString(this_query_toolpath, this_target)
        (stdout, stderr, exitstatus) = su.cmd(cmdlist, debug_offset=2)
        # Check for errors and display output if necessary
        if exitstatus != 0:
            su.warn('Exit status was %i after running the following query command:\n%s' % (exitstatus, cmdstring))
            su.warn('STDOUT:')
            su.warn('========')
            su.warn(stdout)
            su.warn('========')
            su.warn('STDERR:')
            su.warn('========')
            su.warn(stderr)
            su.warn('========')
            su.die('exiting')
        else:
            combined_output += stdout + '\n'
        # Parse the raw results from the query
        this_versions.parse(combined_output, query_parser_type)
    return (this_versions, this_target)
    
def performAutomatedUpdates(this_descriptor, manifests, this_update_profile, this_query_profile, stvsm_map, system_index, target, max_retries=3):
    """ Perform automated, intelligent updates of all SubSystems in the descriptor system identified by system_index, applied to target, in the following manner:
        1. Compare package versions to target versions
        2. Execute the specified Update Profile for the next SubSystem that has any SubComponents that do not match
        3. Repeat steps 1+2 until one of the following occurs:
            a. All versions match, in which case return successfully
            b. Lack of forward progress (as measured by a decrease in the count of mismatched subcomponents between subsequent version comparisons) in excess of max_retries
            c. The system reboots due to activation of a component (such as x86 BIOS or CPLD)
    """
    # Get the system we'd like to update based on system_index
    this_system = this_descriptor.systems[system_index]

    # Get the package versions (we only need to do this once as they won't change during the updates)
    this_packageversions = PackageVersions()
    this_packageversions.getPackageVersions(this_descriptor, manifests, system_index=system_index)

    # Keep going until all potential updates are performed, or we exceed max_retries attempts with no forward progress
    retries_left = max_retries
    potential_update_count = None
    while retries_left > 0:
        # Query the system versions
        this_systemversions = SystemVersions()
        this_systemversions.getSystemVersions(this_descriptor, manifests, this_query_profile, stvsm_map, system_index, target)
        
        # Update this_target (in case we are using automatic target detection during query)
        this_target = this_systemversions.autotarget
        
        # Compare the system versions to the package versions and display the comparison table
        this_versioncompare = VersionCompare(this_packageversions, this_systemversions)
        this_versioncompare.showComparison()
        if this_versioncompare.mismatchcount != 0:
            if (this_versioncompare.mismatchcount - this_versioncompare.excludecount) != 0:
                su.warn('Mismatch count: %i, Exclude count: %i, Potential Update Count: %i' % (this_versioncompare.mismatchcount, this_versioncompare.excludecount, this_versioncompare.mismatchcount - this_versioncompare.excludecount))
        else:
            su.good('Mismatch count: %i, Exclude count: %i, Potential Update Count: %i' % (this_versioncompare.mismatchcount, this_versioncompare.excludecount, this_versioncompare.mismatchcount - this_versioncompare.excludecount))

        # Check if we are making forward progress
        # Don't compare the potential_update_count if this is the first cycle
        if potential_update_count is not None:
            if (this_versioncompare.mismatchcount - this_versioncompare.excludecount) < potential_update_count:
                su.good('The last update reduced the potential update count by %i SubComponent(s)' % (potential_update_count - (this_versioncompare.mismatchcount - this_versioncompare.excludecount)))
                retries_left = max_retries
            else:
                retries_left -= 1
                su.warn('The last update did not reduce the potential update count, retries remaining: %i' % retries_left)
                if retries_left == 0:
                    break
        potential_update_count = (this_versioncompare.mismatchcount - this_versioncompare.excludecount)
        if potential_update_count == 0:
            break
        
        # Update the next SubSystem that has a mismatched SubComponent and is not excluded by an update filter
        mismatched_subcomponent = this_versioncompare.getNextMismatchedSubComponent()
        su.info('Updating %s using target %s' % (mismatched_subcomponent.sys.subsystem_automation_tag, this_target))
        # Instead of updating the component, just remove it and continue (DEBUG!)
        #this_descriptor.systems[system_index].removesubsystem(mismatched_subcomponent.sys.subsystem_index)
        #continue
        
        # Grab the subsystem from the system using the automation tag from mismatched_subcomponent
        this_subsystem = this_system.getsubsystem(mismatched_subcomponent.sys.subsystem_automation_tag) 

        # Grab the firmware file path from the manifest based on what was specified in the descriptor subsystem definition
        this_fw_file = getManifestFile(manifests, this_subsystem.automationtagpath)
        this_fw_filepath = this_fw_file.full_os_path

        # Grab the update profile based on what was specified in the descriptor subsystem definition
        current_update_profile = this_update_profile.getProfile(this_subsystem.updateprofile)
        
        # Now execute the actual update commands based on the steps included in the update profile
        for this_update_step in current_update_profile.updatesteps:
            su.info('Update step: %s' % this_update_step.description)
            # Grab the update tool details based on the update step
            this_tool_filename = getToolPath(this_update_step,manifests)
            # Generate a list to pass onto su.cmd based on the update profile
            this_command_list = this_update_step.completeCommandList(toolpath=this_tool_filename, device=this_target, filename=this_fw_filepath)
            # Display the update command we are about to execute
            su.info('Running the following command:\n'+' '.join(this_command_list))
            # Run the command, capturing stdout, stderr, exitcode
            (stdout, stderr, exitcode) = su.cmd(this_command_list, debug_offset=2)
            # Check the exit code and display error output if nonzero
            if exitcode != 0:
                su.warn('Exit status from the above command was: %i' % exitcode)
                su.warn('\n-== STDOUT ==-\n'+stdout)
                su.warn('\n-== STDERR==-\n'+stderr)
                su.error('Unable to complete the update steps, will try again if retry count has not been exhausted')
                # Break out of the loop that executes the update steps for this update profile
                break

    if potential_update_count > 0 and retries_left == 0:
        su.warn('Mismatch count: %i, Exclude count: %i, Potential Update Count: %i' % (this_versioncompare.mismatchcount, this_versioncompare.excludecount, potential_update_count))
        su.die('Retries remaining: %i, exiting with error status' % retries_left)
        return 1
    if potential_update_count == 0 and this_versioncompare.excludecount > 0:
        su.good('All potential updates from this controller are complete')
        su.warn('There are %i potential updates that were excluded from this controller (see notes), ensure these udpates are completed from the partner controller' % this_versioncompare.excludecount)
        return 0
    if potential_update_count == 0 and this_versioncompare.excludecount == 0:
        su.good('All updates are complete')
        return 0

def createManualUpdate(this_descriptor, manifests, this_update_profile, system_index):
    """ Create a manual update folder for the specified sysem (with no ability to identify different system types or query target system FW) in the following manner:
        1. Create a directory to hold the manual update package, named as follows: ./descriptor-header-summary_system-shortname_manual-update
        2. Copy the firmware and tools files from the packages to the new directory
        3. Generate update shell scripts for each subsystem, named as follows: subsystem-index_subsystem-tag-name_update.sh
            - The shell script will include comments with a descriptive information header
            - The update commands will include all steps based on the specified update_profile
            - The only included error checking will be to ensure that the previous step returned with exit status 0
        """
    this_system = this_descriptor.systems[system_index]

    # Create a directory to hold the manual update package
    manual_update_directory_name = '%s_%s_manual-update' % (this_descriptor.header.summary, this_system.shortname)
    manual_update_directory_full_os_path = os.path.join(os.curdir, manual_update_directory_name)
    su.info('Creating directory %s' % manual_update_directory_full_os_path)
    # Make sure the directory isn't already there
    if os.path.exists(manual_update_directory_full_os_path):
        su.die('Directory already exists')
    else:
        os.mkdir(manual_update_directory_full_os_path)

    # Gather the firmware and tools files from the specified packages and copy them to the new directory
    # Also collect the update profiles into set for later use (so we can gather the update tools into the same folder)
    # An update profile may be used more than once, and a given update tool may also be used more than once, use sets to only copy once
    update_profiles_set = Set()
    su.info('Copying firmware files to directory')
    for this_subsystem in this_system.subsystems:
        this_file = getManifestFile(manifests, this_subsystem.automationtagpath)
        copy2(this_file.full_os_path, manual_update_directory_full_os_path)
        su.good('    > %s' % this_file.full_os_path)
        update_profiles_set.add(this_subsystem.updateprofile)
    # Now that we know all of the update profiles that we need, gather a set of all of the update tools that we need
    su.info('Copying required update tools to directory')
    update_tools_full_path_set = Set()
    profile_missing = False
    for needed_profile in update_profiles_set:
        profile = this_update_profile.getProfile(needed_profile)
        for updatestep in profile.updatesteps:
            temp_full_path = ''
            # If it is a direct path, just add as-is
            if updatestep.tooldirectpath:
                temp_full_path = su.fix_path(None, None, updatestep.tooldirectpath)
            # If it is a manifest path, look up the tool via the automation tag path in the manifest
            else:
                this_tool = getManifestFile(manifests, updatestep.toolautomationtagpath)
                if this_tool:
                    temp_full_path = this_tool.full_os_path
                else:
                    su.die('Unable to locate requested file with automation tag path [%s] in provided manifests' % p.toolpath)
            # Now add the full path to our set, and put the file name only back into the update step as we'll need that later when we build the script
            update_tools_full_path_set.add(temp_full_path)
            (temp_path, temp_filename) = os.path.split(temp_full_path)
            updatestep.tool_filename_only = temp_filename
                
    # Now that we know the full path to all of the update tools that we need, copy the tools to the directory
    for this_tool_full_os_path in update_tools_full_path_set:
        copy2(this_tool_full_os_path, manual_update_directory_full_os_path)
        su.good('    > %s' % this_tool_full_os_path)

    # Now Generate the update shell scripts for each subsystem
    # Loop through subsystems, generate a script for each step in the specified update profile
    su.info('Creating manual update scripts')
    for this_subsystem in this_system.subsystems:
        manual_script_name = '%s_%s.sh' % (this_subsystem.index, this_subsystem.automationtagpath.automationtag)

        # Grab the update profile based on what was specified in the descriptor subsystem definition
        current_update_profile = this_update_profile.getProfile(this_subsystem.updateprofile)
                
        # Grab the firmware file name only from the manifest based on what was specified in the descriptor subsystem definition,
        # no need to error check here since we did it above when copying
        this_fw_file = getManifestFile(manifests, this_subsystem.automationtagpath)
        this_fw_filename = this_fw_file.filename

        # Build the script using the information obtained above
        # First, the script header
        manual_script_list = []
        manual_script_list.append('#!/bin/sh')
        manual_script_list.append('')
        manual_script_list.append('# Automatically generated manual update script')
        manual_script_list.append('# Genrated on %s by %s' % (su.timenow(), os.path.basename(__file__)))
        manual_script_list.append('')
        manual_script_list.append('if [[ $1 == \"\" ]]; then echo \"USAGE:\\n$0 device\\n  Where: [device] is the firmware update device path or IP\"; exit 1; fi')
        manual_script_list.append('device=$1')
        manual_script_list.append('')
        
        # Now add in the actual update commands based on the steps included in the update profile
        for this_update_step in current_update_profile.updatesteps:
            # Grab the tool file name only from this_update_step, we inserted it into the update step above when we were copying the tools to our new folder
            this_tool_filename = './' + this_update_step.tool_filename_only
            this_step_comment = '# ' + this_update_step.description
            this_command_string = this_update_step.completeCommandString(toolpath=this_tool_filename, device='${device}', filename=this_fw_filename)
            results_check_command = 'if [ $? -ne 0 ]; then echo \"### ERROR, EXITING\"; exit 1; fi'
            manual_script_list.append(this_step_comment)
            manual_script_list.append('echo \"# ' + this_update_step.description + '\"')
            manual_script_list.append(this_command_string)
            manual_script_list.append(results_check_command)
            manual_script_list.append('')
        manual_script_list.append('exit 0')
        # Now write the script to the file
        this_script_full_os_path = os.path.join(manual_update_directory_full_os_path, manual_script_name)
        this_script_file_object = open(this_script_full_os_path, 'w')
        # Writelines doesn't add newlines, so we will add them here instead of cluttering up the content above
        this_script_file_object.writelines(su.add_newline(manual_script_list))
        this_script_file_object.close()
        # Make the script executable
        su.make_executable(this_script_full_os_path)
        # Inform the user that the script was written successfully
        su.good('    > %s' % manual_script_name)

def main():
    """ Check dependendencies and arguments then run appropriate functions, display usage info otherwise """
    parser = argparse.ArgumentParser(description=description_string)
    parser.add_argument('-d', '--descriptor', help='Path to the ...configuration_descriptor.xml file to use, if unspecified the current working directory will be searched')
    parser.add_argument('--checkfiles', action='store_true', help='Validate descriptor SubSystem tags against discovered manifests')
    parser.add_argument('--show_package_versions', action='store_true', help='Show the package versions for descriptor SubComponents')
    parser.add_argument('--show_system_versions', action='store_true', help='Show the system versions for descriptor SubComponents')
    parser.add_argument('--compare_versions', action='store_true', help='Compare system versions to package versions')
    parser.add_argument('--perform_updates', action='store_true', help='Perform intelligent updates of system SubComponents that do not match package versions')
    parser.add_argument('--create_manual_update', action='store_true', help='Create a manual update package folder')
    parser.add_argument('--target', help='Path to device target or IP address for system to query or update (required for show_system_versions, compare_versions and perform_updates')
    parser.add_argument('--system_index', help='System index from descriptor (required for show_package_versions, show_system_versions, compare_versions, perform_updates and create_manual_update')
    parser.add_argument('--exclude', help='Comma separated list of SubSystem indices to exclude (applies to all possible actions)')
    parser.add_argument('--force', help='Comma separated list of SubSystem indices to always update, even if the system versions match the package versions (applies only to perform_updates)')
    parser.add_argument('-c', '--color', action='store_true', help='Enable color in output')
    parser.add_argument('-t', '--timestamp', action='store_true', help='Enable timestamps in output')
    parser.add_argument('-q', '--quiet', action='store_true', help='Suppress non-error output')
    parser.add_argument('-s', '--silent', action='store_true', help='Suppress all output (overrides quiet)')
    parser.add_argument('-l', '--logfile', help='Path to log file (color is not logged)')
    parser.add_argument('-v', '--verbosity', action='count', help='Output verbosity level (use multiple times to increase the verbosity level: -vvvv == level 4; 1=quiet, 2=standard 3+=debug')
    parser.add_argument('-V', '--version', action='store_true', help='Display version and exit')
    args = parser.parse_args()
    
    # Configure message and logging output
    if args.verbosity:
        su.debug_level = args.verbosity
        su.enable_prefix_strings(default='%s::' % os.path.basename(__file__))
    else:
        su.debug_level = 2
        su.enable_prefix_strings(default='%s::' % os.path.basename(__file__))
    
    if args.color:
        su.enable_color()
        
    if args.timestamp:
        su.enable_timestamps()
        
    if args.quiet:
        su.debug_level = 0
        
    if args.silent:
        su.debug_level = -sys.maxint -1
        
    if args.logfile:
        su.enable_logfile(args.logfile)
        
    if args.version:
        su.info('Version: %s' % version_string)
        return 0

    # Output the version string and import the configuration descriptor and manifests
    su.info('Version: %s' % version_string)
    scriptroot = os.path.dirname(os.path.realpath(__file__))
    
    # Handle the optional system_index
    system_index = None
    if args.system_index is not None:
        try:
            system_index = int(args.system_index)
        except:
            su.die('system_index must be a single integer')
    
    # Handle the optional SubSystem exclusion list
    exclusions_list = []
    if args.exclude is not None:
        # Ensure the format is either a single number, or a comma separated list of numbers
        if type(args.exclude) is not str:
            su.die('The value provided to exclude must be a comma separated list of numbers')
        else:
            try:
                for n in args.exclude.split(','):
                    exclusions_list.append(int(n))
            except:
                su.die('The value provided to exclude must be a comma separated list of numbers')

    # Handle the optional SubSystem forced update list
    forced_update_list = []
    if args.force is not None:
        # Ensure the format is either a single number, or a comma separated list of numbers
        if type(args.force) is not str:
            su.die('The value provided to force must be a comma separated list of numbers')
        else:
            try:
                for n in args.force.split(','):
                    forced_update_list.append(int(n))
            except:
                su.die('The value provided to force must be a comma separated list of numbers')

    # Discover the Configuration Descriptor (if not specified), then import
    if args.descriptor:
        descriptor_file = {'path':os.path.dirname(args.descriptor), 'filename':os.path.basename(args.descriptor)}
    else:
        descriptor_file = discoverDescriptor(scriptroot)
    this_descriptor = descriptor.Descriptor(path=descriptor_file['path'], filename=descriptor_file['filename'])
    su.info(str(this_descriptor))    

    # If provided, confirm that the system index is valid, then apply exclusions (if provided)
    if system_index is not None:
        if system_index <= (this_descriptor.systemcount - 1) and system_index >= 0:
            su.info('System index %i is valid' % system_index)
            # Apply exclusions (if specified) by removing them from this_descriptor
            for subsystem_index_to_remove in exclusions_list:
                removed_subsystem_string = this_descriptor.systems[system_index].removesubsystem(subsystem_index_to_remove)
                su.info('Removed subsystem: %s' % removed_subsystem_string)
        else:
            su.warn('Invalid system index [%i], valid systems include the following:' % system_index)
            i = 0
            for this_system in this_descriptor.systems:
                su.msg('%sSystem [%i] - %s%s' % (su.c.CYAN, system_index, str(this_system), su.c.WHITE))
                i += 1
            su.die('Please specify a valid system index')

    # Manifests
    manifest_files = discoverManifests(scriptroot)
    manifests = []
    for manifest_file in manifest_files:
        newmanifest = manifest.Manifest(path=manifest_file['path'], filename=manifest_file['filename'])
        manifests.append(newmanifest)
    
    # Validate the files if requested
    if args.checkfiles:
        if checkFiles(this_descriptor, manifests, system_index=system_index):
            su.info('File validation passed for all systems')
        else:
            su.die('One or more files failed validation check')
            
    # Show package versions if requested
    if args.show_package_versions:
        if system_index is None:
            su.die('show_package_versions requires system_index to be specified')
        this_packageversions = PackageVersions()
        this_packageversions.getPackageVersions(this_descriptor, manifests, system_index)
        this_packageversions.showPackageVersions()

    # Show system versions if requested
    if args.show_system_versions:
        # Confirm that a system target was provided
        if system_index is None:
            su.die('show_system_versions requires system_index to be specified')
        if args.target is None:
            su.die('show_system_versions requires target to be specified')
        # Discover UpdateProfile, QueryProfile and STVSM
        update_profile_file = discoverUpdateProfile(scriptroot)
        this_query_profile = update_profile.QueryProfileCollection(update_profile_file['path'], update_profile_file['filename'])
        stvsm_file = discoverSTVSM(scriptroot)
        stvsm_map = stvsm.MapCollection(stvsm_file)
        # Query then display the system versions
        this_systemversions = SystemVersions()
        this_systemversions.getSystemVersions(this_descriptor, manifests, this_query_profile, stvsm_map, system_index=system_index, target=args.target)
        this_systemversions.showSystemVersions()
        
    # Compare system versions to package versions if requested
    if args.compare_versions:
        if system_index is None:
            su.die('compare_versions requires system_index to be specified')
        # Confirm that a system target was provided
        if args.target is None:
            su.die('compare_versions requires target to be specified')
        # Get the package versions
        this_packageversions = PackageVersions()
        this_packageversions.getPackageVersions(this_descriptor, manifests, system_index=system_index)
        # Discover UpdateProfile, QueryProfile and STVSM
        update_profile_file = discoverUpdateProfile(scriptroot)
        this_query_profile = update_profile.QueryProfileCollection(update_profile_file['path'], update_profile_file['filename'])
        stvsm_file = discoverSTVSM(scriptroot)
        stvsm_map = stvsm.MapCollection(stvsm_file)
        # Query the system versions
        this_systemversions = SystemVersions()
        this_systemversions.getSystemVersions(this_descriptor, manifests, this_query_profile, stvsm_map, system_index=system_index, target=args.target)
        # Compare the system versions to the package versions and display the comparison table
        this_versioncompare = VersionCompare(this_packageversions, this_systemversions)
        this_versioncompare.showComparison()
        if this_versioncompare.mismatchcount != 0:
            if (this_versioncompare.mismatchcount - this_versioncompare.excludecount) != 0:
                su.warn('Mismatch count: %i, Exclude count: %i, Potential Update Count: %i' % (this_versioncompare.mismatchcount, this_versioncompare.excludecount, this_versioncompare.mismatchcount - this_versioncompare.excludecount))
        else:
            su.good('Mismatch count: %i' % this_versioncompare.mismatchcount)
        return (this_versioncompare.mismatchcount - this_versioncompare.excludecount)
        
    # Perform updates of downrev components, comparing versions after each SubSystem update completes successfully before moving on to the next SubSystem
    if args.perform_updates:
        if system_index is None:
            su.die('perform_updates requires system_index to be specified')
        # Confirm that a system target was provided
        if args.target is None:
            su.die('perform_updates requires target to be specified')
        # Validate the files for the specified system
        su.info('Checking files before attempting to upgrade')
        if checkFiles(this_descriptor, manifests, system_index):
            su.good('File validation passed for system index [%i], proceeding with upgrades' % system_index)
        else:
            su.die('One or more files failed validation check')
        # Discover UpdateProfile, QueryProfile and STVSM
        update_profile_file = discoverUpdateProfile(scriptroot)
        this_update_profile = update_profile.UpdateProfileCollection(update_profile_file['path'], update_profile_file['filename'])
        this_query_profile = update_profile.QueryProfileCollection(update_profile_file['path'], update_profile_file['filename'])
        stvsm_file = discoverSTVSM(scriptroot)
        stvsm_map = stvsm.MapCollection(stvsm_file)
        # Perform automated updates, then exit with the status returned by performAutomatedUpdates
        return performAutomatedUpdates(this_descriptor, manifests, this_update_profile, this_query_profile, stvsm_map, system_index, args.target)
        
    # Create a manual update package folder if requested
    if args.create_manual_update:
        # Validate the files for the specified system
        su.info('Checking files before attempting to package')
        if checkFiles(this_descriptor, manifests, system_index):
            su.good('File validation passed for system index [%i], proceeding with packaging' % system_index)
        else:
            su.die('One or more files failed validation check')
        # Discover UpdateProfile
        update_profile_file = discoverUpdateProfile(scriptroot)
        this_update_profile = update_profile.UpdateProfileCollection(update_profile_file['path'], update_profile_file['filename'])
        # Create the manual update folder
        createManualUpdate(this_descriptor, manifests, this_update_profile, system_index=system_index)
    
    # If we got here just return 0
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
