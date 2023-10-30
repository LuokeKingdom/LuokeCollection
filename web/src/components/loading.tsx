// Loader.tsx
import React from 'react';
import styled, { keyframes } from 'styled-components';

// Create the keyframes for the spin animation
const spin = keyframes`
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
`;

// Create a styled div for the loader
const LoaderContainer = styled.div`
  border: 4px solid rgba(0, 0, 0, 0.1);
  width: 50px;
  height: 50px;
  border-radius: 50%;
  border-left-color: #282c34;

  animation: ${spin} 1s linear infinite;
`;

const Loader: React.FC = () => {
  return <LoaderContainer />;
};

export default Loader;
