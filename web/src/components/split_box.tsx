import React from 'react';
import styled from 'styled-components';

const Container = styled.div`
  display: flex;
  border: 1px solid #ccc;  // Optional: add a border around the whole container
`;

const Box = styled.div`
  flex: 1;  // This ensures both boxes take up equal width
  padding: 10px;  // Some padding for aesthetics
  box-sizing: border-box;  // This ensures padding and border are included in width and height

  &:first-child {
    border-right: 1px solid #ccc;  // Separator line
  }
`;

interface SplitBoxProps {
  left: React.ReactNode;
  right: React.ReactNode;
}

const SplitBox: React.FC<SplitBoxProps> = ({ left, right }) => {
  return (
    <Container>
      <Box>{left}</Box>
      <Box>{right}</Box>
    </Container>
  );
};

export default SplitBox;
