import React from 'react';
import './App.css';
import SplitBox from './components/split_box';
import Collection3x3 from './components/collection3x3';
import Square from './components/square';

function App() {
  return (
    <div className="App">
      <SplitBox 
        left={<Collection3x3 items={new Array(9).fill(0).map(x=><Square />)} />} 
        right={<Collection3x3 items={new Array(9).fill(0).map(x=><Square />)} start_key={9} />} 
      />
    </div>
  );
}

export default App;
