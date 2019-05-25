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
      <Button>Sign up</Button>
    </TestSpace>
    <h1>Welcome to Liquidator.</h1>
  </>
);

export default App;
