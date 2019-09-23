import * as React from 'react';
import * as DocumentTitle from 'react-document-title';

import { shallow } from 'enzyme';

import { AzurePage } from '../';

describe('AzurePage', () => {
  const setup = () => {
    const wrapper = shallow<AzurePage>(<AzurePage/>)
    return { props, wrapper };
  };

  let props;
  let wrapper;

  beforeAll(() => {
    const setupResult = setup();
    props = setupResult.props;
    wrapper = setupResult.wrapper;
  });

  describe('render', () => {
    it('renders DocumentTitle w/ correct title', () => {
      expect(wrapper.find(DocumentTitle).props().title).toEqual('Connect - Amundsen');
    });

    it('renders correct header', () => {
      expect(wrapper.find('#add-header').text()).toEqual('Connect an Azure Database');
    });

    it('renders <hr>', () => {
      expect(wrapper.contains(<hr className="header-hr"/>));
    });

  });
});
