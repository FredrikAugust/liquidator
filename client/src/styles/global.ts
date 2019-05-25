import { createGlobalStyle } from 'styled-components';

/**
 * This file should be used for things that are global to the entire
 * application, such as resets and standards.
 */

const GlobalStyle = createGlobalStyle`
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
`;

export default GlobalStyle;
