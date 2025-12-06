import requests
import zipfile
import io
import os
import shutil
from .basics.abstr import abstract_executable

def download_repo_zip(repo_url, target_dir):
    try:
        # convert to zip
        if repo_url.endswith('.git'):
            repo_url = repo_url[:-4]
        if repo_url.startswith('https://github.com'):
            zip_url = repo_url.replace('https://github.com', 'https://api.github.com/repos') + '/zipball/main'
        else:
            raise ValueError("Unsupprotable url.")
        
        # Downloading zip
        response = requests.get(zip_url)
        response.raise_for_status()
        
        # Delete result dir if then exist
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        
        # Unpack zip
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            # Creating temp dir for unpack
            temp_dir = "./temp_extract"
            zip_file.extractall(temp_dir)
            
            # Move content
            extracted_items = os.listdir(temp_dir)
            if extracted_items:
                repo_content_dir = os.path.join(temp_dir, extracted_items[0])
                shutil.move(repo_content_dir, target_dir)
            
            # Deleting tem dir
            shutil.rmtree(temp_dir)
        
        print(f"Reposetory successfully downloaded to {target_dir}")
        return True
        
    except Exception as e:
        print(f"Zip-Downloading Error: {e}")
        return False



class Github(abstract_executable):
    def __init__(self):
        super().__init__()
        self._name = 'github'
        self.commands = {
            'download': {'commnd': self.get, 'min_args': 2, 'args': ['repo_url', 'target_dir']},
            '-d': 'download',
            'help': {'commnd': self.help, 'min_args': 0}, 
            '-h': 'help',
        }
        
    def help(self):
        text = \
'''download  (-d) : download repo to taret dir
help (-h) : show that message'''
        self.out.output(
            self.out.text_to_frame(text)
        )
        
    def get(self, *args):
        repo = args[0]
        target = args[1]
        download_repo_zip(repo, target)