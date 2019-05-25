import React from 'react';

import { storiesOf } from '@storybook/react';
import Button from '../components/molecules/atoms/Button';

storiesOf('Button/Default/Light', module)
  .addDecorator(fn => <div style={{ padding: '3em' }}>{fn()}</div>)
  .add('inverted', () => <Button.Default inverted>Hello Button</Button.Default>)

storiesOf('Button/Default/Dark', module)
  .addDecorator(fn => <div style={{ padding: '2em', background: 'black' }}>{fn()}</div>)
  .add('default', () => <Button.Default>Hello Button</Button.Default>)
  .add('invertedBg', () => <Button.Default invertedBg>Hello Button</Button.Default>)

storiesOf('Button/Raised/Light', module)
  .addDecorator(fn => <div style={{ padding: '3em' }}>{fn()}</div>)
  .add('inverted', () => <Button.Raised inverted>Hello Button</Button.Raised>)

storiesOf('Button/Raised/Dark', module)
  .addDecorator(fn => <div style={{ padding: '3em', background: 'black' }}>{fn()}</div>)
  .add('default', () => <Button.Raised>Hello Button</Button.Raised>)
  .add('invertedBg', () => <Button.Raised invertedBg>Hello Button</Button.Raised>)