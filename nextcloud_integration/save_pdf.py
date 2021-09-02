import frappe
import requests
from frappe.utils.file_manager import save_file, save_file_on_filesystem


def save_pdf(doc, method=None):
	"""
	Save PDF
	"""
	if not is_doctype_allowed(doc):
		return

	print_format = get_print_format(doc.doctype)
	pdf = get_pdf_data(doc.doctype, doc.name, print_format)
	save_and_attach(pdf, doc.doctype, doc.name)


def get_pdf_data(doctype, name, print_format):
	"""
	Get PDF Data
	"""
	html = frappe.get_print(doctype, name, print_format=print_format)
	return frappe.utils.pdf.get_pdf(html)


def save_and_attach(content, to_doctype, to_name):
		file_name = "{}.pdf".format(to_name)
		save_file(file_name, content, to_doctype, to_name, is_private=1)


def get_print_format(item):
	"""
	Get Print Format
	"""
	return frappe.get_doc('NextCloud Print List', item).print_format
	

def is_doctype_allowed(doc):
	"""
	Is Doctype Allowed
	"""
	doctypes = frappe.get_list('NextCloud Print List')
	allowed_doctypes = [doc.name for doc in doctypes]
	return doc.doctype in allowed_doctypes
