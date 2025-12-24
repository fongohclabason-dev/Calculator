import React from 'react'
import './Display.css'

export default function Display({ display, memory, onMemoryAdd, onMemoryClear }) {
  return (
    <div className="display-container">
      {memory !== 0 && (
        <div className="memory-indicator">
          <span>M: {memory.toFixed(2)}</span>
          <button onClick={onMemoryClear} className="memory-clear-btn">Clear</button>
        </div>
      )}
      <div className="display">
        {display}
      </div>
      <button onClick={onMemoryAdd} className="memory-add-btn">M+</button>
    </div>
  )
}
