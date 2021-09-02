import frappe

def save_pdf(doc, method=None):
	"""
	Save PDF
	"""
	if not is_doctype_allowed(doc):
		return

	print_format = get_print_format(doc)


def upload_pdf():
	"""
	Upload PDF to Nextcloud
	"""
	pass


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

	return doc not in allowed_doctypes