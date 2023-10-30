import React from 'react';
import './App.css';
import SplitBox from './components/collection/split_box';
import Collection3x3 from './components/collection/collection3x3';
import Square from './components/square';
import Background from './components/background';
import Position from './components/position';
import Center from './components/center';
import Loader from './components/loading';

function App() {
  return (
    <div className='App'>
    <Center>
    <Background width='1200px' height='800px' $image_url='training.png' >
      <SplitBox 
        left={<Collection3x3 items={new Array(9).fill(0).map(x=><Loader />)} />} 
        right={<Collection3x3 items={new Array(9).fill(0).map(x=><Loader />)} start_key={9} />} 
      />
    </Background>
    </Center>
    </div>
  );
}

export default App;
