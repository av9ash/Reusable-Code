from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
import re

class SPDownload:
    def __init__(self, url, target_dir='.'):
        self.site_url = "https://site_rul.com"
        self.client_id = "cid_here"
        self.client_secret = "c_secret_here"
        self.url = url
        self.dl_filename = url.split('/')[-1]
        self.dl_filename = self.dl_filename.split('&')[0]
        self.target_path = target_dir + "/" + self.dl_filename
        self.dl_link = ""
        self.__create_session()
        self.__get_link()
        self.download()

    def __create_session(self):
        try:
            self.ctx_auth = AuthenticationContext(self.site_url)
            self.ctx_auth.acquire_token_for_app(self.client_id, self.client_secret )
            self.ctx = ClientContext(self.site_url, self.ctx_auth)
            self.ctx.load(self.ctx.web)
            self.ctx.execute_query()
            return True
        except:
            return False

    def __get_link(self):
        mat = re.search(r'DocumentURL\=.*(\/sites\/engdoccenter\/[^&]+)\&\S+', self.url)
        if mat:
           self.dl_link = mat.group(1)
        else:
           print("Unsupport EngDoc Center sharepoint link format:", self.url)

    def download(self):
        if self.dl_link:
            response = File.open_binary(self.ctx, self.dl_link)
            with open(self.target_path, "wb") as f:
                f.write(response.content)
                f.close()
            print("Document saved to [{}].".format(self.target_path))
        else:
            print("Empty sharepoint download link, skipped.")
