import * as React from 'react';
import { Form, IFields, required, isEmail} from "../Form";
import { Field } from "../Field";
import * as DocumentTitle from 'react-document-title';
import { Link } from 'react-router-dom';

export const database_type2 = "Azure";
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
  server: {
    id: "server",
    label: "Server Name",
    validation: { rule: required }
  }
};

export class AzurePage extends React.Component<{}, any> {
  constructor(props){
  super(props);

   this.state = {
         displayMenu: false,
       };

    this.showDropdownMenu = this.showDropdownMenu.bind(this);
    this.hideDropdownMenu = this.hideDropdownMenu.bind(this);

  };

  showDropdownMenu(event) {
      event.preventDefault();
      this.setState({ displayMenu: true }, () => {
      document.addEventListener('click', this.hideDropdownMenu);
      });
    }

    hideDropdownMenu() {
      this.setState({ displayMenu: false }, () => {
        document.removeEventListener('click', this.hideDropdownMenu);
      });

    }
  render() {

    return (
      <DocumentTitle title="Connect - Amundsen">
        <div className="container">
          <div className="row">
            <div className="col-xs-12">
              <h3 id="add-header">Connect an Azure Database</h3>
              <hr className="header-hr"/>
              <Form
                action="http://localhost:5000/api/admin/v0"
                fields={fields}
                render={() => (
                  <React.Fragment>
                    <div  className="dropdown" style = {{background:"#428bca",width:"200px"}} >
                      <div className="button" onClick={this.showDropdownMenu}> Select Database </div>
                      { this.state.displayMenu ? (
                      <ul>
                      <li><Link to="/oracle">Oracle Database</Link></li>
                      <li><Link to="/aurora">Amazon Aurora</Link></li>
                      </ul>
                      ):
                      (
                        null
                      )
                      }
                    </div>
                    <div className="alert alert-info" role="alert">
                      Enter your database credentials below to add your database to Amundsen.
                    </div>
                   <Field {...fields.username}/>
                   <Field {...fields.password}/>
                   <Field {...fields.server}/>
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

export default AzurePage;
