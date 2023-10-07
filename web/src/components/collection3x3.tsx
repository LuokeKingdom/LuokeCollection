import React from 'react';
import styled from 'styled-components';

const FlexContainer = styled.div`
  display: flex;
  flex-wrap: wrap;
  width: 500px;  // Total width of the container
  height: 500px;  // Total height of the container
  align-content: flex-start; // Ensures rows are stacked at the top
`;

const Box = styled.div`
  border: 1px solid #ccc;
  display: flex;
  justify-content: center;
  align-items: center;
  box-sizing: border-box;
  width: calc(33.33% - 10px);  // Deducting the gap width
  height: calc(33.33% - 10px); // Deducting the gap height
  margin: 5px;  // Half of the desired gap
`;

interface CollectionProps {
  items: React.ReactNode[];
  start_key?: number;
}

const Collection3x3: React.FC<CollectionProps> = ({ items, start_key=0 }) => {
  if (items.length !== 9) {
    throw new Error('The items prop must contain exactly 9 objects.');
  }

  return (
    <FlexContainer>
      {items.map((item, index) => (
        <Box key={index + start_key}>
          {item}
        </Box>
      ))}
    </FlexContainer>
  );
};

export default Collection3x3;
