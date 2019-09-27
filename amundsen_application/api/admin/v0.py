from flask import Response, jsonify, make_response, request, json
from flask.blueprints import Blueprint
from werkzeug.utils import secure_filename
import subprocess
import os
import sys
import zipfile
from amundsen_application.api.admin import exceptions
from sqlalchemy import exc
from amundsen_application.api.admin import adw_extract

admin_blueprint = Blueprint('admin', __name__,url_prefix='/api/admin/v0')

@admin_blueprint.errorhandler(exceptions.DBError)
def handle_DB_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

## wallet needs to be in this directory
## /usr/lib/oracle/18.3/client64/lib/network/admin
UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = set(['zip','csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin_blueprint.route('/', methods=['POST','GET','DELETE'])
def sample_data():
    if request.method=='POST':
        ####### Check if POST request is of type application/json #############
        if request.is_json:

            print('Load Data Initiated')
            db_cred=json.loads(json.dumps(request.json))

            ##change this path to where amundsendatabuilder lives on your client##
            path ='/home/opc/amundsen_lyft_app/v1_databuilder'

            ## Call sample_data_loader.py to load data
            python_bin=os.path.join(path,'venv/bin/python')
            script_file = os.path.join(path,'example/scripts/sample_oracle_loader.py')

            print('Extracting data from ADW')

            with adw_extract.cd(path):
                try:
                    subprocess.check_output([python_bin, script_file,db_cred['username'],db_cred['password'],db_cred['service']],
                                            stderr=subprocess.STDOUT)
                except subprocess.CalledProcessError:
                    raise exceptions.DBError('Could not connect DB. Check if username/password is correct. ',status_code=400)

                    # subprocess.Popen([python_bin, script_file,db_cred['username'],db_cred['password'],db_cred['service']])

            return jsonify({'message': 'Database Succesfully Added Into Amundsen'})

            # except sqlalchemy.exc.DatabaseError as err:
            # except:
            #     # if err.orig.args[0]== 1017:
            #     #     raise exceptions.DBError('Username/Password Incorrect',status_code=400)
            #     # if err.orig.args[0]== 12154:
            #     #     raise exceptions.DBError('Service Name is Incorrect or Wallet File Has Not Been Uploaded',status_code=400)
            #     raise exceptions.DBError('db error',status_code=400)


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
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

            with zipfile.ZipFile(os.path.join(UPLOAD_FOLDER, filename), 'r') as zipref:
                zipref.extractall(UPLOAD_FOLDER)
                zipref.close()


            response = jsonify({'message': 'File Succesfully Uploaded!'})
            return(response)

    return ('sample api landing page')
