# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from .nextcloud import save_to_nextcloud

__version__ = '0.0.1'


@frappe.whitelist()
def migrate_to_nextcloud():
	files = frappe.get_list('File')
	for f in files:
		frappe.enqueue('nextcloud_integration.nextcloud.save_to_nextcloud', doc=f)
