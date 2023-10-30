import React, { ReactNode } from 'react';
import styled from 'styled-components';

interface CenteredComponentProps {
  children: ReactNode;
}

// Styled component
const CenteredDiv = styled.div`
  flex:1;
  display: flex;
  justify-content: center;
  align-items: center;
`;

const CenteredComponent: React.FC<CenteredComponentProps> = ({ children }) => {
  return <CenteredDiv>{children}</CenteredDiv>;
};

export default CenteredComponent;
