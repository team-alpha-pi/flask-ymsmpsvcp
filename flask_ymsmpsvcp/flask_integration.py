from .crawl_logic import Routes
from flask import Flask, current_app, Blueprint
import yaml

bp = Blueprint('crawl', __name__, static_folder=None)

@bp.route('/')
def get_root():
    return current_app.config['YMSMPSCCP_TREE'].root.to_json()

    
class YMSMPSCCP:
    def __init__(self, app=None, settings_info_yaml_path=None):
        self.app: Flask = app
        if app is not None and settings_info_yaml_path is not None:
            self.init_app(app, settings_info_yaml_path)
        else:
            raise RuntimeError('Either all or none of the arguments must be passed')


    def init_app(self, app, settings_info_yaml_path):
        self.app = app
        with open(settings_info_yaml_path, 'r') as f:
            settings_yaml = yaml.safe_load(f)

        def build_tree():
            app.config['YMSMPSCCP_TREE'] = Routes(list(app.url_map.iter_rules()), settings_yaml)
        
        self.app.before_first_request(build_tree)
        self.app.register_blueprint(bp)


    def hide(self, fx_name):
        self.app.config['YMSMPSCCP_TREE'].hide(fx_name)
    
    def unhide(self, fx_name):
        self.app.config['YMSMPSCCP_TREE'].unhide(fx_name)

    