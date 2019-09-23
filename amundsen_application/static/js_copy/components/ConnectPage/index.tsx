import * as React from 'react';
import * as DocumentTitle from 'react-document-title';
import { Link } from 'react-router-dom';
import './styles.scss';

export class ConnectPage extends React.Component<{}, any> {
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
              <h3 id="add-header">Connect a New Database</h3>
              <hr className="header-hr"/>
              <div  className="dropdown" id="connect" style = {{background:"#428bca",width:"200px"}} >
                <div className="button" onClick={this.showDropdownMenu}> Select Database </div>
                { this.state.displayMenu ? (
                <ul>
                <li><Link id ="db" to="/oracle">Oracle Database</Link></li>
                <li><Link to="/azure">Microsoft Azure</Link></li>
                <li><Link to="/aurora">Amazon Aurora</Link></li>
                </ul>
                ):
                (
                  null
                )                  }
              </div>
          </div>
        </div>
      </div>
      </DocumentTitle>
    );
  }
}

export default ConnectPage;
