import React from 'react';
import styled from 'styled-components';

interface ContainerProps {
  width: string;
  height: string;
}
interface ImageProps {
  $image_url: string;
}
interface BackgroundProps {
  width: string;
  height: string;
  $image_url: string;
  children: React.ReactNode
}
const Container = styled.div<ContainerProps>`
  display: flex;
  width: ${props => props.width};
  height: ${props => props.height};
`


const ImageLayer = styled.div<ImageProps>`
  background-image: url(${props=>props.$image_url});
  flex:1;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  justify-content: center;
  align-items: center;
`;

const Background: React.FC<BackgroundProps> = ({ width, height, $image_url, children }) => {
  return (
    <Container width={width} height={height} >
        <ImageLayer $image_url={$image_url} >
            {children}
        </ImageLayer>
    </Container>
  )
}

export default Background