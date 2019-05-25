import styled from 'styled-components';

interface IButtonProps {
  inverted?: boolean;
  invertedBg?: boolean;
}

const Button = styled.button<IButtonProps>`
  padding: .7em 1em;
  text-transform: uppercase;
  outline: 0;
  cursor: pointer;

  /* CSS variable declaration */
  --bg: ${(props) => props.invertedBg || props.inverted ? 'white' : 'black'};
  --fg: ${(props) => props.invertedBg || props.inverted ? 'black' : 'white'};
  --border-color: ${(props) => props.inverted ? 'black' : 'white'};

  background: var(--bg);
  color: var(--fg);

  border: 1px solid var(--border-color);
  border-radius: 2px;

  margin-top: 0;
  transition: border .2s, margin-top .2s;

  &:hover {
    ${(props) => props.invertedBg ? `
      color: white;
      background: black;
    ` : ``}
    border-top: 1px solid rgba(0,0,0,0);
    border-left: 1px solid rgba(0,0,0,0);
    border-right: 1px solid rgba(0,0,0,0);
    border-bottom: 1px solid var(--border-color);
  }

  &:active {
    border-bottom: 7px solid var(--border-color);
    margin-top: -6px;
  }
`;

const RaisedButton = styled.button<IButtonProps>`
  padding: .8em 2.3em;
  font-size: 1.1em;
  font-weight: 600;
  cursor: pointer;

  margin: 3px 3px 10px 10px;

  font-family: 'Roboto Mono', 'monospace';
  text-transform: uppercase;

  top: 0;
  left: 0;
  position: relative;

  transition: box-shadow .2s, top .2s, left .2s;

  outline: 0;

  border-radius: 2px;

  /* CSS variable declaration */
  --bg: ${(props) => props.invertedBg || props.inverted ? 'black' : 'white'};
  --fg: ${(props) => props.invertedBg || props.inverted ? 'white' : 'black'};
  --border-color: ${(props) => props.inverted ? 'black' : 'white'};
  --box-shadow-fill: ${(props) => props.inverted ? 'white' : 'black'};
  --box-shadow-border: ${(props) => props.inverted ? 'black' : 'white'};

  background: var(--bg);
  color: var(--fg);

  border: 2px solid var(--border-color);

  box-shadow: -7px 7px 0 -1px var(--box-shadow-fill),
              -7px 7px 0 0px var(--box-shadow-border);

  &:hover {
    box-shadow: -5px 4px 0 -1px var(--box-shadow-fill),
                -5px 4px 0 0px var(--box-shadow-border);
    top: 2px;
    left: -2px;
  }

  &:active {
    box-shadow: 0px 0px 0px var(--fg), 0px 0px 0px var(--bg);
    top: 7px;
    left: -7px;
  }
`;

export default { Raised: RaisedButton, Default: Button };
