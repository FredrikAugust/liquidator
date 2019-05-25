import { createGlobalStyle } from 'styled-components';

/**
 * This file should be used for things that are global to the entire
 * application, such as resets and standards.
 */

const GlobalStyle = createGlobalStyle`
    @import url('https://fonts.googleapis.com/css?family=Roboto+Mono:300,400&display=swap');

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
`;

export default GlobalStyle;
