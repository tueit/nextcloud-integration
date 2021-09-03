import requests
import frappe
import urllib
from os import path, getcwd
import owncloud
from owncloud import HTTPResponseError

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

    remtote_path = ["ERPNext" , doc.attached_to_doctype , doc.attached_to_name]
    build_directory_structure(oc, remtote_path)

    remote_path_str = '/'.join(remtote_path) + '/' + doc.file_name
    oc.put_file(remote_path_str, file_path)

    if nextcloud_setting.migrate_to_nextcloud:
      update_with_link(doc, build_link(nextcloud_setting, remote_path_str))


def update_with_link(doc, link):
  frappe.db.set_value(doc.doctype, doc.name, 'file_url', link)

def build_directory_structure(oc, directories):
  for index, directory in enumerate(directories):
    folder = '/'.join(directories[0:index + 1])
    try:
      oc.mkdir(folder)
    except HTTPResponseError:
      pass

def checked_for_migration(doc):
  """
  Migrate Stuff to NextCloud
  """
  return doc.migrate_to_nextcloud


def build_link(settings, remote_file_path):
  dav_url = urllib.parse.urljoin(settings.nextcloud_url, settings.webdav_url) 
  return dav_url + '/' + remote_file_path


@frappe.whitelist()
def migrate_to_nextcloud():
  files = frappe.get_list('File')

  for f in files:
    if f.attached_to_doctype:
      pass