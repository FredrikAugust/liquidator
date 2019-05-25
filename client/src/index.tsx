import React from 'react';
import ReactDOM from 'react-dom';

import App from './App';

import * as serviceWorker from './serviceWorker';
ReactDOM.render(<App />, document.getElementById('root'));

// This will only actually be enabled when we're in production, aka.
// with the output of `npm build`.
serviceWorker.register();
