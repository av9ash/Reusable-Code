from app import tango
from archive import credentials
import sharepy
import json
import os
import time


class Sharepoint(object):
    def __init__(self):
        self.username = credentials.DEEPTHOUGHT['user']
        self.password = credentials.DEEPTHOUGHT['password']

        self.jnpr_sp = 'https://yourdomain.sharepoint.com'
        self.site_name = '/tide/tango'
        self.headers = {"accept": "application/json;odata=verbose",
                        "content-type": "application/x-www-urlencoded; charset=UTF-8"}

    def authenticate(self):
        # Authenticating session takes time so load one if already done.
        try:
            sp_path = os.getcwd() + '/sp-session.pkl'
            print(sp_path)
            if time.time() - os.path.getmtime(sp_path) > 900:
                os.remove(sp_path)
            self.sp_conn = sharepy.load()
        except FileNotFoundError:
            self.sp_conn = sharepy.connect(self.jnpr_sp, username=self.username + '@yourdomain.net',
                                           password=self.password)
            self.sp_conn.save()

    def upload_to_sharepoint(self, file_name, target_location, content):
        """
        Upload content to target location with specified file name.

        input:
        :param file_name: Ex: 77985.docx,
        :param target_location: 77985
        :param content: bytes
        :return: json
        """
        self.authenticate()
        print('Creating folder')
        p = self.sp_conn.post(self.jnpr_sp + "/sites" + self.site_name + "/_api/web/folders",
                              json={
                                  "__metadata": {"type": "SP.Folder"},
                                  "ServerRelativeUrl": 'Shared Documents/testplans/' + target_location
                              })

        print(p.status_code)
        print('Saving File')
        p = self.sp_conn.post(
            self.jnpr_sp + "/sites" + self.site_name +
            "/_api/web/GetFolderByServerRelativeUrl('Shared Documents/testplans/"
            + target_location + "')/Files/add(url='" + file_name + "',overwrite=true)",
            data=content, headers=self.headers)

        print(p.status_code)
        if p.status_code == 200:
            msg = self.jnpr_sp + '/sites' + self.site_name + '/Shared%20Documents/testplans/' + target_location
        else:
            msg = 'Ran into an error. Status Code: ' + str(p.status_code)

        return json.dumps(msg)

    def get_file_meta(self, filename):
        """
        Get the metadata for input file name.

        Makes call to multiple apis.

        :param filename: Ex: 63924.pdf, 79036.docx, 77985.pdf
        :return: Dictionary
        """
        self.authenticate()
        # username = credentials.DEEPTHOUGHT['user']
        # password = credentials.DEEPTHOUGHT['password']
        # jnpr_sp = 'https://yourdomain.sharepoint.com'

        result = {}
        if '.' not in filename:
            return json.dumps("Missing file extension.")
        else:
            tpid = filename.split('.')[0]

        # Authenticating session takes time so load one if already done.
        #     try:
        #         sp_conn = sharepy.load()
        #     except FileNotFoundError:
        #         sp_conn = sharepy.connect(jnpr_sp, username=username + '@yourdomain.net', password=password)
        #         sp_conn.save()

        query_created_details = "https://yourdomain.sharepoint.com/sites/tide/tango/_api/web" \
                                "/GetFolderByServerRelativeUrl('Shared Documents/testplans/" + str(
            tpid) + "/')/Files"
        p = self.sp_conn.get(query_created_details)
        if p.status_code == 200:
            meta = json.loads(p.content)['d']['results']
            for item in meta:
                # print(item['TimeCreated'], item['TimeLastModified'], item['UIVersionLabel'])
                result['TimeCreated'] = item['TimeCreated']
                result['TimeLastModified'] = item['TimeLastModified']
                result['UIVersionLabel'] = item['UIVersionLabel']
        else:
            result['Error ' + str(p.status_code)] = 'Unable to get document creation/modification details'

        result['Versions'] = self.get_history_versions(tpid, filename)

        query_modified_by = "https://yourdomain.sharepoint.com/sites/tide/tango/_api/Web" \
                            "/GetFileByServerRelativePath(" \
                            "decodedurl='/sites/tide/tango/Shared%20Documents/testplans/" + str(
            tpid) + "/" + filename + "')/ModifiedBy"
        p = self.sp_conn.get(query_modified_by)
        if p.status_code == 200:
            meta = json.loads(p.content)['d']
            # print(meta['Title'], meta['Email'])
            result['Username'] = meta['Title']
            result['Email'] = meta['Email']

        else:
            result['Error ' + str(p.status_code)] = 'Unable to get document user details'

        return result

    def get_history_versions(self, tpid, filename):
        """
        Get list of all history versions.

        :param tpid: Ex 77985
        :param filename: Ex 77985.docx
        :return: list
        """
        self.authenticate()
        query_versions = "https://yourdomain.sharepoint.com/sites/tide/tango/_api/Web" \
                         "/GetFileByServerRelativePath(decodedurl='/sites/tide/tango/Shared%20Documents/testplans/" + \
                         str(
                             tpid) + "/" + filename + "')/Versions"
        p = self.sp_conn.get(query_versions)
        versions = {}
        if p.status_code == 200:
            meta = json.loads(p.content)['d']['results']
            for item in meta:
                versions[item['VersionLabel']] = item['Url']
            return versions
        else:
            return 'Unable to get document versions details'

    # @tango.tools.json_out()
    def get_file(self, target_location, file_name):
        """
        Download file content in bytes from sharepoint.

        :param target_location: 77985
        :param file_name: 77985.docx
        :return: bytes
        """
        self.authenticate()
        path = "https://yourdomain.sharepoint.com/sites/tide/tango/Shared%20Documents/testplans{}{}".format(
            target_location, file_name)

        r = self.sp_conn.get(path)

        return r

    def get_file_version(self, file_name, version):
        """
        Get the specified version of the document.

        input: filename.
        version:

        :param filename: Ex: 63924.pdf or 79036.docx
        :param version: 1.0 or 2.0
        :return: sharepoint link to file
        """
        self.authenticate()
        result = {}

        if '.' not in file_name:
            return json.dumps("Missing file extension.")
        else:
            tpid = file_name.split('.')[0]

        query_versions = "https://yourdomain.sharepoint.com/sites/tide/tango/_api/Web" \
                         "/GetFileByServerRelativePath(decodedurl='/sites/tide/tango/Shared%20Documents/testplans/" + \
                         str(
                             tpid) + "/" + file_name + "')/Versions"
        p = self.sp_conn.get(query_versions)
        if p.status_code == 200:
            for file_details in json.loads(p.content)['d']['results']:
                if file_details['VersionLabel'] == str(version):
                    url = "https://yourdomain.sharepoint.com/sites/tide/tango/" + file_details['Url']
                    resp = self.sp_conn.get(url)
                    if resp.status_code == 200:
                        return resp.content
                    else:
                        result['Error ' + str(p.status_code)] = 'Unable to get document from SP.'
        else:
            result['Error ' + str(p.status_code)] = 'Unable to get document link.'

        return result

# Driver code
# tpid = '10022-1'
# sp = Sharepoint()
# # versions = sp.get_file_version(str(tpid) + '.pdf','1.0')
# versions = sp.get_history_versions(tpid, str(tpid) + '.pdf')
# print(versions)
