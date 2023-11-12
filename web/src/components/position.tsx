import React, { ReactNode } from 'react';
import styled from 'styled-components';

interface PositionedComponentProps {
  x: number;
  y: number;
  children: ReactNode;
}

const RelativeDiv = styled.div`
  position: relative;
`

const PositionedDiv = styled.div<{ x: number; y: number }>`
  position: absolute;
  left: ${(props) => props.x}px;
  top: ${(props) => props.y}px;
`;

const PositionedComponent: React.FC<PositionedComponentProps> = ({ x, y, children }) => 
<RelativeDiv>
  <PositionedDiv x={x} y={y}>{children}</PositionedDiv>
</RelativeDiv>
;

export default PositionedComponent;
