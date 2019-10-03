import * as React from 'react';
import { Form, IFields, required, isEmail} from "../Form";
import { Field } from "../Field";
import * as DocumentTitle from 'react-document-title';
import { FilePond } from 'react-filepond';
import { Link } from 'react-router-dom';
import "../filepond.min.css";

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
  }
};
export class OraclePage extends React.Component<{}, any> {
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
              <h3 id="add-header">Connect an Oracle Database</h3>
              <hr className="header-hr"/>
              <Form
                action="http://129.213.125.129:5000/api/admin/v0"
                fields={fields}
                render={() => (
                  <React.Fragment>
                    <div  className="dropdown" style = {{background:"#428bca",width:"200px"}} >
                      <div className="button" onClick={this.showDropdownMenu}> Select Database </div>
                      { this.state.displayMenu ? (
                      <ul id="dbUl">
                      <li id="dbLi"><Link to="/azure">Microsoft Azure</Link></li>
                      <li id="dbLi"><Link to="/aurora">Amazon Aurora</Link></li>
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
                   <Field {...fields.service} />
                   <FilePond
                    server="http://129.213.125.129:5000/api/admin/v0"
                    labelIdle="<span style='color:#31708f'>Drag & Drop your Cloud Wallet or <span class='filepond--label-action style='color:#31708f'>Browse</span></span>"
                    />
                    <br></br>
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

export default OraclePage;
