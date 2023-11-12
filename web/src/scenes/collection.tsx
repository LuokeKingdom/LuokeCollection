import React from 'react';
import Collection3x3 from '../components/collection3x3';
import Background from '../components/background';
import Position from '../components/position';
import Center from '../components/center';
import Loader from '../components/loading';


const CollectionScene = () => {
    return (
        <Center>
        <Background width='1200px' height='800px' $image_url='training.png' >
        <Position x={130} y={180}>
            <Collection3x3 items={new Array(9).fill(0).map(x=><Loader />)} />
        </Position>
        </Background>
        </Center>
    )
}

export default CollectionScene