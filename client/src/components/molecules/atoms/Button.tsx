import styled from 'styled-components';

const Button = styled.button`
  padding: .6em 3em;

  background: white;
  color: black;

  border-radius: 2px;
  border: none;

  box-shadow: -7px 7px 0 -1px black,
              -7px 7px 0 0px white;

  font-family: 'Roboto Mono', 'monospace';
  text-transform: uppercase;

  top: 0;
  left: 0;

  transition: box-shadow .3s, top .3s, left .3s;

  position: relative;
  outline: 0;

  &:hover {
    box-shadow: -4px 4px 0 -1px black,
                -4px 4px 0 0px white;
    top: 3px;
    left: -3px;
  }

  &:active {
    box-shadow: 0px 0px 0px black, 0px 0px 0px white;
    top: 7px;
    left: -7px;
  }
`;

export default Button;
