from flask import Response, jsonify, request, json
from flask.blueprints import Blueprint
from werkzeug.utils import secure_filename
import subprocess
import os
import sys
import zipfile
from amundsen_application.api.admin import exceptions

admin_blueprint = Blueprint('admin', __name__,url_prefix='/api/admin/v0')


## wallet needs to be in this directory
## /usr/lib/oracle/18.3/client64/lib/network/admin
## or you can put the wallet in any directory and change the directory name in sqlnet.ora
## and set the TNS_ADMIN environment variable to the new directory

UPLOAD_FOLDER = '/usr/lib/oracle/18.3/client64/lib/network/admin'
ALLOWED_EXTENSIONS = set(['zip'])

## Functions ##
def allowed_file(filename):
    '''
    Checks if file extension is valid
    '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@admin_blueprint.errorhandler(exceptions.DBError)
def handle_DB_error(error):
    '''
    Returns exception handling in JSON format
    '''
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

## Classes ##
class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


@admin_blueprint.route('/', methods=['POST','GET','DELETE'])
def sample_data():
    '''
    REST endpoint for accepting POST Request
    '''
    if request.method=='POST':

        ####### Check if POST request is of type application/json #############
        if request.is_json:

            print('Load Data Initiated')
            db_cred=json.loads(json.dumps(request.json))

            ## this should be the path where amundsendatabuilder lives on your client##
            path ='/home/opc/amundsen_lyft_app/v1_databuilder'

            ## Call sample_data_loader.py to load data
            python_bin=os.path.join(path,'venv/bin/python')
            script_file = os.path.join(path,'example/scripts/sample_oracle_loader.py')

            print('Extracting data from Autonomous Database')

            ## call and  execute sample_oracle_loader.py as a subprocess
            with cd(path):
                try:
                    subprocess.check_output([python_bin, script_file,db_cred['username'],db_cred['password'],db_cred['service']],
                                            stderr=subprocess.STDOUT)
                except subprocess.CalledProcessError:
                    raise exceptions.DBError('Could not connect DB. Check if username/password is correct. ',status_code=400)


            print('Database Successfully Loaded Into Amundsen')
            return jsonify({'message': 'Database Successfully Added Into Amundsen'})


        ############### check if the POST request is sending a file####################

        if 'filepond' not in request.files:
            response =jsonify({'message':'No File Part.Please try Again.'})
            return(response)


        file = request.files['filepond']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            response =jsonify({'message':'No Selected File. Please Try Again.'})
            return(response)


        if file and allowed_file(file.filename):

            print('File Upload Initiated')

            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

            print('Unzipping File')

            with zipfile.ZipFile(os.path.join(UPLOAD_FOLDER, filename), 'r') as zipref:
                zipref.extractall(UPLOAD_FOLDER)
                zipref.close()

            print ('File Succesfully Uploaded')
            response = jsonify({'message': 'File Succesfully Uploaded!'})
            return(response)

    return ('sample api landing page.')
