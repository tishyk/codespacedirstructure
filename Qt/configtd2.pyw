#!/opt/python3/bin/python3
# @@ AVID HEADER - DO NOT EDIT @@
# Copyright 2011-2017 by Avid Technology, Inc.
# @@ AVID HEADER @@
"""
#  configtd.pyw
#  Graphical User Interface for the environment data.
"""
import copy
############################################################
import os
import sys
import time

from PyQt4 import QtGui, QtCore

import util.cenvdata
from CExceptions import CGenericExcn
from core.np_constants import ISIS_NET_PROVIDER, MN_NET_PROVIDER, MSWIN_NET_PROVIDER
from core.os_constants import IS_NT, IS_OSX
from services.CPyro import is_testmonkey_running
from util.CUpgradeTool import CUpgradeTool

try:
    from PyQt4 import uic
    config_td_dir = os.path.dirname(os.path.realpath(__file__))
    CConfigTd2MainForm = uic.loadUiType(os.path.join(config_td_dir, 'ui', 'configtd2_main.ui'))[0]
    CConfigTd2DialogGroupForm = uic.loadUiType(os.path.join(config_td_dir, 'ui', 'configtd2_copy_dialog.ui'))[0]
except ImportError:
    # uic module is not installed with PyQt library
    # use precompiled ui interface
    from ui.ConfigTdUi import Ui_MainWindow as CConfigTd2MainForm
    from ui.ConfigTdUi import Ui_Dialog as CConfigTd2DialogGroupForm


