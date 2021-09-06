// Copyright (c) 2021, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('NextCloud Print List', {
	doc_type(frm, cdt, cdn) {
		frappe.db.get_list('Print Format',{filters:[['doc_type', '=', frm.doc.doc_type]]})	
		.then(data => {
			const ops = data.map(each => each.name)
			frm.set_df_property('print_format', 'options', ['Standard', ...ops])
		})
	}
});
