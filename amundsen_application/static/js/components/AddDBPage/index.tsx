import * as React from 'react';
import { Form, IFields, required, isEmail} from "./Form";
import { Field } from "./Field";
import * as DocumentTitle from 'react-document-title';
import { FilePond } from 'react-filepond';
import 'filepond/dist/filepond.min.css';

const fields: IFields = {
  username: {
    id: "username",
    label: "Username",
    validation: { rule: required }
  },
  password: {
    id: "password",
    label: "Password",
    editor: "password",
    validation: { rule: required }
  },
  service: {
    id: "service",
    label: "Service Name",
    validation: { rule: required }
  },
  database: {
    id: "database",
    label: "Database",
    editor: "dropdown",
    options: ["", "Oracle DB"],
    validation: { rule: required }
  },
};
export class AddDBPage extends React.Component {

  render() {
    return (
      <DocumentTitle title="AddDB - Amundsen">
        <div className="container">
          <div className="row">
            <div className="col-xs-12">
              <h3 id="add-header">Connect a New Database</h3>
              <hr className="header-hr"/>
              <Form
                action="http://localhost:5000/api/admin/v0"
                fields={fields}
                render={() => (
                  <React.Fragment>
                    <div className="alert alert-info" role="alert">
                      Enter your database credentials below to add your database to Amundsen.
                    </div>
                   <Field {...fields.username}    />
                   <Field {...fields.password} />
                   <Field {...fields.service}  />
                   <Field {...fields.database} />
                   <FilePond server='http://localhost:5000/api/admin/v0'/>
                   <br></br>
                   <br></br>
                  </React.Fragment>
              )}
            />
          </div>
        </div>
      </div>
      </DocumentTitle>
    );
  }
}

export default AddDBPage;