class CSelectDialog(QtGui.QDialog, CConfigTd2DialogGroupForm):
    """
    # select groups to copy to.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def add_item(self, group_name):
        """
        # Adds selected group into view
        """
        item = QtGui.QListWidgetItem(group_name)
        item.setCheckState(False)
        self.list_widget_groups.addItem(item)

    def add_items(self, group_names):
        """
        # Adds selected groups into view
        """
        for group in group_names:
            self.add_item(group)

    def clear(self):
        """
        # remove groups from view
        """
        self.list_widget_groups.clear()

    def all_items(self):
        """
        # retuurns all items in view
        """
        items = []
        for index in range(self.list_widget_groups.count()):
            items.append(self.list_widget_groups.item(index))

        return items

    def get_checked(self):
        """
        # returns checked items in view
        """
        return [item for item in self.all_items() if bool(item.checkState())]


class CMainFrame(QtGui.QMainWindow, CConfigTd2MainForm):
    """
    # Main form that is used for any manipulations with configtd xml file.
    """
    HOSTNAME_COLUMN = 0
    TM_STATUS_COLUMN = 1
    DEFAULT_TM_STATUS = "Unknown"

    def __init__(self, cenvdata, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.__cenvdata = cenvdata
        self.tabs_widget_logs.setVisible(False)
        QtGui.QToolTip.setFont(QtGui.QFont('OldEnglish', 10))
        self.copy_dialog = CSelectDialog(self)

        # Redirecting stdout and stderr to text boxes
        sys.stdout = OutLog(self.info_text_edit, sys.stdout)
        sys.stderr = OutLog(self.error_text_edit, sys.stderr)
        self.env_copy = {}
        self._save_envdatacopy()

        # Fill fields with values from xml file
        self.__set_default_values_storage()
        self.__set_default_values_isis()
        self.__set_default_values_video()
        self.__set_default_values_cifs()
        self.__set_default_values_failover()
        self.__set_default_values_test_settings()
        self.__set_default_values_remote_group()
        self.__set_default_values_upgrade_clients()

        # improve form view
        self.__update_view()

    def __update_view(self):
        """
        # update view for all items in form
        # like: fields size, spacing, margin, etc.
        """
        for variable, variable_type in vars(self).items():

            # set layout margins
            if isinstance(variable_type, QtGui.QLayout):
                layout = getattr(self, variable)

                # get layout for tab
                if ((isinstance(layout.parent(), QtGui.QWidget) and
                     self.tabWidget.indexOf(layout.parent()) != -1)):

                    layout.setMargin(20)
                    layout.setSpacing(20)

            #set label min length
            if isinstance(variable_type, QtGui.QLabel):
                label = getattr(self, variable)
                label.setMinimumWidth(120)

            #set line_edit min length
            if isinstance(variable_type, QtGui.QLineEdit):
                line_edir = getattr(self, variable)
                line_edir.setMinimumWidth(130)
                line_edir.setMinimumHeight(21)

        self.adjustSize()
        self.setMinimumSize(self.size())
        self.tabWidget.setCurrentWidget(self.storage_panel)

    def on_copy_click(self):
        """
        Copies the current remote clients to the specified remote group.
        """
        if self.hoststable.rowCount():
            current_groups = self.__cenvdata.get_agent_groups()

            # can't copy to the current group
            current_groups.remove(self.groupcombobox.currentText())

            self.copy_dialog.clear()
            self.copy_dialog.add_items(current_groups)

            # Open copy dialog, and copy users if user accepted dialog
            if self.copy_dialog.exec_() == QtGui.QDialog.Accepted:
                current_clients = [str(self.hoststable.item(index, 0).text())
                                   for index in range(self.hoststable.rowCount())]

                selected_groups = [item.text() for item in self.copy_dialog.get_checked()]

                # copy clients from current group into selected groups
                for group in selected_groups:
                    for client in current_clients:

                        if client not in self.__cenvdata.get_agents_from_group_name(group):
                            print("Adding client {} to group {}".format(client, group))
                            self.__cenvdata.add_agent_to_group(group, client)
        else:
            QtGui.QMessageBox.critical(self, "Group empty", "Current group has no clients to copy")

    def on_add_click(self):
        """
        Adds a remote client to the selected group.
        """
        new_remote_clients, dialogflag = QtGui.QInputDialog.getText(self, "New Remote Client",
                                                                    "Enter semi-colon separated list of new clients            ")
        if dialogflag:
            if new_remote_clients:
                group_name = self.groupcombobox.currentText()

                # User could enter semi-colon separated list
                clients = [client.lower() for client in new_remote_clients.split(';') if client]

                for client in clients:
                    if client not in self.__cenvdata.get_agents_from_group_name(group_name):
                        self.__cenvdata.add_agent_to_group(str(group_name), str(client))

                        self.__hoststable_append_row(QtGui.QTableWidgetItem(client),
                                                     QtGui.QTableWidgetItem(self.DEFAULT_TM_STATUS))

                    else:
                        QtGui.QMessageBox.information(self, "Add Clients", "Client '{}' already in list".format(client))
            else:
                QtGui.QMessageBox.critical(self, "Invalid remote client name", "Can not add empty hostname")

    def on_remove_all_click(self):
        """
        Removes all remote clients from the currently selected group
        """
        group_name = self.groupcombobox.currentText()
        if group_name:
            self.__cenvdata.remove_all_agents_from_group(str(group_name))
            self.hoststable.setRowCount(0)

    def on_remove_click(self):
        """
        Removes the selected remote client(s) from the current group.
        """
        group_name = self.groupcombobox.currentText()
        if group_name:
            # select items only from first column
            selected_hosts = [row for row in self.hoststable.selectedItems() if row.column() == 0]

            for host in selected_hosts:
                self.__cenvdata.remove_agent_from_group(str(group_name), host.text())
                self.hoststable.removeRow(host.row())

    def on_validate_click(self):
        """
        Verifies Test Monkey is running on all remote clients
        """

        for index in range(self.hoststable.rowCount()):
            client = self.hoststable.item(index, 0).text()

            # Change Cursor to Wait
            QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
            tm_running = "RUNNING" if is_testmonkey_running(client) else "NOT RUNNING"
            QtGui.QApplication.restoreOverrideCursor()

            self.hoststable.setItem(index, self.TM_STATUS_COLUMN, QtGui.QTableWidgetItem(tm_running))

    def on_save(self):
        """
        #  Retrieves the data from all panels and writes the data contained in the environment object to disk.
        """
        self.__savefile()

    def on_about(self):
        """
        shows about help
        """
        QtGui.QMessageBox.information(self, "About ConfigTD",
                                      "Config the SQA testing environment data,\ncreated 12/31/2011")

    @staticmethod
    def on_confluence():
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://avid-ondemand.atlassian.net/wiki/spaces/SBENG/"
                                                   "pages/45646467/Python+3.4+Testware+Install+Instructions",
                                                   QtCore.QUrl.TolerantMode))

    def on_verify_click(self):
        """
        Verify is system director hosts are accessible
        """

        hosts = [self.failover_sd_line_edit_1.text(),
                 self.failover_sd_line_edit_2.text()]

        unavailable_hosts = [host for host in hosts if self.__ping_host(host)]

        if unavailable_hosts:
            QtGui.QMessageBox.critical(self, "Host unavailable", "The following hosts are unavailable: {}"
                                       .format(", ".join(unavailable_hosts)))
        else:
            QtGui.QMessageBox.information(self, "Hosts available",
                                          "Both of the hosts are available")

    def on_text_changed_in_logs(self):
        # get tab index for changed
        index = self.tabs_widget_logs.indexOf(self.sender().parent())
        text = self.tabs_widget_logs.tabText(index)
        self.tabs_widget_logs.setTabText(index, text.strip(" *") + ' *')

    def on_text_clicked_in_logs(self):
        index = self.tabs_widget_logs.indexOf(self.sender().parent())
        self.on_log_tab_selected(index)

    def on_clear_logs(self):
        """
        # Clear all messages in logs
        """
        self.info_text_edit.blockSignals(True)
        self.error_text_edit.blockSignals(True)

        self.info_text_edit.clear()
        self.error_text_edit.clear()

        self.info_text_edit.blockSignals(False)
        self.error_text_edit.blockSignals(False)

    def on_log_tab_selected(self, index):
        text = self.tabs_widget_logs.tabText(index)
        self.tabs_widget_logs.setTabText(index, text.strip(" *"))

    def populatelist_ctrl(self, group_name):
        """
        # Populates the listctrl with the members of the passed in group name.
        """
        self.hoststable.setRowCount(0)
        for group_member in self.__cenvdata.get_agent_group_members(group_name):

            self.__hoststable_append_row(QtGui.QTableWidgetItem(group_member),
                                         QtGui.QTableWidgetItem(self.DEFAULT_TM_STATUS))

    def save(self):
        self.__save_cifs()
        self.__save_failover()
        self.__save_isis()
        self.__save_storage()
        self.__save_test_settings()
        self.__save_video()

    def closeEvent(self, event):
        """
        ##  Checks to see if any data was modified before being saved.
        ##  It will prompt the user to save if changes are found.
        """
        self.save()

        for key in self.__cenvdata.required_keys:
            data = self.__cenvdata.get_value_by_key(key)

            if (self.env_copy[key] != data):
                result = QtGui.QMessageBox.information(self, "Save On Close",
                                                       "Do you wish to save before closing?",
                                                       QtGui.QMessageBox.Yes |
                                                       QtGui.QMessageBox.No |
                                                       QtGui.QMessageBox.Cancel)

                if result == QtGui.QMessageBox.Yes:
                    self.__cenvdata.save()
                    break

                elif result == QtGui.QMessageBox.No:
                    break

                else:
                    event.ignore()

    def __hoststable_append_row(self, *args):
        """
        # Append new row into hosts table, with selected items.
        # args: items that will be added as columns for a new row
        """
        row = self.hoststable.rowCount()
        self.hoststable.insertRow(row)
        self.hoststable.setRowHeight(row, 18)

        for column, widget in enumerate(args):
            self.hoststable.setItem(row, column, widget)

    def _save_envdatacopy(self):
        """
        ##  Saves a copy of the data in the CEnvData object to check
        ##  against the data when the user closes the application.
        """
        self.env_copy = copy.deepcopy(self.__cenvdata.env_data_dict)


    def __savefile(self, filename=None, keep_original=True):
        """
        ##  Saves environment data to filename. If filename
        ##  is not specified, the current filename is used.
        ##
        ##  keepOriginal will set env_data_file back to
        ##  original filename if filename is not equal to None.
        """
        try:
            self.save()

            if (filename):
                original = self.__cenvdata.env_data_file
                self.__cenvdata.env_data_file = filename

                # Save to disk
                self.__cenvdata.save()
                if (keep_original):
                    self.__cenvdata.env_data_file = original
            else:
                self.__cenvdata.save()
        except CGenericExcn as excn:
            if "User doc transfer failed" in excn.desc:
                self.setStatusTip(excn.desc)
                return
            elif util.cenvdata.IP_ADDR_ERROR == excn.desc:
                self.setStatusTip("No data was saved.")
                return
            else:
                raise

        # Update the copy
        self._save_envdatacopy()

        status_text = "Saved to %s at %s" % (self.__cenvdata.env_data_file, time.strftime("%H:%M:%S%p"))
        self.setStatusTip(status_text)

    def __set_default_values_remote_group(self):
        """
        # Get default values from cenvdata, and put them into remote group tab
        """
        if self.__cenvdata.get_agent_groups():
            self.groupcombobox.addItems(self.__cenvdata.get_agent_groups())
            self.groupcombobox.setCurrentIndex(self.groupcombobox.findText("SingleRemoteClient"))

    def __set_default_values_storage(self):
        """
        # Sets the default value for each text box and drop drop menu in the main panel.
        """

        #Group box: Mount data
        self.mount_user_box.setText(self.__cenvdata.get_mount_user())
        self.mount_passwd_box.setText(self.__cenvdata.get_mount_password())
        self.scratch_dir_box.setText(self.__cenvdata.get_scratch_dir())
        self.enable_mount_box.setChecked(self.__cenvdata.get_enable_mounting())

        #Group box: Primary unity
        self.server_box1.setText(self.__cenvdata.get_server())
        self.workspace_box1.setText(self.__cenvdata.get_workspace())
        self.storage_group_box1.setText(self.__cenvdata.get_storage_group())
        self.np_combobox1.addItems(self.__set_np_default(self.__cenvdata.get_np()))
        self.np_combobox1.setCurrentIndex(0)

        #Group box: Secondary unity
        self.server_box2.setText(self.__cenvdata.get_server2())
        self.workspace_box2.setText(self.__cenvdata.get_workspace2())
        self.storage_group_box2.setText(self.__cenvdata.get_storage_group2())
        self.np_combobox2.addItems(self.__set_np_default(self.__cenvdata.get_np()))
        self.np_combobox2.setCurrentIndex(0)

        #Group box: Remote host
        self.remote_client_box.setText(self.__cenvdata.get_remote_client())

        #Group box: Test behaviour
        self.sotf_box.setChecked(self.__cenvdata.get_stop_on_test_failure())
        self.devmode_box.setChecked(self.__cenvdata.get_developer_mode())
        self.log_settings_box.setChecked(self.__cenvdata.get_reset_trace_settings())
        self.log_value_box.setText(self.__cenvdata.get_trace_setting())
        regex = QtCore.QRegExp('(0x){0,1}[0-9A-Fa-f]{1,8}')
        self.log_value_box.setValidator(QtGui.QRegExpValidator(regex, self.log_value_box))

    def __save_storage(self):
        """
        ##  Retrieves the text in each text box and stores it in the
        ##  CEnvData object. Does NOT write to the environment file
        """

        # translate 'CIFS' into OS specific type
        if str(self.np_combobox1.currentText()) == 'CIFS':
            if IS_NT:
                self.__cenvdata.set_np(MSWIN_NET_PROVIDER)
            elif IS_OSX:
                self.__cenvdata.set_np('smbfs')
            else:
                self.__cenvdata.set_np('cifs')
        else:
            self.__cenvdata.set_np(str(self.np_combobox1.currentText()))
            self.__cenvdata.set_np2(str(self.np_combobox2.currentText()))

        self.__cenvdata.set_server(str(self.server_box1.text()))
        self.__cenvdata.set_workspace(str(self.workspace_box1.text()))
        self.__cenvdata.set_storage_group(str(self.storage_group_box1.text()))
        self.__cenvdata.set_mount_user(str(self.mount_user_box.text()))
        self.__cenvdata.set_scratch_dir(str(self.scratch_dir_box.text()))
        self.__cenvdata.set_mount_password(str(self.mount_passwd_box.text()))
        self.__cenvdata.set_remote_client(str(self.remote_client_box.text()))
        self.__cenvdata.set_enable_mounting(bool(self.enable_mount_box.checkState()))
        self.__cenvdata.set_stop_on_test_failure(self.sotf_box.isChecked())
        self.__cenvdata.set_reset_trace_settings(self.log_settings_box.isChecked())
        self.__cenvdata.set_trace_setting(self.log_value_box.text())
        self.__cenvdata.set_developer_mode(bool(self.devmode_box.isChecked()))
        self.__cenvdata.set_server2(str(self.server_box2.text()))
        self.__cenvdata.set_workspace2(str(self.workspace_box2.text()))
        self.__cenvdata.set_storage_group2(str(self.storage_group_box2.text()))

    def __set_default_values_isis(self):
        """
        # Sets the default value for each text box and drop drop menu in the isis panel.
        """
        #Group box: isis data
        self.mcu_text.setText(self.__cenvdata.get_admin_user())
        self.mcp_text.setText(self.__cenvdata.get_admin_password())
        self.sbu_text.setText(self.__cenvdata.get_usa_user())
        self.sbp_text.setText(self.__cenvdata.get_usa_password())
        self.management_port.setText(self.__cenvdata.get_management_port())

        #Group box: ftp server
        self.ftpserver_text.setText(self.__cenvdata.get_cifs_ftp_server())
        self.ftp_loginname_text.setText(self.__cenvdata.get_cifs_ftp_user())
        self.ftp_password_text.setText(self.__cenvdata.get_cifs_ftp_password())

        #Group box: Licensing
        self.system_id_text.setText(self.__cenvdata.get_system_id())
        self.activation_id_text.setText(self.__cenvdata.get_activation_id())

        self.sb_system_id_text.setText(self.__cenvdata.get_sb_system_id())
        self.sb_activation_id_text.setText(self.__cenvdata.get_sb_activation_id())

    def __save_isis(self):
        """
        ##  Retrieves the text in each text box and stores it in the
        ##  CEnvData object. Does NOT write to the environment file
        """
        self.__cenvdata.set_admin_user(str(self.mcu_text.text()))
        self.__cenvdata.set_admin_password(str(self.mcp_text.text()))
        self.__cenvdata.set_usa_user(str(self.sbu_text.text()))
        self.__cenvdata.set_usa_password(str(self.sbp_text.text()))

        self.__cenvdata.set_cifs_ftp_server(str(self.ftpserver_text.text()))
        self.__cenvdata.set_cifs_ftp_user(str(self.ftp_loginname_text.text()))
        self.__cenvdata.set_cifs_ftp_password(str(self.ftp_password_text.text()))

        self.__cenvdata.set_system_id(str(self.system_id_text.text()))
        self.__cenvdata.set_activation_id(str(self.activation_id_text.text()))
        self.__cenvdata.set_sb_system_id(str(self.sb_system_id_text.text()))
        self.__cenvdata.set_sb_activation_id(str(self.sb_activation_id_text.text()))
        self.__cenvdata.set_management_port(self.management_port.text())

    def __set_default_values_video(self):
        """
        # Sets the default values for this panel
        """
        #Group box: video data
        self.text1.setText(self.__cenvdata.get_com_port())
        self.text2.setText(self.__cenvdata.get_video_standard())
        self.text3.setText(self.__cenvdata.get_airo_server())
        self.story_tc_box.setChecked(self.__cenvdata.get_story_tc())
        self.still_cue_box.setChecked(self.__cenvdata.get_still_cue())

        #Group box: storage data
        self.use_pattern_feed.setChecked(self.__cenvdata.get_pattern_feed())

    def __save_video(self):
        """
        ##  Retrieves the text in each text box and stores it in the
        ##  CEnvData object. Does NOT write to the environment file
        """
        self.__cenvdata.set_com_port(str(self.text1.text()))
        self.__cenvdata.set_video_standard(str(self.text2.text()))
        self.__cenvdata.set_airo_server(str(self.text3.text()))
        self.__cenvdata.set_story_tc(bool(self.story_tc_box.checkState()))
        self.__cenvdata.set_still_cue(bool(self.still_cue_box.checkState()))
        self.__cenvdata.set_pattern_feed(bool(self.use_pattern_feed.checkState()))

    def __set_default_values_cifs(self):
        """
        # Sets the default values for this panel
        """
        #Group box: cifs server
        self.cifs_server_name_line_edit.setText(self.__cenvdata.get_cifs_server_name())
        self.cifs_isis_server_line_edit.setText(self.__cenvdata.get_sd_name_for_cifs_server())

        #Group box: cifs shares
        self.cifs_share_line_edit_1.setText(self.__cenvdata.get_cifs_share_1())
        self.cifs_share_line_edit_2.setText(self.__cenvdata.get_cifs_share_2())

    def __save_cifs(self):
        """
        ##  Retrieves the text in each text box and stores it in the
        ##  CEnvData object. Does NOT write to the environment file
        """
        self.__cenvdata.set_cifs_server_name(str(self.cifs_server_name_line_edit.text()))
        self.__cenvdata.set_sd_name_for_cifs_server(str(self.cifs_isis_server_line_edit.text()))
        self.__cenvdata.set_cifs_share_1(str(self.cifs_share_line_edit_1.text()))
        self.__cenvdata.set_cifs_share_2(str(self.cifs_share_line_edit_2.text()))

    def __set_default_values_failover(self):
        """
        # Sets the default values for this panel
        """
        self.failover_sd_line_edit_1.setText(self.__cenvdata.get_first_failover_sd_name())
        self.failover_sd_line_edit_2.setText(self.__cenvdata.get_second_failover_sd_name())

    def __save_failover(self):
        """
        ##  Retrieves the text in each text box and stores it in the
        ##  CEnvData object. Does NOT write to the environment file
        """
        self.__cenvdata.set_first_failover_sd_name(str(self.failover_sd_line_edit_1.text()))
        self.__cenvdata.set_second_failover_sd_name(str(self.failover_sd_line_edit_2.text()))

    def __set_default_values_test_settings(self):
        """
        # Sets the default values for this panel
        """
        self.invert_pattern_qty_line_edit.setText(self.__cenvdata.get_invert_pattern_qty())

        self.packetdrop_uptime_line_edit.setText(self.__cenvdata.get_packetdrop_uptime())
        self.packetdrop_downtime_line_edit.setText(self.__cenvdata.get_packetdrop_downtime())

        self.switchdrop_uptime_line_edit.setText(self.__cenvdata.get_switchdrop_uptime())
        self.switchdrop_downtime_line_edit.setText(self.__cenvdata.get_switchdrop_downtime())

    def __save_test_settings(self):
        """
        ##  Retrieves the text in each text box and stores it in the
        ##  CEnvData object. Does NOT write to the environment file
        """
        self.__cenvdata.set_invert_pattern_qty(int(self.invert_pattern_qty_line_edit.text()))
        self.__cenvdata.set_packetdrop_downtime(int(self.packetdrop_downtime_line_edit.text()))
        self.__cenvdata.set_packetdrop_uptime(int(self.packetdrop_uptime_line_edit.text()))
        self.__cenvdata.set_switchdrop_downtime(int(self.switchdrop_downtime_line_edit.text()))
        self.__cenvdata.set_switchdrop_uptime(int(self.switchdrop_uptime_line_edit.text()))

    def __set_default_values_upgrade_clients(self):
        """
        # Reads saved upgrade data, establishes connection
        # between signals and slots.
        """
        self.clients_upgrade_table.setColumnWidth(0, 300)
        self.clients_upgrade_table.setColumnWidth(1, 60)
        self.clients_upgrade_table.setColumnWidth(2, 245)
        self.server_ip_line_edit.setInputMask("000.000.000.000;_")
        self._upgrade_clients_running = False
        self.upgrade_tool = CUpgradeTool()
        clients = self.upgrade_tool.get_clients()
        server_ip = self.upgrade_tool.server_ip
        installer_source = self.upgrade_tool.installer_source
        if clients:
            self.clients_upgrade_table.setRowCount(len(clients)+1)
            for i in range(len(clients)):
                self.clients_upgrade_table.setItem(i, 0, QtGui.QTableWidgetItem(clients[i][0]))
                combo = QtGui.QComboBox(self.clients_upgrade_table)
                combo.addItems(["win", "linux", "mac"])
                combo.setProperty("host", clients[i][0])
                combo.setCurrentIndex(combo.findText(clients[i][1]))
                self.clients_upgrade_table.setCellWidget(i, 1, combo)

                combo_logs = QtGui.QComboBox(self.clients_upgrade_table)
                combo_logs.setProperty("host", clients[i][0])
                self.clients_upgrade_table.setCellWidget(i, 2, combo_logs)

                combo.currentIndexChanged.connect(self.__upgrade_clients_os_changed)
        else:
            self.clients_upgrade_table.setRowCount(1)

        combo = QtGui.QComboBox(self.clients_upgrade_table)
        combo.addItems(["win", "linux", "mac"])
        combo.setCurrentIndex(-1)
        self.clients_upgrade_table.setCellWidget(self.clients_upgrade_table.rowCount()-1, 1, combo)
        combo_logs = QtGui.QComboBox(self.clients_upgrade_table)
        self.clients_upgrade_table.setCellWidget(self.clients_upgrade_table.rowCount()-1, 2, combo_logs)
        combo.currentIndexChanged.connect(self.__upgrade_clients_os_changed)

        if server_ip:
            self.server_ip_line_edit.setText(server_ip)
        if installer_source:
            index = self.installer_source_combo_box.findText(installer_source)
            self.installer_source_combo_box.setCurrentIndex(index)
        else:
            self.installer_source_combo_box.setCurrentIndex(-1)

        self.server_ip_line_edit.editingFinished.connect(self.__save_clients_upgrade)
        self.installer_source_combo_box.currentIndexChanged.connect(self.__save_clients_upgrade)
        self.clients_upgrade_push_button.clicked.connect(self.__upgrade_clients_action)
        self.clients_upgrade_table.itemChanged.connect(self.__upgrade_clients_host_changed)
        self.upgrade_tool.logs_changed.connect(self.__upgrade_clients_logs_changed)

    def __upgrade_clients_host_changed(self, changes):
        """
        # Triggered on client hostname change
        """
        self.clients_upgrade_table.cellWidget(self.clients_upgrade_table.currentRow(), 1).setProperty("host",
                                                                                                      changes.text())
        self.clients_upgrade_table.cellWidget(self.clients_upgrade_table.currentRow(), 2).setProperty("host",
                                                                                                      changes.text())

        if self.clients_upgrade_table.cellWidget(self.clients_upgrade_table.currentRow(), 1).currentIndex() != -1 \
                and changes.text() != ""\
                and self.clients_upgrade_table.currentRow() == self.clients_upgrade_table.rowCount() - 1:
            self.clients_upgrade_table.setRowCount(self.clients_upgrade_table.rowCount() + 1)
            combo = QtGui.QComboBox(self.clients_upgrade_table)
            combo.addItems(["win", "linux", "mac"])
            combo.setCurrentIndex(-1)
            self.clients_upgrade_table.setCellWidget(self.clients_upgrade_table.rowCount() - 1, 1, combo)
            combo_logs = QtGui.QComboBox(self.clients_upgrade_table)
            self.clients_upgrade_table.setCellWidget(self.clients_upgrade_table.rowCount() - 1, 2, combo_logs)
            combo.currentIndexChanged.connect(self.__upgrade_clients_os_changed)
        elif changes.text() == "" and self.clients_upgrade_table.rowCount() > 1:
            self.clients_upgrade_table.removeRow(self.clients_upgrade_table.currentRow())
        self.__save_clients_upgrade()

    def __upgrade_clients_os_changed(self, option):
        """
        # Triggered on client os change
        """
        if self.clients_upgrade_table.item(self.clients_upgrade_table.rowCount()-1, 0) \
                and self.sender().property("host") == self.clients_upgrade_table.item(self.clients_upgrade_table.rowCount()-1, 0).text() \
                and option != -1 \
                and self.sender().property("host") != "":
            self.clients_upgrade_table.setRowCount(self.clients_upgrade_table.rowCount() + 1)
            combo = QtGui.QComboBox(self.clients_upgrade_table)
            combo.addItems(["win", "linux", "mac"])
            combo.setCurrentIndex(-1)
            self.clients_upgrade_table.setCellWidget(self.clients_upgrade_table.rowCount() - 1, 1, combo)
            combo_logs = QtGui.QComboBox(self.clients_upgrade_table)
            self.clients_upgrade_table.setCellWidget(self.clients_upgrade_table.rowCount() - 1, 2, combo_logs)
            combo.currentIndexChanged.connect(self.__upgrade_clients_os_changed)
        self.__save_clients_upgrade()

    def __save_clients_upgrade(self):
        """
        # Runs after every client upgrade data change
        """
        clients = []
        for row in range(self.clients_upgrade_table.rowCount()-1):
            hostname = self.clients_upgrade_table.item(row, 0).text()
            os_type = self.clients_upgrade_table.cellWidget(row, 1).currentText()
            clients.append([hostname, os_type])
        self.upgrade_tool.save_data(self.server_ip_line_edit.text(), self.installer_source_combo_box.currentText(), clients)

    def __upgrade_clients_action(self):
        """
        # Runs client upgrade for all stored clients
        """
        self.clients_upgrade_table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.combo_logs = []
        for row in range(self.clients_upgrade_table.rowCount()):
            self.clients_upgrade_table.cellWidget(row, 1).setDisabled(True)
            self.combo_logs.append(self.clients_upgrade_table.cellWidget(row, 2))

        self.server_ip_line_edit.setDisabled(True)
        self.installer_source_combo_box.setDisabled(True)
        self.clients_upgrade_push_button.setDisabled(True)
        self._upgrade_clients_running = True
        self.upgrade_tool.upgrade()

    def __upgrade_clients_logs_changed(self, logs):
        """
        # Updates combobox for every client upgrade logs
        """
        for box in self.combo_logs:
                host = box.property("host")
                box.clear()
                box.setProperty("host", host)
                box.addItems(logs[host])
                box.setCurrentIndex(box.count()-1)

    def keyPressEvent(self, event):
        """
        # Deletes selected clients form client upgrade tab
        """
        if event.key() == QtCore.Qt.Key_Delete and self.tabWidget.currentIndex() == 7 and not self._upgrade_clients_running:
            for item in self.clients_upgrade_table.selectedItems():
                self.clients_upgrade_table.removeRow(item.row())
            self.__save_clients_upgrade()

    def __ping_host(self, hostname):
        """
        # Returns true if ping is successful.
        """
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        if IS_NT:
            ping_cmd = ["-4", "-n", "2", hostname]
        else:
            ping_cmd = ["-c", "2", hostname]
        ping_process = QtCore.QProcess(self)
        exit_code = ping_process.execute("ping", ping_cmd)

        QtGui.QApplication.restoreOverrideCursor()

        return bool(exit_code)

    def __set_np_default(self, my_np):
        """
        # Returns the list of default network providers.
        """
        net_providers = []

        # translate CIFS type into "CIFS" otherwise append at top
        if my_np:
            if my_np in ["cifs", "smbfs", MSWIN_NET_PROVIDER]:
                net_providers.append("CIFS")
            else:
                net_providers.append(my_np)

        for net_provider in [ISIS_NET_PROVIDER, MN_NET_PROVIDER, "CIFS"]:
            if net_provider not in net_providers:
                net_providers.append(net_provider)

        return net_providers


class OutLog:
    """
    # Class to redirect Stdout and Strerr to textbox
    # this class replace default stdout/stderror streams
    """
    def __init__(self, edit, out=None):
        """(edit, out=None) -> can write stdout, stderr to a
        QTextEdit.
        edit = QTextEdit
        out = alternate stream ( can be the original sys.stdout )
        """
        self.edit = edit
        self.out = out

    def write(self, text):
        """
        # Implements write functionality for stream
        """
        cursor = self.edit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        if self.out:
            self.out.write(text)

    def flush(self):
        """
        # flushes output of stream
        """
        if self.out:
            self.out.flush()

if __name__ == "__main__":

    cenvdata = util.cenvdata.CEnvData(load_regardless=True)
    app = QtGui.QApplication(sys.argv)
    mainwindow = CMainFrame(cenvdata)
    mainwindow.show()
    sys.exit(app.exec_())
