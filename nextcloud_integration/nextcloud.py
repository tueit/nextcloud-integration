import requests
import frappe
import urllib
from os import path, getcwd
import owncloud


def save_to_nextcloud(doc, event=None):
    nextcloud_setting = frappe.get_single('Nextcloud Setting')
    username = nextcloud_setting.nextcloud_username
    password = nextcloud_setting.get_password('password')
    cloud_url = nextcloud_setting.nextcloud_url

    session = requests.Session()
    session.auth = (username, password)
    site_path = frappe.utils.get_site_path()

    if not doc.is_private:
      file_path = site_path + '/public' + doc.file_url 
    else:
      file_path = site_path + doc.file_url

    oc = owncloud.Client(cloud_url)
    oc.login(username, password)
    oc.put_file('local.pdf', file_path)