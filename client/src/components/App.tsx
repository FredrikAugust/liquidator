import React from 'react';

import styled from 'styled-components';

import GlobalStyle from '../styles/global';

import Button from './molecules/atoms/Button';

const TestSpace = styled.div`
  background: black;
  padding: 4em;
`;

const App: React.FC = () => (
  <>
    <GlobalStyle />
    <TestSpace>
      <Button.Raised>Sign up</Button.Raised>
      <Button.Raised invertedBg>Sign up</Button.Raised>
    </TestSpace>
    <h1>Welcome to Liquidator.</h1>
    <Button.Raised inverted>Sign up</Button.Raised>
  </>
);

export default App;
